# Project Workspace Protocol

Use this reference for directory/toolspace design, truth-source rules, repository separation, source/version governance, project registration, template versioning, and migration.

## Contents

1. Placement model
2. Mother-system structure
3. Formal-project structure
4. Project control and state
5. Source and terminology governance
6. Version and release governance
7. Template and registry governance
8. Rescue sequence

## Placement Model

A project workspace is the operational truth source for current state, active versions, decisions, risks, evidence, deliverables, archive, and backflow.

The workspace is a digital representation of accepted work, not a substitute business method. Every mandatory object or directory should trace to an actual work object, state, artifact, decision, evidence boundary, or recovery requirement. Do not create the full example tree when the selected digitization slice needs less.

Default placement:

- Mother system: standards, lifecycle, Gates, templates, methods, role rules, governance, reusable knowledge, project registry, and template history.
- Formal project: one project’s facts, drafts, evidence, review records, releases, decisions, archive, and project-specific assets.
- Sandbox/pilot: temporary trials inside the mother system; never the permanent archive of formal projects.

Prefer an independent repository/workspace per formal project. If the team chooses a monorepo or one toolspace, record the tradeoff and add active-project limits, archive/pruning rules, access boundaries, and version baselines.

If a large legacy monorepo already exists, do not batch-move projects. Read `legacy-monorepo-transition.md`, register the current topology, protect new projects with independent placement, and migrate existing projects one at a time after their active version and rollback baseline are resolved.

## Mother-System Structure

Adapt names to the team while preserving responsibilities:

```text
team-operating-system/
  00-system-rules/
    system-version.md
    workflow-contract.json
    system-boundary.md
  01-team-context/
    team-profile.md
    project-type-map.md
  02-workflow/
    lifecycle-map.md
    work-item-map.md
    stage-gate-map.md
  03-role-matrix/
    role-slots.md
    responsibility-matrix.md
    escalation-rules.md
  04-deliverable-standards/
    deliverable-index.md
    review-checklists/
  05-templates/
    project-workspace-template/
      template-manifest.md
  06-sandbox/
  07-source-and-evidence/
    source-quality-rules.md
  08-knowledge-base/
    reusable-cases/
    methods/
    failure-lessons/
    indexes/
  09-governance/
    project-registry.md
    migrations/
    improvement-log.md
  tools/
```

Declare exactly one runtime project-template source. Bundled Skill assets may generate it, but do not remain a second runtime truth source.

## Formal-Project Structure

```text
<project-id>-<name>/
  template-manifest.md
  project-control.md
  00-brief/
    project-brief.md
  01-context/
    stakeholder-context.md
    requirement-notes.md
  02-stage-state/
    stage-state.yaml
  03-work-records/
    work-item-log.md
    meeting-decision-notes.md
    deliverable-review-records.md
  04-deliverables/
    deliverable-index.md
    drafts/
    candidates/
    released/
  05-evidence/
    source-register.md
    pending-sources/
    verified-sources/
    rejected-sources/
  06-decisions-risks-changes/
    decision-log.md
    risk-log.md
    change-log.md
  07-archive-backflow/
    archive-index.md
    retrospective.md
    knowledge-backflow-card.md
```

## Project Control And State

The project control page should answer:

- Project identity, type, and repository/workspace reference.
- Current and target digitization profile plus adoption evidence.
- Existing work semantics being preserved and unresolved business decisions.
- System, template, and contract versions.
- Current stage and work item.
- Current Gate result.
- Current artifact state.
- Approval requirement, human approval state, and the human decision source for the requirement.
- Owner, reviewer, and decision slot.
- Active deliverable and immutable version identity.
- Current source and decision baselines.
- Blockers, pending decisions, next action, and next Gate.
- Last update date and updater.

Keep `stage-state.yaml` machine-readable. Do not combine Gate, artifact, approval, and escalation in one field.

For file-based AI-maintained systems, add an instruction entrypoint at every independently opened mutation root:

```text
AGENTS.md
docs/ai/project-context.md
docs/ai/architecture-guardrails.md
docs/ai/current-task.md
docs/plan/current-todo.md
```

