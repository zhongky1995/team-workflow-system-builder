# Governance Contract

Use this reference when a workflow system is reused across stages, templates, projects, repositories, or AI sessions.

## Contents

1. Contract layers
2. State model
3. Gate identity
4. Version and template rules
5. Project registry
6. Migration rules
7. Validation rules

## Contract Layers

Keep three versions explicit:

| Version | Meaning |
|---|---|
| System version | Lifecycle, governance, methods, and operating behavior |
| Template version | Copy-ready project workspace schema |
| Contract/schema version | Machine-readable fields, enums, paths, and validation rules |

Do not infer compatibility from matching filenames. Record the versions in the mother system, template manifest, project control page, and migration record.

## State Model

Keep these fields independent:

### Gate result

Default values:

- `not-checked`: no decision yet.
- `pass`: exit conditions are met.
- `conditional-pass`: work may proceed with named non-blocking actions.
- `return`: return to an owner or prior node for revision.
- `blocked`: work cannot proceed until a missing fact, resource, dependency, or decision is resolved.

### Artifact state

Default values:

- `not-recorded`: legacy or imported artifact state has not been evidenced yet; use only during migration.
- `draft`
- `reviewed`
- `revised`
- `candidate`
- `frozen`
- `released`
- `replaced`
- `archived`
- `paused`

### Approval requirement

Default values:

- `undetermined`: the accountable human has not decided whether approval is required.
- `not-required`: an accountable human explicitly decided that no approval is required; cite the decision source.
- `required`: approval is required; cite the rule or decision source.

### Human approval

Default values:

- `not-recorded`: historical approval evidence is absent; never interpret as approved.
- `not-requested`
- `pending`
- `approved`
- `rejected`

### Action or escalation

Use an action field for `request-material`, `return-for-revision`, `escalate`, `pause`, `record-approval-evidence`, or other workflow-specific next actions. Do not encode an action as a Gate state or let an execution action stand in for a human decision.

Rules:

- `candidate` does not mean `approved`.
- `pass` does not mean `released`.
- `undetermined` must not be converted to `not-required` merely to unblock the workflow.
- A decided approval requirement must cite a human decision source.
- `released` requires a decided approval requirement; when approval is `required`, human approval must be `approved`.
- `conditional-pass` must name the remaining actions, owners, and due dates.
- A frozen or released artifact must not be silently overwritten.
- `not-recorded` is an explicit migration state, not a shortcut for skipping current-project governance.

## Gate Identity

Use stable IDs when Gates appear in more than one file or project.

- System Gate: `<NAMESPACE>-G<number>`, such as `DL-G3`.
- Project-specific check: `QA-<PROJECT-OR-TOPIC>-<number>`.
- Keep one canonical mapping of Gate ID to checkpoint name and meaning.
- Do not reuse a system Gate ID for a project-specific check.
- Preserve historical evidence during migration by renaming colliding custom checks to `QA-*` rather than deleting them.

## Version And Template Rules

1. Declare one runtime template source in the mother system.
2. Treat bundled Skill assets as generation inputs, not the runtime truth source of every installed system.
3. Add a template manifest to each generated project.
4. Do not hand-edit two canonical copies of the same template.
5. Upgrade templates through a migration record; do not silently overwrite project facts.
6. Record active artifact path, version, predecessor, status, owner, date, and checksum for high-risk releases.

## Project Registry

The mother system registry should contain only routing metadata:

- Project ID and name.
- Repository/workspace reference.
- Current stage.
- Active artifact version and state.
- Approval requirement, human approval, and their evidence source in the project workspace.
- System/template versions.
- Last verified date.

Keep project facts, business content, evidence, and detailed decisions in the formal project workspace.

When registering legacy projects, use a transitional stage/version, `approval_requirement=undetermined`, and `not-recorded` states rather than inferring artifact or approval history from filenames or README claims.

## Migration Rules

Create a migration record when changing:

- Stage identity or lifecycle order.
- Gate ID, meaning, or allowed result.
- Artifact or approval status semantics.
- Required template files or fields.
- AI instruction entrypoints, runtime capability requirements, or enforcement levels.
- Target runtime work-item inventory, dispatch route, AI action class, selected capability, fallback, or writeback semantics.
- Mother-system/project placement.
- Release, archive, or backflow rules.

Record from/to versions, affected projects, actions, excluded content, rollback point, validation, and unresolved human decisions.

For schema `0.4.x -> 0.5.x`, map old `human_approval=not-required` to `approval_requirement=not-required` plus `human_approval=not-requested` only when a human decision source exists. Otherwise migrate to `approval_requirement=undetermined`; do not manufacture a decision source.

For schema `0.5.x -> 0.6.x`, keep `ai_runtime.enabled=false` until a target-owned dispatch registry accounts for the complete selected-slice work-item inventory. Do not convert build-time specialist routes or candidate Skill IDs into runtime installation evidence.

## Validation Rules

For a reusable file-based system, validate at least:

- Contract JSON is parseable; required nested fields exist; enums are unique; malformed contracts fail without crashing the validator.
- Stage and Gate IDs are unique.
- Template Gate labels match canonical definitions.
- Required project files exist.
- Required AI entrypoints exist at the umbrella, mother-system, and formal-project roots that are actually used.
- Routed capabilities are packaged and installed/discoverable; installed copies or links match the canonical package.
- Build-time specialist routes and target runtime dispatch are separate; every target work item in the selected slice is routed or explicitly excluded.
- Candidate capability IDs are not treated as selected or installed evidence; required selected capabilities resolve to recorded installed paths.
- Pre-write validation is distinguishable from advisory documentation and post-write reporting.
- Project status fields use allowed values and required operational fields are nonblank.
- Registry rows use the canonical schema, point to valid locations when locally available, and match project state exactly.
- Approval requirement, result, and human decision source are consistent.
- Frozen/released artifacts have version, immutable identity, and approval evidence.
- Eligible projects have non-template backflow records.
- Project-specific checks use `QA-*`.
- Distribution packages exclude VCS, caches, OS metadata, existing archives, and all symbolic links.

Start from `assets/templates/workflow-contract.json` and adapt the values to the team’s actual lifecycle.
