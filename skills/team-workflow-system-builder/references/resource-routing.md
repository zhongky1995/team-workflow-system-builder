# Bundled Resource Routing

Use this reference when the selected transformation slice needs file-based implementation, validation, packaging, or a reusable template profile. Do not copy every asset by default.

## Scripts

| Script | Use when | Preconditions | Writes | Required follow-up |
|---|---|---|---|---|
| `scripts/create_system.py` | A new file-based mother system needs a deterministic starting layout | Accepted workflow boundary; new target path | Creates a new mother system only; refuses existing paths | Adapt the contract to accepted work, validate, then establish an immutable baseline |
| `scripts/create_project.py` | A formal project should be generated from the current runtime template | Valid mother system, existing workspace parent, accepted project ID/name | Creates one project, validates it, and registers it transactionally; Git history is created only with explicit `--init-git` | Resolve initialization fields and external backup warnings |
| `scripts/validate_workflow_system.py` | A mother system or named formal projects need contract validation | File-based layout using the bundled contract schema or an explicitly adapted compatible profile | Read-only | Keep errors separate from warnings; do not fake legacy state to clear warnings |
| `scripts/create_scoped_baseline.py` | A non-Git or large repair needs an external rollback snapshot | Exact mutation paths and explicit exclusions | Writes a tar archive and manifest outside the target | Record archive identity and restore rule in the migration record |
| `scripts/package_system.py` | A validated mother system needs deterministic ZIP distribution | Valid system; no symbolic links | Writes one ZIP with preserved file modes and an embedded SHA-256 manifest; refuses existing output unless `--overwrite` is explicit | Verify recipient/release authority separately |
| `scripts/validate_specialist_routing_registry.py` | The specialist registry changes | Registry JSON present | Read-only | Re-run Skill evals for changed routing behavior |

Run scripts from their installed Skill path. Do not assume that listing a script here authorizes its writes. Resolve target paths and authority first.

After changing bundled scripts or the machine contract, run:

```bash
python3 -m unittest discover -s <skill-root>/tests -v
```

## System Bootstrap Profiles

`create_system.py --profile minimal` creates only:

- the system version and machine contract;
- the canonical Gate map;
- the project registry;
- the contract-required formal-project template files.

`create_system.py --profile standard` adds common intake, context, work-record, version, evidence, knowledge, and governance directories. It is still a starter profile, not a business method. Remove or rename objects that do not trace to accepted work before adoption.

The script deliberately does not create Git history. After the team-specific contract is accepted, establish an authorized Git commit/tag or external immutable baseline.

## Project Template Asset Map

| Asset | Default target in a formal project | Use when |
|---|---|---|
| `template-manifest.md` | `template-manifest.md` | Always for generated projects |
| `project-control.md` | `project-control.md` | Always for file-based project truth state |
| `stage-state.yaml` | `02-stage-state/stage-state.yaml` | Always when machine validation is used |
| `intake-card.md` | `00-brief/intake-card.md` | Requests often enter incomplete or from multiple channels |
| `scenario-card.md` | `00-brief/scenario-card.md` | The real work object or boundary is still being recovered |
| `client-alignment-card.md` | `01-context/client-alignment-card.md` | Stakeholder goals, scope, or reading permission need confirmation |
| `material-reading-plan.md` | `01-context/material-reading-plan.md` | Deep client/stakeholder materials must be read within an approved boundary |
| `work-item-record.md` | `03-work-records/work-item-record.md` | Handoffs need explicit input/output/state/evidence |
| `deliverable-review-checklist.md` | `03-work-records/deliverable-review-checklist.md` | Deliverables require repeatable quality review |
| `active-version-index.md` | `04-deliverables/active-version-index.md` | More than one artifact version can affect active work or release |
| `source-register.md` | `05-evidence/source-register.md` | Formal claims depend on sources, exports, screenshots, or changing references |
| `decision-log.md` | `06-decisions-risks-changes/decision-log.md` | Decisions change scope, baselines, acceptance, or authority |
| `risk-log.md` | `06-decisions-risks-changes/risk-log.md` | Risks need owners, triggers, and mitigation |
| `change-log.md` | `06-decisions-risks-changes/change-log.md` | Scope/KPI/timeline/resource/acceptance changes need control |
| `archive-index.md` | `07-archive-backflow/archive-index.md` | Project closure or formal archive is in scope |
| `retrospective.md` | `07-archive-backflow/retrospective.md` | Outcome/process evidence must be reviewed |
| `knowledge-backflow-card.md` | `07-archive-backflow/knowledge-backflow-card.md` | Evidence-backed reusable knowledge may return to the mother system |

Mother-system-only assets include `system-version.md`, `workflow-contract.json`, `workflow-gate-map.md`, and `project-registry.md`. `decision-risk-change-log.md` is a compact alternative to the three separate logs; do not install both as competing truth sources.

`ai-work-item-dispatch.json` is a mother-system runtime asset. Keep it disabled and empty until the selected workflow slice has an accepted work-item inventory and AI runtime is explicitly in scope. When enabled, every inventoried item must be runtime-routed or explicitly excluded; see `references/runtime-capability-dispatch.md`.

## Safe Invocation Order

```text
accepted transformation contract
  -> create/adapt system
  -> validate system
  -> establish authorized baseline
  -> create project
  -> validate project and registry coherence
  -> pilot real work
  -> package only after validation and release authorization
```

If a legacy layout differs, adapt the contract and validator profile through a recorded migration. Do not rearrange accepted work merely to make these bundled paths pass.
