# Legacy Monorepo Transition

Use this reference when a mature mother system already contains many formal projects, large binary assets, historical snapshots, duplicated templates, or no reliable version-control baseline.

## Contents

1. Transition target
2. Audit without content flooding
3. Scope-aligned baseline
4. Registered transition
5. Validation debt
6. Project migration batches

## Transition Target

Do not make immediate directory purity the goal. Establish a controlled transition:

- New formal projects default to independent workspaces.
- Existing embedded projects remain in place until individually baselined and migrated.
- The mother-system registry records routing metadata and a transitional state such as `legacy-unversioned` or `not-recorded`.
- One runtime template source governs new work.
- Historical distribution snapshots remain immutable and are not hand-maintained as a second runtime source.

## Audit Without Content Flooding

Start with metadata and control surfaces:

1. Measure total size, file count, top-level size distribution, project count, nested repositories, and binary-heavy areas.
2. Inspect navigation, project controls, source/version registers, lifecycle, Gates, template sources, registries, retrospective/backflow, and automation.
3. Sample 2-3 project governance surfaces representing new, mature, and legacy projects.
4. Do not open client binaries or bulk-read project content unless a control-plane finding requires it and the material boundary permits it.

Treat a long project README as routing evidence, not proof of approval, release, or backflow completion.

## Scope-Aligned Baseline

For a large non-Git workspace, a full archive may be slow, wasteful, or unsafe. A scoped baseline is valid when all are true:

- The repair contract lists every mutable control file or directory.
- Client/project content and large binaries are explicitly excluded and remain untouched.
- The control files are archived outside the target before edits.
- The archive checksum, included paths, timestamp, and restore rule are recorded.
- A full topology/inventory is retained when structural placement claims depend on it.

Use `scripts/create_scoped_baseline.py` for the archive and manifest. A scoped baseline does not authorize later edits outside its recorded mutation surface.

## Registered Transition

1. Establish system, template, and contract versions without retroactively applying them to legacy projects.
2. Add stable lifecycle and Gate IDs.
3. Add `not-recorded` for absent historical artifact/approval evidence and `approval_requirement=undetermined` when the approval rule itself is unknown.
4. Register every formal project with ID, name, workspace, transitional stage, active-version pointer, artifact state, approval requirement/result, version adoption, and last verified date.
5. Keep project facts in each project workspace; do not copy them into the registry.
6. Protect new-project creation so it defaults outside the mother system and registers only after successful initialization.

## Validation Debt

Classify validation output:

- Error: contract inconsistency, duplicate identity, missing required truth source, invalid state, unsafe release claim, or broken registry reference.
- Warning: recommended legacy directory missing, project version not migrated, approval not recorded, backflow incomplete, or external backup pending.

Do not eliminate warnings by creating empty directories, blank retrospectives, placeholder approvals, or invented active versions. Record the warning as project migration debt with an owner or future batch.

## Project Migration Batches

Migrate one project or a small risk-aligned batch:

1. Resolve its active deliverable and source/version baseline.
2. Create an independent snapshot or repository baseline.
3. Map legacy states to the canonical contract using evidence.
4. Add or repair project control, Gate, decisions/risks/changes, release evidence, archive, and backflow.
5. Validate the project.
6. Update its registry row only after validation.
7. Move the workspace only when references, access, backup, and rollback are confirmed.

Leave projects that have not passed these steps in the registered transitional state.
