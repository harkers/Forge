<!-- Managed by harkers/repo-standards at revision 9a0c7824. Use .repo-standards.yml overrides instead of editing this header away. -->

# Infrastructure Discovery Standard

Owner and coordinator decision, 2026-11-26: **mandatory for every Software Factory project.** This
file is the single canonical text; `AGENTS.md`, `CLAUDE.md`, the agent role contracts, the global
Claude instructions and the Harker Knowledge vault note **Infrastructure discovery standard** point
here rather than copying it. It extends the knowledge standard (`docs/process/knowledge.md`), which
makes the vault authoritative, and the engineering standard (`docs/process/engineering.md`), which
governs deploys and host moves.

## Rule

Before executing a task that touches a host, a filesystem path or a deployed service, an agent
MUST verify the target against the Harker Knowledge vault and against the live system (read-only),
and record what it found in an infrastructure discovery record. A host, path, address or version
named in a brief, issue, plan or prior conversation is a claim, not a fact, until it has been
checked.

## Before work

1. **Read the documentation.** Read the vault note for the host or component
   (`02-Infrastructure/`, `Hosts/` for scan-derived entries, and the note whose `repo` property
   names the repository). Treat `verified: no` as unchecked.
2. **Check the live system, read-only.** Confirm the host is reachable, plays the expected role
   (production, development or rollback), and that the service identity, state, version, schema
   and data path match. Discovery commands change nothing: no restarts, writes or configuration
   edits.
3. **Record what was found** as an infrastructure discovery record (below): each claimed value
   beside the observed value, where each came from, and the decision taken. Classify claims with
   the evidence classes in `docs/process/behavioral-policy.md`.

## Material and non-material discrepancies

A discrepancy is **material** when it concerns any of:

- the production host;
- a database;
- a deployment target;
- service identity;
- schema version;
- credential scope;
- anything else that could cause harm or invalidate evidence.

A discrepancy is **non-material** when it is an outdated description, a historical reference or a
minor documentation inconsistency that cannot change what the operation acts on.

## Fail closed

Operational agents MUST fail closed on the affected operation when a material discrepancy between
documentation and live infrastructure cannot be resolved: stop that operation, record both values
and their sources, and escalate to the coordinator or owner. Do not proceed on either value. Only
the affected operation stops; unrelated work in the same session continues.

Never silently substitute a different production target. Before acting on a value other than the
one the brief named, establish its authority (a vault note, decision record or deploy log that says
it is the intended target) and record the decision. Proceed on the verified value only when the
intent of the task is unambiguous and the verified value is clearly the intended target, and state
the deviation in the report.

A non-material discrepancy does not block work: record it and correct it through the normal
workflow (a vault note update, an issue or a pull request).

## Infrastructure discovery record

Each discovery is recorded as a JSON document conforming to
`schemas/infrastructure-discovery-record.schema.json`, one per task and host, stored under
`evidence/infrastructure-discovery/` (subdirectories allowed) or listed in the completion packet's
`infrastructure_discovery.records`. A record holds: the task, the host and its classification
(`production`, `development`, `rollback`, or `unknown` when the role could not be established), each
checked item with its claimed value, observed value and their sources, whether each discrepancy is
material, `verified_at`, the overall `material` flag and the decision (`proceed_as_documented`,
`proceed_with_verified`, `stopped_escalated` or `record_and_correct`). Records name where a
credential lives (a Keychain item, an Infisical secret name), never its value.

`verified_at` is an RFC 3339 date-time with an explicit offset (`Z` or `+hh:mm`). Date-only and
offset-less values are invalid. A value more than five minutes (the clock-skew tolerance) ahead of
the validating machine's clock is invalid. There is no default expiry: a historical record stays
valid as audit history, and a caller that needs current evidence passes `--max-age` (for example
`--max-age 1d`), which rejects older records.

A submitted record committed to the repository MUST satisfy `tools/validate_discovery.py`, which
checks the schema and these rules:

- comparison of claimed and observed values ignores case and surrounding whitespace; mandatory text
  fields cannot be blank;
- a discrepancy in a material category (production host, database, deployment target, service
  identity, schema version, credential scope) cannot be marked non-material, and an agreeing value
  cannot be marked material;
