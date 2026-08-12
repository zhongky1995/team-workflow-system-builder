---
name: team-workflow-system-builder
description: >-
  Convert an existing or accepted team/project way of working into a shared, governed operating system, then add bounded AI assistance or execution only where it is safe and verifiable. Use for AS-IS recovery, workflow digitization, project workspace/state design, handoffs, Gates, role slots, source/version/decision governance, repository repair, migration, runtime activation, target-workflow work-item/Skill dispatch, AI task boundaries, validation, adoption, retrospectives, knowledge backflow, and packaging a proven workflow for reuse. Use roles, versions, validation, migration, capability routing, or AI-workflow concerns here only when they are part of transforming or repairing a team operating workflow. 中文触发：团队工作数字化、流程线上化、项目管理线上化、AI 工作流、工作项与 Skill 调度、项目工作区、项目治理、仓库审计与修复、交接、门禁、信源、版本、迁移、复盘和知识回流。Do not use it to invent business strategy, domain methodology, organization policy, or arbitrary software architecture that the team has not accepted.
---

# Team Workflow System Builder

Operational revision: `0.7.0`.

Own the transformation contract and integration result:

```text
accepted work
  -> explicit and structured
  -> operated on the chosen local/shared/platform surface
  + proportionate governance
  + bounded AI only where requested and proven
```

Do not act as an all-purpose business consultant, domain expert, application architect, and Skill packager at the same time. Preserve accepted work semantics, identify unresolved business decisions, route specialist implementation, and integrate the result into one operable system.

## Core Boundary

This Skill owns:

- the current-work baseline and transformation boundary;
- AS-IS recovery and TO-BE digital operating model on the appropriate execution surface;
- digitization-profile recovery and target-slice selection;
- work decomposition, specialist routing, integration, migration, and acceptance;
- file-based project governance when the bundled contract and scripts fit.

This Skill does not own:

- business strategy, product strategy, or organization redesign;
- the correctness of an industry/domain method;
- custom application, platform, API, database, security, or infrastructure architecture;
- detailed creation of another Skill when a dedicated Skill-packaging capability is available;
- human decisions about policy, authority, approval, release, or external commitments.

If these are unresolved, record the gap and route it to the responsible human or specialist. Do not invent a business rule merely to make the digital system complete.

## Preserve These Patterns

1. Separate business methods, workflow rules, project facts, evidence, governance, runtime, and reusable knowledge.
2. Treat each formal project workspace as its operational truth source.
3. Route complex work by `stage -> deliverable -> work item` only after the real workflow is understood.
4. Define result-owning role slots and decision rights before mapping job titles.
5. Keep Gate results, artifact states, approval requirements, human approval results, decision sources, and escalation actions separate.
6. Register sources, decisions, terminology, and versions before they affect formal outputs.
7. Separate the mother system/template repository from formal project repositories by default.
8. Establish a recoverable baseline before repair or migration.
9. Distinguish documented design, packaged capability, installation, discovery, invocation, and enforcement.
10. Close only after archive and evidence-backed knowledge backflow.
11. Keep build-time specialist routing separate from the target workflow's runtime work-item dispatch.

Remove industry-specific logic unless the target workflow requires it.

## Route Before Acting

Classify context, action, and authority profile using `references/request-routing-and-authority.md`, then identify the current and target digitization profile.

### Context

- `new`: no reliable workflow-system baseline exists;
- `existing`: a workflow, repository, workspace, or template pack exists;
- `continuation`: a previously accepted audit or implementation contract is current.

### Action

- `repository-audit`: inspect digitization, governance, runtime, and migration health;
- `guided-start`: progressively recover the accepted work and target boundary;
- `system-build`: turn accepted work into a governed digital operating model and implementation MVP;
- `repair-implementation`: repair an existing online or AI execution system safely;
- `template-pack`: deliver copy-ready online-work assets;
- `role-redesign`: clarify result ownership and decision rights without inventing policy;
- `material-organization`: organize approved workflow evidence needed by the selected transformation slice;
- `skill-packaging`: define the workflow capability boundary, then hand detailed packaging to a dedicated Skill builder when available.

### Authority Profile

Record authorization by effect rather than treating risk as one ladder:

- `access`: `read-only` or `scoped-write` for the named mutation surface;
- `external-write`: send, publish, deploy, or change an external system only when explicitly named;
- `destructive`: overwrite, delete, replace, or irreversible migration only for exact confirmed targets;
- `decision-recording`: record a named human decision without making that decision for the human.

One flag does not imply another. Repository write access does not authorize external release, destructive action, or human approval.

“Continue” inherits only the latest accepted transformation contract. It does not authorize a new business method, organization policy, custom platform, or external release.

### Digitization Profile

Record four independent dimensions and change only the smallest necessary slice:

- representation: `tacit/manual`, `documented`, or `structured`;
- execution surface: `local`, `shared-repository`, `shared-toolspace`, or `platform`;
- governance: `unmanaged`, `controlled`, or `governed`;
- AI coverage: `none`, `assisted`, or `executable`, recorded per work item rather than claimed for the whole system.

