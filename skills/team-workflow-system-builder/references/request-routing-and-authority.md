# Request Routing, Digitization Profile, And Authority

Use this reference to decide whether to inspect, model, digitize, AI-enable, repair, hand off, or stop.

## Contents

1. Request classification
2. Digitization gap
3. Read authorization
4. Continuation behavior
5. Specialist handoffs
6. Material boundaries
7. Examples

## 1. Classify The Request

Classify context, action, and authority effects independently. Then record the current and target digitization profile. A composite request needs an ordered chain; do not collapse all phases into one “system build.”

### Context

| Value | Evidence |
|---|---|
| `new` | No trustworthy workflow-system baseline exists |
| `existing` | A workflow, repository, workspace, template pack, or online system exists |
| `continuation` | A current conversation or control file contains an accepted transformation contract |

### Action

| Value | Main result |
|---|---|
| `repository-audit` | Digitization/runtime health map and safe next fixes |
| `guided-start` | Progressive AS-IS recovery and target-boundary confirmation |
| `system-build` | Accepted work translated into a governed digital operating model and MVP |
| `repair-implementation` | Recoverable scoped repair of an online or AI execution system |
| `template-pack` | Copy-ready online-work assets and manifest |
| `role-redesign` | Result ownership and decision-right map without invented policy |
| `material-organization` | Approved materials organized within a recorded boundary |
| `skill-packaging` | Workflow capability boundary and handoff to a dedicated Skill builder when available |

### Authority Profile

| Dimension | Allowed value | Meaning |
|---|---|---|
| Access | `read-only` / `scoped-write` | Inspect only, or modify the exact accepted mutation surface |
| External effect | `none` / explicitly named action | Send, publish, deploy, message, or mutate a named external tool |
| Destructive effect | `none` / explicitly named targets | Overwrite, delete, replace, or perform an irreversible migration |
| Decision recording | `none` / record named human decision | Record evidence of a human decision without making the decision |

Authorization is not a ladder. `scoped-write` does not imply external effects, destructive effects, or decision authority. A request to publish does not imply deletion; permission to record approval does not authorize AI to decide approval.

## 2. Locate The Digitization Gap

Record independent dimensions:

| Dimension | Values | Observable evidence |
|---|---|---|
| Representation | `tacit/manual` / `documented` / `structured` | Stable work objects, states, roles, artifacts, and decisions become progressively explicit |
| Execution surface | `local` / `shared-repository` / `shared-toolspace` / `platform` | Where real participants operate the structured workflow |
| Governance | `unmanaged` / `controlled` / `governed` | Sources, versions, permissions, approvals, audit, and recovery are increasingly active |
| AI coverage | `none` / `assisted` / `executable` per work item | AI drafts or recommends, or performs bounded actions through runtime controls and validation |

Track adoption separately as `designed`, `online-tested`, `pilot-adopted`, or `operationally-accepted`. Use the smallest change that resolves the request. Do not rebuild a working dimension or add AI execution when the underlying work object, state, authority, exception, or acceptance rule is unresolved.

## 3. Read Authorization

An explicit repository/workflow audit authorizes read-only inspection of the named or current workspace. Begin with structure, control files, version history, templates, registries, and runtime entrypoints.

Repository presence alone does not authorize reading unrelated client/stakeholder content. Ask for a material boundary only when deep business content is needed.

## 4. Continuation Behavior

When the user says “continue,” “implement it,” or equivalent:

1. Recover the latest accepted transformation contract.
2. Check repository and workflow evidence for drift.
3. Continue the next safe step inside the same business-work boundary, digitization target, and mutation surface.
4. Do not restart discovery already completed.
5. Do not treat AI-proposed business redesign, custom software architecture, or release as inherited scope.

Continuation may advance only the accepted representation, execution-surface, governance, AI-coverage, or adoption target. If new work changes the meaning of the business process or decision rights, return the decision to the human owner.

## 5. Specialist Handoffs

Route rather than absorb work when:

- a domain method or policy must be judged;
- a custom application, platform, API, database, security, or infrastructure must be designed;
- another reusable Skill must be implemented and packaged;
- organization authority, approval, release, or external commitment is required.

The handoff must state the accepted workflow facts, exact problem, required output, human boundary, validation, and integration destination. The primary Skill remains responsible for reconciling specialist output with the governed digital operating model.

### Registry Resolution

Use `specialist-routing-registry.json` when any work item may leave the owner Skill’s direct boundary.

1. Decompose composite requests before routing.
2. Apply `human-policy-authority` and `domain-method-correctness` before implementation routes.
3. Match the most specific route whose `when` conditions fit and whose `exclusions` do not fit.
4. Use route priority only to resolve otherwise comparable matches.
5. Check the active Skill catalog for the listed candidates. Read the selected Skill before using it.
6. If no named candidate is available, search the active catalog by `discovery_tags`; otherwise return the route’s visible fallback.
7. Do not install missing capabilities without an explicit user request.
8. Record the chosen route, candidate or human owner, required output, validation, integration destination, and result.

The registry does not invoke a Skill by itself. The active host agent performs capability discovery and invocation. This distinction prevents a configuration file from being mistaken for an installed runtime or an autonomous orchestrator.

## 6. Material Boundaries

Before deep organization of client/stakeholder materials, record:

- transformation objective;
- approved source range;
- output form and destination;
- excluded and no-edit range;
- confidentiality, copyright, and reuse restrictions.

Do not infer that permission to organize materials also authorizes changing business rules or publishing results.

## 7. Examples

| Request | Route |
|---|---|
| “把我们现在靠群聊推进的交付流程线上化” | `guided-start/system-build + scoped-write`, recover AS-IS then move representation to structured and choose a shared execution surface |
| “系统已经在线，想让 AI 自动检查交付物” | Preserve the governed shared surface and set `AI coverage=assisted` only for the named review work item |
| “我们还没确定谁能批准报价，先让 AI 自动审批” | Stop and return the policy/authority decision to the human owner |
| “需要开发一个带数据库和权限的 SaaS” | Keep the workflow model here; hand software architecture to an engineering specialist |
| “把稳定工作流打成 Skill” | Define capability/input/output/boundary here; hand Skill internals and eval packaging to a Skill builder |
| “审计后继续修控制面” | `repository-audit -> repair-implementation`; preserve scope, baseline, rollback, and validation |