- a claimed value that could not be observed is material: what was not verified may be wrong;
- a check with nothing claimed and nothing observed verified nothing, and only a stop is valid;
- work may proceed only when a target (production host or deployment target) was observed and it is
  the record's host;
- a material discrepancy ends in `stopped_escalated` (naming who it went to) or
  `proceed_with_verified`, which needs `intent_unambiguous: true`, the authority, the deviation, and
  every material discrepancy listed in `covers`; one decision cannot silently cover a second;
- a non-material discrepancy ends in `record_and_correct` (naming the correction) or, as a
  precaution, `stopped_escalated`; `record_and_correct` and `proceed_with_verified` need a
  discrepancy, and `proceed_as_documented` needs none;
- a host whose classification is `unknown` can only be `stopped_escalated`;
- one record per task and host: a duplicate or conflicting second record invalidates both;
- with `--task`, a record named explicitly (argument or packet) for another task is a binding
  error; `--require` needs `--task`.

The validator also scans records for credential values (private keys, JWT and bearer tokens,
GitHub and AWS keys, age secret keys, credentials in URLs, password assignments).
This scan is defence in depth, not leak prevention, and it is not comprehensive: gitleaks
(RS-SEC-001) remains the mandatory secret control.

## Status: what is and is not enforced (Phase 1)

| Level | What exists now |
|---|---|
| Documented requirement | Everything in this standard, shipped to every repository as `docs/process/infrastructure-discovery.md` and pointed to from `AGENTS.md`, `CLAUDE.md` and the operational role contracts. |
| Validation of submitted records | The managed verification workflow runs `tools/validate_discovery.py --root .` on every pull request and fails on any invalid committed record. A repository with no records passes. |
| Mandatory evidence gate | **Not yet.** Nothing forces a task that touches infrastructure to produce a record. `--require --task <id>` exists for that purpose, and the completion packet carries an `infrastructure_discovery` block, but no gate runs them automatically (Phase 2). |
| Runtime enforcement | **None.** Nothing stops an agent from acting on a host before discovery. Compliance at the moment of action rests on the agent following this standard. |

Not done in Phase 1: an evidence gate that requires a record for host-touching tasks, machine
validation of completion packets, runtime prevention, and WorkHub integration (task start time,
applicability and task identity supplied by the control plane rather than by the agent).

Known governance limitation, for the WorkHub assurance programme: the repository merge pre-flight
(`tools/merge_preflight.py`) accepts overlapping work once the pull request description contains
the text `Overlap-reviewed: #N`. It trusts the presence of that string; it does not verify who wrote
it or that a review took place.

## The inventory records, per host

The vault inventory (one note per machine or component, with `verified` and `sources` properties)
holds, for each host:

- hostname and purpose;
- hardware and operating system;
- network address and SSH connectivity (how to reach it and which key, never the key itself);
- hosted services;
- classification: production, development or rollback;
- deployment locations (install paths and data directories);
- last verification date;
- known limitations.

## After work

After a substantive, verified change (an address, a deployment, a classification, a status), update
the affected vault note in place as `docs/process/knowledge.md` describes: read it first, change
only what is needed, bump `updated`, set `verified` and `sources`. Never write secrets into a note
or a discovery record.

## Worked example (2026-11-26)

A Task 11 brief said to snapshot the production database from athena. The live check found athena
refusing SSH, and the vault recorded that the production server had moved to Zeus VM 221
(`192.168.10.171`) on 2026-11-06. The discrepancy was material (production host). Its authority was
established from the vault note and the move record; the intent (snapshot production) was
unambiguous and the verified value was clearly the target, so the snapshot was taken from VM 221
and the deviation recorded. athena's database is a stale rollback. The documentation was corrected
in [MediaFlow PR 269](https://forge.harker.systems/vulcan/mediaflow/pulls/269); the wider work is
tracked in [zeus-infra issue 54](https://forge.harker.systems/vulcan/zeus-infra/issues/54). The
record is reproduced as the passing fixture
`schemas/fixtures/infrastructure-discovery.pass.json` in repo-standards.

## Review

Work that touched a host, path or deployed service without a valid discovery record, or that
proceeded past an unresolved material discrepancy, is a review finding of at least `Important`.
