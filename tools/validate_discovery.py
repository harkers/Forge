#!/usr/bin/env python3
# Managed by harkers/repo-standards at revision 1ccc10ee. Use .repo-standards.yml overrides instead of editing this header away.
"""Validate infrastructure discovery records (standards/infrastructure-discovery.md).

A record says what an agent verified about one host before a task touched it:
claimed against observed values, their sources, whether each discrepancy is
material, and the decision taken. The JSON Schema covers structure; this tool
adds the cross-field rules, so a submitted record cannot claim a decision the
standard does not allow.

Scope (Phase 1): this validates the records it is given. It is not a runtime
control: it cannot stop an agent acting on a host before writing a record, and
nothing yet makes a record mandatory for a task (a Phase 2 gate). Its secret
scan is defence in depth only and is not comprehensive: gitleaks (RS-SEC-001)
remains the mandatory secret control.

Usage:
    validate_discovery.py                          # every record under evidence/infrastructure-discovery/ (recursive)
    validate_discovery.py path/to/record.json      # named records
    validate_discovery.py --require --task 11      # fail unless one valid record exists for task 11
    validate_discovery.py --packet docs/completion/ISSUE-11-completion-packet.md --task 11
    validate_discovery.py --require --task 11 --max-age 1d   # a current check: reject older records

Timestamps are RFC 3339 date-times with an explicit offset (`Z` or `+hh:mm`).
A record up to CLOCK_SKEW (5 minutes) ahead of this clock is accepted; later
is "in the future". There is no default expiry: historical records stay valid
for audit, and a caller that needs current evidence passes --max-age.

Exit codes: 0 valid (or nothing to check without --require), 1 invalid or
required record missing, 2 usage error. Log level: --verbose, or LOG_LEVEL
(default INFO).
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCHEMA = ROOT / "schemas" / "infrastructure-discovery-record.schema.json"
DEFAULT_DIR = Path("evidence") / "infrastructure-discovery"
#: Tolerance for a record timestamped slightly ahead of this machine's clock.
CLOCK_SKEW = timedelta(minutes=5)

LOG = logging.getLogger("validate_discovery")

#: Categories whose discrepancy is material by definition (the standard's list).
MATERIAL_CATEGORIES = {
    "production_host",
    "database",
    "deployment_target",
    "service_identity",
    "schema_version",
    "credential_scope",
}

#: Categories whose observed value names the machine the operation acts on;
#: work may only proceed when one was observed and it is the record's host.
TARGET_CATEGORIES = {"production_host", "deployment_target"}

PROCEED_OUTCOMES = {"proceed_as_documented", "proceed_with_verified"}

# RFC 3339 date-time with a mandatory offset (Z or +hh:mm).
_RFC3339 = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})$"
)

# --- secret scan: defence in depth only; gitleaks is the control ----------

#: Shapes that are a credential value wherever they appear.
SECRET_SHAPES = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{2,}\.[A-Za-z0-9_-]{2,}"),  # JWT
    re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/-]{16,}=*"),
    re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b"),
    re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    re.compile(r"\bAGE-SECRET-KEY-1[0-9A-Z]{50,}\b"),
    re.compile(r"\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@"),  # credentials in a URL
)

#: `password=<value>`: any literal value is a credential value.
_PASSWORD_ASSIGN = re.compile(
    r"(?i)\b(?:password|passwd|passphrase|pwd)\b\s*(?:[:=]|\bis\b)\s*(\S+)"
)
#: `token: <value>`: a credential value only when the value looks like one.
_TOKEN_ASSIGN = re.compile(
    r"(?i)\b(?:token|secret|api[_-]?key|access[_-]?key|client[_-]?secret)\b\s*[:=]\s*(\S+)"
)
#: First words of a credential REFERENCE (where it lives), not a VALUE.
REFERENCE_WORDS = {
    "stored", "in", "keychain", "infisical", "see", "kept", "held", "lives", "rotated",
    "redacted", "from", "at", "via", "env", "environment", "vault", "file", "not", "none",
    "n/a", "managed", "item", "read", "named", "the",
}


def _is_reference(value: str) -> bool:
    word = value.strip("\"'`,.;()[]").lower()
    return word in REFERENCE_WORDS or word.startswith(("<", "$", "*"))


def _looks_like_value(value: str) -> bool:
    value = value.strip("\"'`,.;()[]")
    return len(value) >= 12 and bool(re.search(r"[A-Za-z]", value)) and bool(re.search(r"\d", value))


def contains_secret(text: str) -> bool:
    """True when `text` appears to hold a credential value (not a reference to one)."""
    if any(p.search(text) for p in SECRET_SHAPES):
        return True
    if any(not _is_reference(m.group(1)) for m in _PASSWORD_ASSIGN.finditer(text)):
        return True
    return any(
        not _is_reference(m.group(1)) and _looks_like_value(m.group(1))
        for m in _TOKEN_ASSIGN.finditer(text)
    )


# --- record rules ----------------------------------------------------------


def load_schema(schema_path: Path | None = None) -> dict[str, Any]:
    return json.loads((schema_path or DEFAULT_SCHEMA).read_text(encoding="utf-8"))


def parse_timestamp(value: Any) -> datetime | None:
    """A timezone-aware RFC 3339 date-time, or None."""
    if not isinstance(value, str) or not _RFC3339.match(value):
        return None
    try:
        # The pattern requires an offset, so the result is always timezone-aware.
        return datetime.fromisoformat(value.replace("z", "Z").replace("t", "T"))
    except ValueError:
        return None


FORMAT_CHECKER = jsonschema.FormatChecker()


@FORMAT_CHECKER.checks("date-time")
def _date_time(value: object) -> bool:
    return not isinstance(value, str) or parse_timestamp(value) is not None


def _norm(value: Any) -> str | None:
    return value.strip().casefold() if isinstance(value, str) else None


def is_discrepancy(check: dict[str, Any]) -> bool:
    """A claim was made and the observation differs from it (or could not be made).

    Comparison ignores case and surrounding whitespace.
    """
    claimed = _norm(check.get("claimed"))
    if claimed is None:
        return False
    return claimed != _norm(check.get("observed"))


def _blank(value: Any) -> bool:
    return not isinstance(value, str) or not value.strip()


def _strings(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        return [s for v in value.values() for s in _strings(v)]
    if isinstance(value, list):
        return [s for v in value for s in _strings(v)]
    return []


def semantic_errors(
    record: dict[str, Any],
    now: datetime | None = None,
    max_age: timedelta | None = None,
) -> list[str]:
    errors: list[str] = []
    checks = record.get("checks") or []
    decision = record.get("decision") or {}
    outcome = decision.get("outcome")
    host = record.get("host") or {}
    host_names = {_norm(host.get(k)) for k in ("name", "address") if host.get(k)}
    proceeds = outcome in PROCEED_OUTCOMES

    discrepancies: list[dict[str, Any]] = []
    observed_targets = 0
    for index, check in enumerate(checks):
        where = f"checks/{index} ({check.get('item', '?')})"
        disc = is_discrepancy(check)
        if disc:
            discrepancies.append(check)
        claimed, observed = check.get("claimed"), check.get("observed")
        category = check.get("category")
        if disc and category in MATERIAL_CATEGORIES and not check.get("material"):
            errors.append(f"{where}: a {category} discrepancy is material by definition")
        if not disc and check.get("material"):
            errors.append(f"{where}: marked material but claimed and observed agree")
        if claimed is not None and observed is None and not check.get("material"):
            errors.append(
                f"{where}: an unobservable value cannot be treated as non-material; "
                "what could not be verified may be wrong"
            )
        if claimed is None and observed is None and outcome != "stopped_escalated":
            errors.append(f"{where}: nothing was claimed or observed, so nothing was verified")
        if category in TARGET_CATEGORIES and observed is not None:
            observed_targets += 1
            if proceeds and host_names and _norm(observed) not in host_names:
                errors.append(
                    f"{where}: observed target {observed!r} is not the record's host "
                    f"({', '.join(sorted(n for n in host_names if n))})"
                )

    if proceeds and observed_targets == 0:
        errors.append(
            "checks: no observed target (production_host or deployment_target); "
            "work cannot proceed against a target nobody verified"
        )

    material = [c for c in discrepancies if c.get("material")]
    any_material = bool(material)
    if bool(record.get("material")) != any_material:
        errors.append(f"material: is {record.get('material')} but the checks say {any_material}")

    if outcome == "proceed_with_verified" and not discrepancies:
        errors.append(
            "decision/outcome: proceed_with_verified with no discrepancy; use proceed_as_documented"
        )
    if any_material and outcome not in {"stopped_escalated", "proceed_with_verified"}:
        errors.append(
            "decision/outcome: a material discrepancy must end in stopped_escalated or "
            f"proceed_with_verified, not {outcome}"
        )
    if discrepancies and not any_material and outcome not in {"record_and_correct", "stopped_escalated"}:
        errors.append(
            "decision/outcome: a non-material discrepancy is recorded and corrected "
            f"(record_and_correct) or stopped as a precaution (stopped_escalated), not {outcome}"
        )
    if outcome == "record_and_correct" and not discrepancies:
        errors.append("decision/outcome: record_and_correct with nothing to correct")

    if outcome == "proceed_with_verified":
        if decision.get("intent_unambiguous") is not True:
            errors.append(
                "decision/intent_unambiguous: proceed_with_verified requires true; otherwise fail closed"
            )
        for field in ("authority", "deviation"):
            if _blank(decision.get(field)):
                errors.append(f"decision/{field}: required for proceed_with_verified")
        covered = {_norm(item) for item in decision.get("covers") or []}
        for check in material:
            if _norm(check.get("item")) not in covered:
                errors.append(
                    f"decision/covers: material discrepancy {check.get('item')!r} is not covered; "
                    "each one needs its own resolution, or the operation stops"
                )
    if outcome == "stopped_escalated" and _blank(decision.get("escalated_to")):
        errors.append("decision/escalated_to: required for stopped_escalated")
    if outcome == "record_and_correct" and _blank(decision.get("correction")):
        errors.append("decision/correction: required for record_and_correct")

    if host.get("classification") == "unknown" and outcome != "stopped_escalated":
        errors.append(
            "host/classification: the host's role was not established, so the only valid "
            "outcome is stopped_escalated"
        )

    verified_at = parse_timestamp(record.get("verified_at"))
    if verified_at is None:
        errors.append(
            "verified_at: not an RFC 3339 date-time with an offset: "
            f"{record.get('verified_at')!r}"
        )
    else:
        current = now or datetime.now(timezone.utc)
        if verified_at > current + CLOCK_SKEW:
            errors.append(
                f"verified_at: {record['verified_at']} is in the future "
                f"(clock-skew tolerance {CLOCK_SKEW})"
            )
        if max_age is not None and current - verified_at > max_age:
            errors.append(
                f"verified_at: {record['verified_at']} is older than --max-age {max_age}; "
                "it remains audit history but does not verify a current operation"
            )

    if any(contains_secret(text) for text in _strings(record)):
        errors.append("record appears to contain a secret (a credential value); name where it lives instead")

    return errors


def validate_record(
    record: Any,
    schema_path: Path | None = None,
    now: datetime | None = None,
    max_age: timedelta | None = None,
) -> list[str]:
    validator = jsonschema.Draft202012Validator(load_schema(schema_path), format_checker=FORMAT_CHECKER)
    structural = [
        f"{'/'.join(str(p) for p in error.path) or '<root>'}: {error.message}"
        for error in sorted(validator.iter_errors(record), key=lambda e: list(e.path))
    ]
    if structural or not isinstance(record, dict):
        return structural
    return semantic_errors(record, now=now, max_age=max_age)


# --- discovery and packets -------------------------------------------------


def discover(root: Path, directory: Path) -> list[Path]:
    base = directory if directory.is_absolute() else root / directory
    return sorted(base.rglob("*.json")) if base.is_dir() else []


def load_packet(path: Path) -> dict[str, Any]:
    """A completion packet: YAML/JSON, or the first fenced YAML block in Markdown
    that carries an `infrastructure_discovery` key."""
    import yaml  # PyYAML ships with the verification workflow

    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        for block in re.findall(r"```ya?ml\n(.*?)```", text, re.DOTALL):
            data = yaml.safe_load(block)
            if isinstance(data, dict) and "infrastructure_discovery" in data:
                return data
        return {}
    data = yaml.safe_load(text)
    return data if isinstance(data, dict) else {}


def packet_records(packet: dict[str, Any], root: Path) -> tuple[list[Path], list[str], bool]:
    """Record paths a packet references, errors, and whether it requires a record."""
    block = packet.get("infrastructure_discovery") or {}
    if not isinstance(block, dict) or not block.get("touches_infrastructure"):
        return [], [], False
    records = block.get("records") or []
    errors = [] if records else ["touches_infrastructure is true but no records are listed"]
    paths = []
    for ref in records:
        path = root / str(ref)
        if path.is_file():
            paths.append(path)
        else:
            errors.append(f"referenced record {ref} does not exist")
    return paths, errors, True


def parse_age(text: str) -> timedelta:
    """`<n>d`, `<n>h` or `<n>m`."""
    match = re.fullmatch(r"(\d+)([dhm])", text.strip())
    if not match:
        raise argparse.ArgumentTypeError("use <n>d, <n>h or <n>m, for example 1d")
    unit = {"d": "days", "h": "hours", "m": "minutes"}[match.group(2)]
    return timedelta(**{unit: int(match.group(1))})


def run(
    paths: list[Path],
    task: str | None,
    require: bool,
    now: datetime | None = None,
    max_age: timedelta | None = None,
    extra_errors: list[str] | None = None,
    bound: set[Path] | None = None,
) -> dict[str, Any]:
    """Validate records. `bound` paths were named explicitly (argument or packet):
    with --task, a bound record for another task is a binding error, not a skip."""
    bound = bound or set()
    results: list[dict[str, Any]] = []
    loaded: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for path in dict.fromkeys(paths):
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            results.append({"path": str(path), "task": None, "valid": False,
                            "errors": [f"cannot read record: {exc}"]})
            continue
        record_task = record.get("task") if isinstance(record, dict) else None
        if task is not None and str(record_task) != task:
            if path in bound:
                results.append({"path": str(path), "task": record_task, "valid": False,
                                "errors": [f"task binding: record is for task {record_task!r}, not {task!r}"]})
            else:
                LOG.debug("skipping %s: task %r is not %r", path, record_task, task)
            continue
        errors = validate_record(record, now=now, max_age=max_age)
        result = {"path": str(path), "task": record_task, "valid": not errors, "errors": errors}
        results.append(result)
        if isinstance(record, dict):
            loaded.append((record, result))

    # One record per task and host: a second is a duplicate or a conflict.
    groups: dict[tuple[str, str], list[tuple[dict[str, Any], dict[str, Any]]]] = {}
    for record, result in loaded:
        key = (str(record.get("task")), _norm((record.get("host") or {}).get("name")) or "")
        groups.setdefault(key, []).append((record, result))
    for (group_task, group_host), members in groups.items():
        if len(members) < 2:
            continue
        kind = "duplicate" if all(m[0] == members[0][0] for m in members) else "conflicting"
        others = ", ".join(m[1]["path"] for m in members)
        for _, result in members:
            result["errors"].append(f"{kind} records for task {group_task} host {group_host}: {others}")
            result["valid"] = False

    for result in results:
        for error in result["errors"]:
            LOG.error("%s: %s", result["path"], error)
        if result["valid"]:
            LOG.debug("%s: valid", result["path"])
    for error in extra_errors or []:
        LOG.error("%s", error)

    valid = [r for r in results if r["valid"]]
    missing = require and not valid
    if missing:
        LOG.error("no valid infrastructure discovery record%s; the operation must not proceed",
                  f" for task {task}" if task else "")
    ok = all(r["valid"] for r in results) and not missing and not extra_errors
    return {"ok": ok, "checked": len(results), "valid": len(valid), "required": require,
            "task": task, "errors": list(extra_errors or []), "records": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("paths", nargs="*", type=Path, help="record files (default: discover)")
    parser.add_argument("--root", type=Path, default=Path("."), help="repository root")
    parser.add_argument("--dir", type=Path, default=DEFAULT_DIR,
                        help=f"record directory under --root, searched recursively (default {DEFAULT_DIR})")
    parser.add_argument("--task", help="task id the records must belong to")
    parser.add_argument("--require", action="store_true",
                        help="fail unless a valid record exists for --task (mandatory with --require)")
    parser.add_argument("--packet", type=Path, action="append", default=[],
                        help="completion packet whose infrastructure_discovery.records are checked")
    parser.add_argument("--max-age", type=parse_age, default=None, metavar="AGE",
                        help="reject records verified longer ago than AGE (for example 1d); default none")
    parser.add_argument("--json", action="store_true", help="machine-readable result on stdout")
    parser.add_argument("-v", "--verbose", action="store_true", help="debug logging")
    args = parser.parse_args(argv)

    level = "DEBUG" if args.verbose else os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=getattr(logging, level, logging.INFO),
                        format="%(levelname)s %(name)s: %(message)s", stream=sys.stderr)

    require = args.require
    bound = {p for p in args.paths}
    paths = list(args.paths) or discover(args.root, args.dir)
    extra_errors: list[str] = []
    for packet_path in args.packet:
        try:
            packet = load_packet(packet_path)
        except (OSError, ValueError) as exc:
            extra_errors.append(f"packet {packet_path}: cannot read: {exc}")
            continue
        found, errors, needed = packet_records(packet, args.root)
        paths.extend(found)
        bound.update(found)
        extra_errors.extend(f"packet {packet_path}: {e}" for e in errors)
        require = require or needed
    if require and args.task is None:
        parser.error("a required record needs --task <id>: records are bound to one task")

    LOG.debug("records to check: %s", [str(p) for p in paths])
    result = run(paths, args.task, require, max_age=args.max_age,
                 extra_errors=extra_errors, bound=bound)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"infrastructure discovery: {result['checked']} checked, {result['valid']} valid"
              f"{' (required)' if require else ''}: {'OK' if result['ok'] else 'FAIL'}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