Track adoption evidence separately as `designed`, `online-tested`, `pilot-adopted`, or `operationally-accepted`. A governed local repository is valid, and one executable AI node does not make the whole workflow AI-executable. Preserve working dimensions and do not add AI while the underlying state, artifact, authority, exception, or acceptance rule is unresolved.

When transformation work may require another capability, read `references/specialist-routing-registry.json`. It routes work needed to build, repair, or package the system. It is not the target team's runtime dispatcher and is not proof that a named Skill is installed.

When the target operating workflow itself will accept AI requests, invoke specialist Skills, or preserve human-only decisions, read `references/runtime-capability-dispatch.md`. Account for every target work item without copying the target business method into this Skill and without turning every work item into a separate Skill.

## Run The Transformation

### 1. Establish The Transformation Contract

Record or infer:

- the existing work to preserve;
- requested online/AI target and output;
- context, action, authority profile, repositories, and exclusions;
- known business rules versus unresolved decisions;
- current and target digitization profile plus adoption evidence;
- decision owner and required human approvals;
- completion evidence, adoption test, and rollback method;
- for AI-maintained files, the real working directory, target paths, instruction scope, and callable capability surface.

For a new or unclear system, use `references/zero-to-one-guided-flow.md`. Ask only the next one or two questions that materially change the digital model.

For an existing repository, read `references/repository-audit-repair.md` and inspect low-risk control surfaces before deep business content.

### 2. Recover The AS-IS Work

Use observed files, tools, records, examples, and decision evidence to map:

```text
scenario
  -> work object
  -> actual trigger
  -> actor / decision owner
  -> action
  -> input and source
  -> output artifact
  -> state change
  -> review / approval
  -> exception and recovery
```

Separate:

- accepted rules;
- actual practice that differs from the written rule;
- historical accidents;
- unresolved or conflicting business decisions;
- digitization assumptions proposed by AI.

Do not silently “improve” the business method while claiming to document it.

### 3. Design The Online Operating Model

Translate the accepted workflow into only the required digital objects:

- project / case / request;
- lifecycle stage and work item;
- actor, owner, reviewer, and decision right;
- source, artifact, version, and active baseline;
- Gate, approval requirement/result/source, action, exception, and audit event;
- archive and reusable-knowledge candidate.

For systems spanning stages, templates, or repositories, read `references/governance-contract.md`, `references/project-workspace-protocol.md`, `references/gates-governance.md`, and `references/role-slot-and-raci.md` only as needed.

Create a template or machine rule only when it represents an accepted work object or protects a frequent/high-risk handoff, decision, evidence, permission, or version boundary.

### 4. Route Build-Time Specialist Implementation

Keep the transformation result unified while routing work by expertise:

- workflow and file-based governance: this Skill;
- unresolved domain method or policy: domain owner / domain specialist;
- custom software, platform, integration, data, security, or infrastructure: architecture/engineering specialist;
- reusable Skill internals, metadata, packaging, and eval design: Skill-packaging specialist;
- external release or organizational authority: human decision owner.

Resolve routing in this order:

1. Split composite requests into independently verifiable work items.
2. Apply human-decision and domain-correctness hard stops first.
3. Match the most specific registry route; use priority only after specificity.
4. Verify the candidate Skill exists in the active catalog and read its `SKILL.md` before invoking it.
5. If no named candidate exists, discover by the registry’s capability tags or return a visible missing-capability handoff. Do not install a Skill unless the user explicitly requests installation.
6. Pass accepted facts, exact problem, required output, human boundary, validation, and integration destination.
7. Reconcile the specialist output with the governed digital operating model before accepting it.

Do not route simple workflow-governance work merely because a more specialized Skill exists. Do not keep specialist work merely because this Skill can describe it. A specialist output is incomplete until it is reconciled with the governed digital operating model.

This routing layer is for the transformation effort. Do not reuse `specialist-routing-registry.json` as the target workflow's production dispatcher. The target runtime needs its own work-item inventory, capability selections, human boundaries, validation, fallback, and writeback contract.

### 5. Implement Online Before AI

For scoped file-based changes:

1. Inspect dirty state and preserve user work.
2. Create an authorized Git commit/tag or an external scope-aligned immutable archive; do not create repository history without write authority.
3. Record allowed files, excluded business content, rollback, and migration semantics.
4. Apply small coherent changes without overwriting frozen/released artifacts.
5. Update the canonical contract, navigation, runtime template, registry, and migration evidence together when affected.
6. Validate from the actual working directory used by real tasks.

Use bundled scripts only when their contract layout fits. Adapt the validation profile to an accepted legacy workflow instead of forcing the workflow to resemble the bundled assets.
Read `references/resource-routing.md` before creating a file-based mother system, selecting template assets, invoking a bundled script, or packaging a distribution.

### 6. Add The AI Execution Layer

AI-enable a work item only when it has clear inputs, permitted actions, expected outputs, evidence, failure behavior, and human authority.

First design the target runtime dispatch contract using `references/runtime-capability-dispatch.md`:

