# Repository Audit And Repair

Use this reference for an existing workflow repository, project workspace, template system, or chaotic file-based project.

## Contents

1. Audit order
2. Health dimensions
3. Repair contract
4. Baseline and rollback
5. Migration and validation
6. Completion report

## Audit Order

Inspect low-risk governance surfaces before deep business content:

1. Repository boundaries and nested repositories.
2. Size profile, file count, binary-heavy areas, version-control status, branches, commits, tags, and remotes.
3. Top-level navigation, control pages, current-task records, and manifests.
4. Lifecycle, Gate definitions, and status vocabulary.
5. Project template, formal project placement, and project registry.
6. Active versions, release evidence, and human approval.
7. Archive, retrospective, and knowledge backflow.
8. AI/runtime activation: actual working directory, instruction scope, packaged versus installed capabilities, and pre-write enforcement.
9. Automation, validation, packaging, and distribution hygiene.
10. Deep project/client content only when needed and authorized.

Do not mutate files during an audit unless the user also requested a fix.

Before recommending a redesign, identify the current digitization profile and adoption evidence, then recover at least one evidence-backed AS-IS workflow slice. Distinguish a broken digital representation from a business method that was never decided. The former may be repaired here; the latter must return to its decision owner or domain specialist.

## Health Dimensions

| Dimension | Healthy evidence | Common failure |
|---|---|---|
| Work fidelity | Online objects, states, roles, and artifacts trace to accepted work or observed practice | The repository contains an elegant invented process that the team does not actually use |
| Digitization profile | Representation, execution surface, governance, AI coverage, and adoption evidence are explicit; working dimensions are preserved | Every audit becomes a complete rebuild or premature AI automation |
| Boundary | System, template, sandbox, and formal projects are distinguishable | Formal projects accumulate inside the mother system |
| Truth source | Current stage, task, owner, decisions, and active version are visible | Chat or memory is the only current state |
| Version safety | Baseline, history, tags/snapshots, migration, rollback | Large uncommitted history or zero commits |
| State semantics | Gate, artifact, approval requirement/result/source, and action states are separate | `pass-as-candidate`, `released` used as Gate result |
| Gate integrity | Stable IDs and canonical meanings | Project-specific checks reuse system Gate IDs |
| Template governance | One runtime template source with version manifest | Duplicate templates drift independently |
| Project registry | Formal projects and their current snapshots are registered | Repositories exist but the mother system cannot enumerate them |
| Release traceability | Version, evidence, checksum, approval, and freeze rule exist | A file is called final without proof |
| Backflow | Provenance, abstraction, destination, and index are complete | Empty retrospective or copied project content |
| Automation | Validation and scaffold smoke tests catch drift | Quality depends only on manual memory |
| Runtime activation | A real task can discover its entrypoint, route to an installed capability, fail preflight, and validate after writing | Rules exist only in a sibling folder; a Skill is documented but not installed; Gates are updated after work |
| Human/AI authority | AI nodes declare allowed actions, evidence, failure behavior, and human decisions | Advice, approval, or unresolved policy is silently converted into autonomous execution |
| Adoption | A real workflow slice has run with named users and recorded friction | Synthetic fixtures are reported as operational adoption |
| Distribution | Package excludes VCS and machine junk, includes a manifest | `.git`, caches, or system files leak into delivery |

## Repair Contract

Before writing, record:

- Objective.
- Existing work and semantics that must be preserved.
- Current and target digitization profile plus adoption evidence.
- Unresolved business rules that this repair may not invent.
- In-scope repositories/workspaces.
- Allowed files or modules.
- Out-of-scope project facts or content.
- Whether Gate, release, approval requirement, or approval-result states may change.
- Completion checks.
- Rollback point.
- Actual task working directory, target paths, applicable instruction entrypoints, and runtime capability destination when AI agents maintain the system.
- Specialist handoffs required for domain policy, custom software architecture, or Skill packaging.

For multi-step repair, add a current-task file containing known facts, assumptions, allowed changes, completion criteria, and next action. Add an AI collaboration entry such as `AGENTS.md` only when the system is maintained through file-based AI work.

Do not assume an `AGENTS.md` inside the mother system governs sibling project repositories. Resolve the instruction chain from the real task working directory to each mutation target. Do not assume a `SKILL.md` or design note is callable merely because it exists in the repository; verify packaging, installation/discovery, and invocation separately.

## Baseline And Rollback

Use the strongest available recoverable baseline:

### Git-backed filesystem

1. Inspect dirty and untracked files without discarding them.
2. Preserve existing user work.
3. Create a baseline commit and descriptive tag before structural repair when authorized.
4. Record the commit/tag in the migration file.
5. Keep each formal project and the mother system independently recoverable.

### Non-Git filesystem

Create a dated archive or immutable copy outside the repair target, record its checksum, and document how to restore it.

For a large workspace, use a scope-aligned baseline only when the repair contract names every mutable control path and explicitly excludes untouched project/client content. Record included paths, exclusions, checksum, timestamp, and restore rule. Use `scripts/create_scoped_baseline.py` when appropriate. Do not broaden later edits beyond the baseline scope.

### SaaS/toolspace

Use export, snapshot, version history, duplication, or another platform-native rollback method. Record the snapshot identity and time.

Do not move or delete “obsolete” files merely because their names look old. Resolve the active version first.

## Migration And Validation

Write a migration record that includes:

- From/to system and template versions.
- Repositories or workspaces affected.
- Semantic changes to states, Gate IDs, templates, and placement.
- Files changed and content explicitly excluded.
- Rollback point.
- Validation commands or manual evidence.
- Remaining warnings and human decisions.
- Runtime activation changes: entrypoint scope, installed capability source, enforcement level, and realistic forward-test evidence.

Apply changes in coherent groups:

1. AS-IS/TO-BE mapping and transformation boundary.
2. Contract and version source.
3. Navigation, project registry, runtime templates, and manifests.
4. AI runtime activation only when the underlying digital operating layer is stable.
5. Existing project migrations.
6. Backflow, indexes, validation, and packaging.

Validate after each risky group. For file-based systems, check syntax, required fields, status vocabulary, Gate identity, registry coverage, version references, backflow completeness, project scaffold creation, and package contents.

For AI-maintained systems, also test:

1. Start from the same working directory used by a real task.
2. Confirm the intended instruction entrypoint applies to the target file.
3. Confirm every routed specialist is packaged and installed/discoverable.
4. Present an invalid project state and confirm preflight prevents production writes.
5. Create or copy a temporary project from the canonical template and run the same preflight.
6. Re-run validation after a scoped mutation.
7. Confirm the AI action classification and that a human-only decision cannot be executed.
8. Record synthetic, pilot, and operational acceptance separately.

Report errors separately from warnings. A warning is migration debt, not permission to invent state or add empty compliance artifacts. Keep missing legacy directories, approvals, versions, or backflow visible until the project is genuinely migrated.

## Completion Report

Lead with the outcome and include:

- What changed.
- Which existing work semantics were preserved, changed, or left unresolved.
- Current and target digitization profile reached, with adoption evidence stated separately.
- What project/business content was deliberately not changed.
- Baseline and rollback identifiers.
- Validation results with errors separated from warnings.
- Repositories/workspaces and clean/dirty state.
- Runtime activation evidence: working directory, entrypoint, installed capability source, preflight result, and post-write validation.
- Specialist handoffs and their integration status.
- Synthetic-test, pilot-adoption, and operational-acceptance evidence separately.
- Remaining human approvals or external backups.
- The smallest next action.