Use these to record scope, allowed files, exclusions, completion evidence, next action, and rollback—not as a duplicate business truth source.

Instruction scope is part of the workspace contract:

- A mother-system entrypoint governs only paths in its scope; it does not automatically govern sibling formal-project repositories.
- A shared umbrella working directory needs a thin routing entrypoint when users start tasks from that directory.
- Every independent formal project needs its own entrypoint because it may be opened without the umbrella or mother system.
- The project contract should require the entrypoint, and validation should fail when it is missing.
- Entry instructions should locate the mother system, read project control first, run pre-write validation, route to the narrowest installed capability, protect immutable artifacts, and run post-write validation.
- Keep entrypoints thin. They activate canonical methods and Skills; they do not duplicate the full workflow.

Track capability state explicitly:

```text
design-documented -> packaged -> installed -> discoverable -> invoked -> validated
```

Do not describe a design note as an active Skill. Prefer one package source plus a deterministic install/link mechanism and a drift check.

For each AI-enabled work item, record whether AI may `assist`, `draft`, `recommend`, `execute-reversible`, or `execute-restricted`, plus the human decision and failure path. Do not infer execution authority from repository write access.

## Source And Terminology Governance

Use a source register when conclusions depend on files, exports, research, screenshots, meeting notes, emails, or changing external references.

| Source state | Meaning |
|---|---|
| `pending` | Received but not checked |
| `needs-original` | Original link/file/trace is missing |
| `needs-date` | Effective date or period is unclear |
| `conflict-pending` | Conflicts with another source |
| `verified` | May support formal conclusions |
| `context-only` | Background only |
| `rejected` | Excluded from formal use |

Record source ID, title, type, provider, date/period, storage path, state, applicable project/stage/deliverable/decision, conflicts, and reuse/quotation boundary.

Track terminology or metric definitions when scope, naming, acceptance, or KPIs can drift. Record definition, applicability, source/decision, owner, state, and conflicts.

## Version And Release Governance

1. Keep one active version per deliverable type.
2. Make every new version inherit from a known predecessor or baseline.
3. Mark old active versions as frozen, replaced, discarded, or archived.
4. Never silently edit frozen or released artifacts.
5. Record path, version, predecessor, change reason, artifact state, owner, date, and checksum/immutable identity for high-risk outputs.
6. Keep human approval separate from artifact state.
7. Record release channel/recipient and replacement or rollback rule.

For Git-backed repositories, keep baseline commits/tags and use small coherent migration commits. For other toolspaces, use platform version history, snapshots, exports, or equivalent immutable evidence.

## Template And Registry Governance

Every generated project should carry `template-manifest.md` with:

- System version.
- Template version.
- Contract/schema version.
- Generation source.
- Creation date.
- Migration history.
- Required AI entrypoint and runtime capability version or source when the project is AI-maintained.

The mother-system project registry should record project ID/name, workspace reference, stage, active version, artifact state, approval requirement, human approval, system/template versions, and last verification. Do not put project facts or sensitive content in the registry.

Update the registry after successful project creation. Make creation transactional: a failed initialization must not leave a registered half-project.

Project creation should refuse placement inside the mother system unless the caller explicitly accepts that exception. Historical embedded projects can remain registered with transitional versions and `not-recorded` states until project-level migration.

## Rescue Sequence

When an existing project is chaotic:

1. Confirm audit/write scope.
2. Inspect dirty state and preserve existing changes.
3. Create an authorized Git tag/commit, archive, export, or platform snapshot as rollback.
4. Record active deliverables and current source/version baseline.
5. Create or repair `project-control.md` and state fields.
6. Register the most important sources, decisions, risks, and terminology conflicts.
7. Write a migration record before moving or renaming structural files.
8. Move only evidence-backed obsolete files into archive.
9. Validate required files, statuses, registry, release evidence, and backflow.
10. Resume from the confirmed active source rather than memory.

Do not treat unnamed screenshots, unrecorded chat decisions, undated drafts, or files outside the controlled workspace as formal truth sources.
