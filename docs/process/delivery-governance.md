<!-- Managed by harkers/repo-standards at revision 9a0c7824. Use .repo-standards.yml overrides instead of editing this header away. -->

# Delivery governance: autonomous merge authority

Status: in force (owner decision "Standing Autonomous Delivery Authority", 2026-11-26). Amended 2026-11-27 (owner
directive "Simplify Governance and Restore Autonomous Delivery": development is not execution). A change to this
document takes effect when the owner merges the repo-standards PR that carries it.

This is the only statement of who may approve or merge. It supersedes any per-repository, per-agent or per-tool
wording. Other instruction files (agent definitions, `AGENTS.md`, `CLAUDE.md`, Codex and OpenCode instructions,
reviewer and coordinator prompts) point here and do not restate approval requirements; where one of them disagrees
with this document, this document wins and the other file is corrected.

## Principle

If the work is authorised, independently reviewed, tested and every applicable gate passes, the coordinator
merges it and moves on. Human intervention is exception-based.

Developing software is not the same as executing a privileged production operation. Writing, testing, reviewing and
merging code that supports a privileged operation (migration code, schema definitions, rollback tooling, deployment
tooling, their tests and documentation) is routine. Running that operation against production (a deployment, a
migration, a backfill, a rollback) is governed by its own execution authorisation, and merging the code never
grants it.

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
changes, database migration code and schema definitions, rollback and deployment tooling, documentation, automated
and regression tests, observability, dependency maintenance within policy,
branches and worktrees, forge issues, independent reviews, CI, non-production integration testing, merging
qualified routine PRs, and progression to the next task in an approved plan.

## Exception classes (owner action required)

- material deviation from an approved architecture, or an unresolved architectural decision;
- new or materially increased security risk; authentication or authorisation changes; trust-boundary changes;
- executing a production deployment outside an existing owner-authorised release policy that covers that exact operation;
- executing a destructive or irreversible operation, or a database migration against production, that the owner or an
  owner-authorised release policy naming that kind of operation has not already authorised (the code for either is
  routine: see Principle);
- activating an external provider or integration in production;
- credential rotation or revocation; release-signing credential changes;
- financial commitments;
- a technical blocker that cannot be resolved within existing authority;
- changes to this policy, to the PR gate's identity rules, or to branch protection.

An approval already given for a defined activity is not requested again unless scope, risk or circumstances change.
Owner-only classes are enforced by path, natively: files that are themselves a security, permission or assurance control
(the policy and its shipped copy, the checker, workflows, verification rules, the assurance configuration, scanner
configuration, and the tools and schemas the required checks run, release records and the owner's acceptance records, signing and install scripts) are Forgejo
`protected_file_patterns`, so the coordinator's merge of a PR touching them is refused and only the owner can merge it (with
`force_merge`). Release records stay protected because the readiness summary put to the owner is derived from them. Source code
is not protected because of what it will later do in production: migration code, schema definitions, rollback and deploy
tooling are routine. Classes that
no path can express (architecture deviation, new security risk without a security path, credentials, spending, production
execution, unresolved decisions) are judged by the coordinator **at planning time** and escalated before the PR is opened.
The list of protected paths lives in `docs/governance/protection/<repo>.json` and is applied and verified by
`tools/governance_apply.py` and `tools/governance_verify.py`.

Every other eligible repository is enrolled from `docs/governance/protection/fleet.json` (owner-only: profiles,
exclusions, protected paths) and `docs/governance/enrolment/repos.json` (routine: which profile a repository has), by
`tools/governance_fleet.py` (dry run by default, idempotent, reads each repository back). It has two profiles:

- `coordinator`: the rules above in full. Given only where every required CI context has succeeded on a recently
  merged PR (the tool checks, and enrols the repository as `owner-merge` otherwise) and a merge does not itself
  deploy. A repository with this profile is in the same position as one whose `merge-policy.json` says `native`: the
  coordinator merges a qualified routine PR without asking. Where the repository has no gate script, the coordinator
  confirms that the approving review's commit is the PR head and merges with `head_commit_id` pinned to it.
- `owner-merge`: agents propose and review, the owner merges. The default, and the profile for infrastructure,
  the governance sources, repositories whose merge triggers a deployment, and repositories with no CI history. Moving
  a repository to `coordinator` is a one-line change to the routine file, reviewed and merged like any routine PR.

Archived repositories, pull mirrors, empty repositories and the repositories the file excludes by name (restricted
stores, client material, test fixtures) are not enrolled. No service identity is a repository or site administrator.
A standards sync carries content that was already reviewed and merged in repo-standards, so its PR in each repository
is not read again; it is proved identical instead. The sync refuses to push from anything but a clean checkout of
repo-standards `origin/main`. `forgejo_sync.py --attest`, run with the reviewer identity from its own clean
`origin/main`, renders the managed files itself and approves the PR's exact head only when the whole tree is the one it
rendered: any extra or altered file fails, and a later push makes the approval stale. The sync then merges only a head
whose tree it rendered and, in every repository the reviewer identity can read, only with that live attestation.
Managed files are protected paths in a `coordinator` repository, so the owner merges that PR: the sync sends the
owner's `force_merge` only when the forge's one remaining refusal is the protected-files rule, which it reports after
status checks and approvals are satisfied.

