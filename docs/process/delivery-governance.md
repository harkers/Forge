<!-- Managed by harkers/repo-standards at revision 1ccc10ee. Use .repo-standards.yml overrides instead of editing this header away. -->

# Delivery governance: autonomous merge authority

Status: proposed amendment. Takes effect when the owner approves the repo-standards PR that carries it.
Origin: owner decision "Standing Autonomous Delivery Authority" (2026-11-26). It supersedes any per-repository,
per-agent or per-tool wording about who may approve a routine merge. There is one policy: this one.

## Principle

If the work is authorised, independently reviewed, tested and every applicable gate passes, the coordinator
merges it and moves on. Human intervention is exception-based.

## Roles (kept separate)

| Role | Does | Must not |
|---|---|---|
| Implementer | writes the change, opens the PR, records evidence | approve or merge its own work; post approval evidence |
| Independent reviewer | reviews the final effective diff at one exact commit, records a verdict | have authored the change; review a different commit than the one merged |
| Coordinator | runs the PR gate and merges when the conditions below hold; progresses to the next task | merge outside the gate; widen its own remit; impersonate the owner or a reviewer |
| Owner | decides the exception classes below; approves changes to this policy | be asked again for something already authorised |

Each role is a distinct identity on the forge. A single shared account cannot separate them: the forge refuses an
author's own approval, and an approval written as text by the token holder proves nothing.

Four forge identities, least privilege: the owner (`vulcan`, owner-held token, never given to an agent), an
implementation identity (`sf-agent`: Write, confined by protection; no approve, no merge), an independent reviewer identity
(`sf-reviewer`: reviews), and a coordinator identity (`sf-coordinator`: merge whitelist only, no approve, no admin). Design, token scopes and branch
protection values: `docs/governance/proposals/forgejo-identities-and-protection.md`.

## Automatic merge conditions (routine class)

A PR merges without further human approval when all hold:

1. It sits inside an approved plan or design (issue or plan linked).
2. Its acceptance criteria are met and its `Verification:` block carries evidence for every level its risk class requires.
3. Every required CI context is `success` on the exact head commit.
4. An independent reviewer's approving review is recorded against that same head commit (a new commit makes it stale).
5. Material findings are resolved. Non-blocking findings are addressed, or recorded as follow-up issues linked from the PR.
6. Security scans and repository-standards checks pass.
7. No reviewer has an unresolved request for changes.
8. No exception class below applies.

An independent approval with only non-blocking nits satisfies condition 4 once condition 5 is met.

## Covered activities

Routine feature work, bug fixes, refactoring, performance work, UI and UX implementation, backward-compatible API
changes, documentation, automated and regression tests, observability, dependency maintenance within policy,
branches and worktrees, forge issues, independent reviews, CI, non-production integration testing, merging
qualified routine PRs, and progression to the next task in an approved plan.

## Exception classes (owner action required)

- material deviation from an approved architecture, or an unresolved architectural decision;
- new or materially increased security risk; authentication or authorisation changes; trust-boundary changes;
- production deployment outside an existing authorised release policy;
- destructive or irreversible operations; production database migrations not already authorised;
- credential rotation or revocation; release-signing credential changes;
- financial commitments;
- a technical blocker that cannot be resolved within existing authority;
- changes to this policy, to the PR gate's identity rules, or to branch protection.

An approval already given for a defined activity is not requested again unless scope, risk or circumstances change.
Owner-only classes are enforced by path, natively: files that carry owner-only risk (the policy and the checker, workflows,
verification rules, migrations, the schema, release records, signing and install scripts) are Forgejo `protected_file_patterns`,
so the coordinator's merge of a PR touching them is refused and only the owner can merge it (with `force_merge`). Classes that
no path can express (architecture deviation, new security risk without a security path, credentials, spending, production
execution, unresolved decisions) are judged by the coordinator **at planning time** and escalated before the PR is opened.
The list of protected paths lives in `docs/governance/protection/<repo>.json` and is applied and verified by
`tools/governance_apply.py` and `tools/governance_verify.py`.

## Mechanical enforcement

Forgejo's native protection is the enforcing layer; `pr-gate.py` is a read-only readiness checker (verification evidence, derived
CI, head pin, advisory owner-only paths). Verified empirically with the service identities: see
`docs/governance/proposals/forgejo-identities-and-protection.md` for the results, including what did not pass.

| Rule | Enforced by | Status |
|---|---|---|
| Approval is a review by a whitelisted reviewer who is not the author; stale reviews dismissed; request-changes blocks | Forgejo | enforced when protection is on |
| Only the coordinator (or owner) merges; implementers cannot push the default branch or merge | Forgejo whitelists | enforced when protection is on |
| Required CI | Forgejo status contexts and the checker | enforced when protection is on |
| Owner-only classes (policy, gate, workflows, migrations, schema, releases, signing) | `protected_file_patterns`; push disabled for everyone; owner merges with `force_merge` | enforced when protection is on |
| Verification evidence for the PR's risk class | the checker (`Verification:` block) | enforced for merges that go through the checker; a direct merge-API call by the coordinator bypasses it (the native rules still apply) |
| The coordinator cannot change its own policy or checker | those files are protected paths | enforced when protection is on |
| Deploy tooling is routine; production execution, migrations, secrets, trust boundaries are not | path patterns: tooling unprotected, the rest protected; execution of a deploy is an owner action | enforced for paths; execution judged by the owner |
| Material findings resolved; non-blocking nits recorded as issues | independent reviewer's verdict | advisory |
| Reporting rules | this document | advisory |

`shield / android` is required only where its workflow triggers for the PR's paths; the checker derives it and fails closed
when the changed files cannot be read. Tests are never weakened to obtain a pass.

## Audit record (WorkHub)

For every merge WorkHub records: implementer identity; independent reviewer identity; applicable policy and version;
the exact reviewed commit; CI evidence per context; acceptance criteria and their status; the merge decision and
the merging identity; outstanding non-blocking findings and their follow-up issues; the timestamped trail.

## Reporting

Report outcomes, not activity: deliverables, merged PRs, test and assurance results, milestone progress, genuine
blockers, material risks, and decisions that need a human. Do not repeat an unchanged waiting state. Do not end a
report by asking whether to continue: continuation is the default.

## What this replaces

See the conflict register in the PR that introduced this file. In short: the "owner approves each merge" and
"agents must not infer merge permission from a passing review" wording is replaced by the conditions above; the
2026-11-22 decision-coordinator grant (MediaFlow merges) is subsumed and generalised: it stays in force for a repository until that repository's merge policy is in `native` mode, and ends there, so that two approval models never run at once; per-agent instruction files
point here instead of restating approval rules.
