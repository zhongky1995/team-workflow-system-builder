# Gates, Review, Approval, And Escalation

Use this reference when designing stage transitions, deliverable reviews, release decisions, and escalation.

## Contents

1. Gate semantics
2. Gate card
3. Lifecycle Gates
4. Deliverable review
5. Escalation
6. Governance by team size
7. Anti-patterns

## Gate Semantics

A stage is complete only when its required output and evidence are visible. A meeting, chat thread, verbal agreement, or memory is not enough.

Use only the Gate results defined in the system contract:

| Result | Meaning | Can proceed? |
|---|---|---|
| `not-checked` | No Gate decision exists | No |
| `pass` | Exit conditions are met | Yes |
| `conditional-pass` | Named non-blocking actions remain | Yes, within the stated condition |
| `return` | Revision is required | No |
| `blocked` | Missing fact, dependency, resource, or decision prevents progress | No |

Keep these separate:

- Artifact state such as `candidate`, `frozen`, or `released`.
- Approval requirement such as `undetermined`, `not-required`, or `required`.
- Human approval such as `not-requested`, `pending`, or `approved`.
- Next action such as `request-material`, `return-for-revision`, or `escalate`.

`escalate` is an action, not a Gate result. `released` is an artifact state, not proof of Gate pass or human approval.

## Gate Card

| Field | Description |
|---|---|
| Gate ID and name | Stable system identity |
| Stage/node | Where the check applies |
| Entry condition | What must exist before work starts |
| Exit condition | What must be true before leaving |
| Required evidence | Files, records, decisions, sources, checklists, acceptance proof |
| Owner slot | Who drives the Gate |
| Review slot | Who checks quality |
| Decision slot | Who resolves disputes or approves |
| Gate result | One canonical Gate result |
| Artifact state | Independent current artifact state |
| Approval requirement | Independent human rule with a decision source |
| Human approval | Independent result state |
| Remaining action | Owner, due date, and escalation path |

Use `assets/templates/stage-gate-card.md`.

## Lifecycle Gates

### Intake Gate

Check before full execution.

Pass evidence:

- Request owner and expected output are known.
- Project type and boundary are clear enough.
- Missing information is visible.
- Decision owner is known when scope is uncertain.

If not passed, produce only a clarification list or reversible minimal diagnosis.

### Planning Gate

Check before execution.

Pass evidence:

- Goal, work items, owners, dependencies, and review criteria are visible.
- Active source/version/terminology baseline exists when needed.
- Project control page and stage state are current.

If not passed, return to the planning owner or escalate a scope/resource/decision blocker.

### Delivery Gate

Check before internal handoff or external delivery.

Pass evidence:

- Deliverable meets its standard.
- Claims trace to evidence.
- Active version is correct.
- Review comments are closed or explicitly accepted.
- Stakeholder-facing terminology matches the current baseline.

A `conditional-pass` may permit internal progression with named actions. Do not treat it as external release approval unless the system contract explicitly allows that Gate to do so.

### Release Gate

Check before publishing, sending, freezing, or making an external commitment.

Pass evidence:

- Candidate version, checksum or immutable identity, and source lineage are recorded.
- Gate results and accepted risks are complete.
- Approval requirement is decided and cites a human decision source.
- Human approval is `approved` when the requirement is `required`.
- Release notes, recipient/channel, and rollback or replacement rule are clear.

Do not release while required human approval is `pending`.

### Change Gate

Check when scope, KPI, timeline, resource, acceptance, deliverable, or external promise changes.

Require a change reason, impact, affected artifacts/owners, decision owner, and updated baselines. Keep the current baseline when the change is not approved.

### Closure Gate

Check before archive.

Require final/unresolved item separation, version identity, evidence package, archive index, retrospective, provenance-aware backflow, and assigned follow-ups.

## Deliverable Review

Review purpose, audience, completeness, evidence, terminology, active version, open decisions, risks, and next action.

Use the canonical Gate result for the review outcome. Record escalation separately. Use `assets/templates/deliverable-review-checklist.md`.

## Escalation

| Situation | Action |
|---|---|
| Missing material | Request material and keep Gate `blocked` or `return` |
| Collaborator unresponsive | Remind once, then escalate to governance owner |
| Scope/KPI/acceptance change | Record change and ask decision owner |
| Timeline risk | Update project control and assign mitigation |
| Quality review fails | Set Gate `return` with evidence and owner |
| Source conflict | Keep source `conflict-pending`; do not use as confirmed fact |
| Version confusion | Freeze the active source decision before continuing |
| Approval requirement undetermined | Return the rule to the decision owner; do not release |
| Approval pending | Keep artifact candidate; do not release |

## Governance By Team Size

### 1-3 people

Use project control, active-version rule, decision/risk/change log, one Gate card, and retrospective/backflow.

### 4-10 people

Add role slots, stage Gates, deliverable review, source register, project registry, and required weekly review outputs.

### 10+ or cross-team

Add formal handoff packages, independent review, escalation paths, version timelines, terminology alignment, migration records, and closure ownership.

## Anti-Patterns

- Creating many templates before finding the real breakpoint.
- Using one field for Gate, artifact, approval requirement/result, and action.
- Letting the project manager own every result.
- Keeping released artifacts editable without replacement rules.
- Reviewing only at the end.
- Treating chat history as the only decision record.
- Calling a project closed before archive and backflow are complete.