What CI a sync PR gets: where the verify check is required, the sync branch has a name the workflow never skips, so
verify and every other required check run and must pass. Elsewhere the verify workflow skips an owner-opened,
owner-pushed sync branch (a skipped check counts as passed on this forge, so a push by anyone else is not skipped),
and that repository's sync PR merges on the attestation and whatever checks its rule requires. In a repository the
reviewer identity is not a collaborator of (excluded, or not yet enrolled), the tree check and the forge's own rule are
the only gates.

repo-standards itself is a `coordinator` repository. Its routine changes (documentation, tests, ordinary standards and
the routine enrolment file `docs/governance/enrolment/repos.json`) merge through the coordinator after the reviewer's
approval of the exact head, the verifier's approval and green CI. Everything that enforces security or assurance, or
that tells agents how they are governed, is an owner-only path there: workflows, hooks, policy, the verifier, its
toolchain and its deployment, the sync and its templates, tools, schemas, profiles, the enforced-rule coverage
baseline, agent definitions and contracts, the governance, review, security, evidence and runtime-contract standards,
ADRs and `docs/governance/protection/**`. The routine file can give a repository a profile and
name its CI contexts, nothing else; it cannot name a repository the protected file lists or excludes, and a
`coordinator` entry takes effect only when the tool finds that repository's required CI green, and it can add required
checks to a repository's rule but never remove one. Reviews of repo-standards PRs are recorded on the forge by the
reviewer identity, on the exact head: PR 124 merged at a commit the reviewer had rejected because that review was not
yet a forge rule. For a routine PR it now is one. A PR that touches an owner-only path can be merged only with the
owner's `force_merge`, which sets every check aside at once, so the forge itself cannot refuse a rejected head there:
the owner merges such a PR with `tools/governance_owner_merge.py`, which tries a plain merge of the pinned head first
and sends `force_merge` only when the forge's sole remaining refusal is the protected-files rule.

Known limit, not closed by this document: on this forge any identity with write access to a repository can post a
commit status through the API, so an implementer could report a required check as passed without it having run. The
independent reviewer and the coordinator's gate are what stand against that today (MediaFlow's gate rejects a required
context posted by a login). A `coordinator` rule ignores stale approvals, so an approval never counts for a head the
reviewer did not see.

Reviewers and coordinators apply the conditions and exception classes as written and do not add a gate this document
does not list. Migration, schema, rollback and deploy source is not owner-only because of its subject matter. The
exception classes above still apply to a change on any path, protected or not: a reviewer who sees one records
request-changes, naming the class, until the owner's decision is linked from the PR. Migration, schema, rollback or
deploy source is never such a class by itself.

Because migration code merges as routine work, the execution authorisation carries the control: the evidence put to
the owner for a production release names every pending migration, and any other change that alters or deletes stored
data at start-up or on deploy without a user action (schema version before and after, the migration and rollback
scripts, and the rehearsal evidence), before anything is executed. A service that migrates at start-up executes every
merged migration on deploy, so a deploy that carries a pending migration is a migration execution: a release policy
authorises it only if it names migrations explicitly; otherwise the owner approves that release on evidence that
lists them.

## Mechanical enforcement

Forgejo's native protection is the enforcing layer; `pr-gate.py` is a read-only readiness checker (verification evidence, derived
CI, head pin, advisory owner-only paths). Verified empirically with the service identities: see
`docs/governance/proposals/forgejo-identities-and-protection.md` for the results, including what did not pass.

| Rule | Enforced by | Status |
|---|---|---|
| Approval is a review by a whitelisted reviewer who is not the author; stale reviews dismissed; request-changes blocks | Forgejo | enforced when protection is on |
| Only the coordinator (or owner) merges; implementers cannot push the default branch or merge | Forgejo whitelists | enforced when protection is on |
| Required CI | Forgejo status contexts and the checker | enforced when protection is on |
| Owner-only classes (policy, gate, workflows, verification rules, assurance configuration and tools, release and owner acceptance records, signing) | `protected_file_patterns`; push disabled for everyone; owner merges with `force_merge` | enforced when protection is on |
| Verification evidence for the PR's risk class | the checker (`Verification:` block) | enforced for merges that go through the checker; a direct merge-API call by the coordinator bypasses it (the native rules still apply) |
| The coordinator cannot change its own policy or checker | those files are protected paths | enforced when protection is on |
| Deploy tooling, migration code and schema definitions are routine; executing a deployment or migration against production, secrets and trust boundaries are not | no path protection for the code; execution needs its own authorisation (owner approval for that release, or an owner-authorised release policy covering that exact operation) | execution judged by the owner |
| Exception classes that no path expresses (authentication, trust boundary, architecture, spending) | the reviewer's request-changes (blocks natively) and the coordinator's reading of condition 8 | advisory: depends on the reviewer and coordinator noticing |
| Release evidence names pending migrations before execution | the deploy plan and the release request | advisory until the readiness tooling lists them |
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