1. Inventory every formal target work item in the selected workflow slice.
2. Mark each item as runtime-routed or explicitly excluded with reason and human owner.
3. For routed items, classify the owner route as `workflow-owner`, `specialist-optional`, or `human-owner`.
4. Classify the AI action as `assist`, `draft`, `recommend`, `execute-reversible`, or `execute-restricted`.
5. Record inputs, allowed actions, outputs, human boundary, pre/post checks, failure behavior, writeback targets, candidate capabilities, selected installed capability, and fallback.
6. Verify candidate, selected, installed, invoked, and accepted states separately. A candidate Skill ID is not runtime activation evidence.
7. Reintegrate specialist results through the workflow owner before Gate, version, or state updates.

Every target work item must be accounted for, but not every item should invoke AI or become a Skill. Human-owned and intentionally non-AI items remain explicit exclusions or `human-owner` routes. Package a separate workflow Skill only after the bounded work item is stable and at least `online-tested`.

Verify this chain:

```text
real task entrypoint
  -> discoverable instructions
  -> current structured state
  -> minimum task context
  -> installed specialist capability
  -> pre-write validation
  -> scoped action
  -> post-write validation
  -> human decision when required
```

Classify each AI node as `assist`, `draft`, `recommend`, `execute-reversible`, or `execute-restricted`. Do not convert advice or approval into autonomous execution.

### 7. Pilot, Migrate, And Backflow

- Test the smallest real workflow slice before broad migration.
- Report representation/surface/governance/AI coverage separately from `online-tested`, `pilot-adopted`, and `operationally-accepted` evidence.
- Keep validation errors separate from migration warnings.
- Preserve unknown legacy state as `not-recorded` rather than guessing.
- Read `references/knowledge-backflow.md` before closure or mother-system updates.

## Minimum Output By Target

- AS-IS recovery: transformation contract, workflow map, unresolved decisions.
- Online model: object/state/action/authority/artifact map plus minimum workspace and migration plan.
- AI enablement: task boundary, context, capability route, human boundary, pre/post validation, and realistic eval.
- Runtime dispatch: full selected-slice work-item inventory, routed/excluded accounting, candidate-versus-selected capability evidence, fallback, reintegration, and adoption state.
- Repair: evidence-backed finding, baseline, scoped change, validation, rollback, and remaining debt.

Do not emit the full system report or complete template pack unless requested. Use `references/output-contracts-by-mode.md`; use `references/system-output-template.md` only for an explicit full system deliverable.

## Completion Check

Before finishing, confirm that:

- the accepted work and unresolved business rules are distinguishable;
- the target digitization profile, adoption evidence, and transformation slice are explicit;
- preserved versus changed workflow semantics are recorded;
- each digital object has a real operational source;
- human and AI authority are separate;
- specialist work was routed and reintegrated rather than silently absorbed;
- each routed work item records its registry route, selected capability or human owner, and fallback when unavailable;
- build-time specialist routes and target runtime routes are stored separately and not confused;
- every target work item in the selected slice is either runtime-routed or explicitly excluded with a reason and human owner;
- candidate Skills are not reported as selected, installed, invoked, or accepted without separate evidence;
- a real online or AI entrypoint was forward-tested when implementation was requested;
- project facts, templates, mother-system knowledge, and released artifacts remain separated;
- repair has a baseline, rollback, validation, and visible warnings;
- the delivered system is no heavier than required for the selected transformation slice.

## Stop Or Route When

- the team has not decided a business rule, policy, decision right, or acceptance standard required by the digital model;
- multiple incompatible workflows fit and no accepted provisional baseline exists;
- custom software/product architecture is required beyond the accepted workflow model;
- a domain method must be judged before it can be digitized;
- a required specialist capability is absent and substituting would change the accepted implementation boundary;
- external/client materials are needed but their reading boundary is unconfirmed;
- structural repair lacks a recoverable baseline;
- overwrite, deletion, publication, approval, or external commitment lacks authority.

Ask only when the missing answer changes the workflow meaning, lifecycle, authority, or release result. Otherwise proceed with explicit, reversible assumptions.

## Reference Routing

- Request and authority: `references/request-routing-and-authority.md`
- Machine-readable specialist routes: `references/specialist-routing-registry.json`
- Target runtime work-item and capability dispatch: `references/runtime-capability-dispatch.md`
- Progressive AS-IS recovery: `references/zero-to-one-guided-flow.md`
- Extended discovery prompts when the next question is unclear: `references/discovery-question-pack.md`
- Existing repository audit/repair: `references/repository-audit-repair.md`
- Legacy monorepo transition: `references/legacy-monorepo-transition.md`
- Status, Gate, version, and migration contract: `references/governance-contract.md`
- Workspace, source, registry, and version: `references/project-workspace-protocol.md`
- Gate, approval requirement/result, and escalation: `references/gates-governance.md`
- Roles and decision rights: `references/role-slot-and-raci.md`
- Closure and backflow: `references/knowledge-backflow.md`
- Output depth: `references/output-contracts-by-mode.md`
- Explicit full system report only: `references/system-output-template.md`
- Bundled scripts, template profiles, and target paths: `references/resource-routing.md`
- Copy-ready files: `assets/templates/`

Load only the references required for the current transformation slice.
