# Standard System Output Template

Use this structure when the user asks for a full team-specific project management or workflow system.

Keep the output practical. Do not fill every section with abstract theory. If information is missing, state reversible operating assumptions and continue only where they do not invent business rules, approval requirements, decision rights, or release authority.

## Contents

1. Conclusion and working contract
2. Existing work, digitization profile, and target boundary
3. AS-IS/TO-BE workflow, work items, decisions, and exceptions
4. Online objects, roles, workspace, and governance
5. AI boundaries, specialist handoffs, runtime, and migration
6. Backflow, pilot, acceptance, and next step

## 1. One-Line Conclusion

State what kind of operating system the team needs.

Example:

> This team first needs its existing intake-to-delivery work represented as shared objects, states, artifacts, and decisions; after that operating slice runs reliably, AI can take over bounded drafting and review tasks.

## 2. Facts, Assumptions, And Design Implications

### Confirmation Status

- Context: new / existing / continuation
- Action: repository-audit / guided-start / system-build / repair-implementation / template-pack / role-redesign / material-organization / skill-packaging
- Access: read-only / scoped-write
- External write authorized: none / exact named action
- Destructive action authorized: none / exact named targets
- Human decision recording authorized: none / exact named decision evidence
- Business/use scenario confirmed: yes / no
- Customer/stakeholder goal confirmed: yes / no
- First-phase output confirmed: yes / no
- Scope boundary confirmed: yes / no
- Workflow direction confirmed: yes / no
- Gate/handoff direction confirmed: yes / no
- Current digitization profile confirmed: yes / no
- Target digitization profile confirmed: yes / no
- Adoption evidence confirmed: yes / no
- Existing work semantics to preserve confirmed: yes / no
- Unresolved business rules identified: yes / no
- Human-only and AI-eligible work boundary confirmed: yes / no
- Materials approved for reading: yes / no
- Repository/material organization exception invoked: yes / no
- If yes, exact user/customer wording:
- Rollback method confirmed when writes are allowed: yes / no / not-required

### Known Facts

- ...

### Working Assumptions

- ...

### Design Implications

- ...

## 3. Business / Use Scenario

### Scenario One-Liner

This project-based management system serves ...

### Typical Project Object

- ...

### Primary Users

- ...

### Scenario Boundary

- In scenario:
- Out of scenario:

## 4. User Value And Business Goal

### Team Value One-Liner

Help the team ...

### Business Goal One-Liner

Turn project work from ... into ...

## 5. Existing Work, Digitization Profile, And System Boundary

### AS-IS Work Evidence

- Representative real case:
- Written rule or SOP:
- Actual practice difference:
- Existing tools and artifacts:
- Business rules already accepted:
- Business rules still unresolved:

### Digitization Profile

- Representation: tacit/manual / documented / structured
- Execution surface: local / shared-repository / shared-toolspace / platform
- Governance: unmanaged / controlled / governed
- AI coverage by named work item: none / assisted / executable
- Adoption evidence: designed / online-tested / pilot-adopted / operationally-accepted
- Target changes for this implementation:
- Working dimensions to preserve:
- Explicitly excluded changes:

### In Scope

- Project intake and scoping.
- Stage management.
- Role responsibility.
- Deliverable review.
- Source/version/decision governance.
- Retrospective and knowledge backflow.

### Out Of Scope For MVP

- Full performance management.
- Organization restructuring.
- Heavy tool migration.
- Automation before the process is stable.

Adjust these bullets to the user's team.

## 6. AS-IS And TO-BE Workflow

Show both when they differ. Do not silently replace actual work with the proposed digital process.

Use a table:

| Stage / Node | AS-IS Trigger And Action | TO-BE Online Operation | Inputs / Sources | Output / State Change | Decision / Exception |
| --- | --- | --- | --- | --- | --- |
| 01 Intake |  |  |  |  |  |
| 02 Planning |  |  |  |  |  |
| 03 Execution |  |  |  |  |  |
| 04 Review / Delivery |  |  |  |  |  |
| 05 Closure / Backflow |  |  |  |  |  |

Rename stages based on the team type.

## 7. Work Item Map

Use stable work item codes only when useful.

| Code | Work Item | Owner Slot | Collaborators | Output | Gate |
| --- | --- | --- | --- | --- | --- |
| W01 |  |  |  |  |  |

## 8. Gate, Handoff, And Decision Map

| Node | Gate / Handoff / Decision | Owner Slot | Required Evidence | If Not Passed |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## 9. Professional Knowledge Gap Map

Separate process gaps from knowledge gaps.

| Gap Type | Gap | Why It Matters | How To Fill | Priority |
| --- | --- | --- | --- | --- |
| Process |  |  |  | P0 / P1 / P2 |
| Knowledge |  |  |  | P0 / P1 / P2 |

## 10. Role Slots And Responsibility Matrix

Explain that slots are not job titles.

| Slot | Responsibility | Failure Risk If Missing | Can Merge In Light Projects? |
| --- | --- | --- | --- |
| R1 Demand / Business Interface |  |  |  |
| R2 Project Governance Owner |  |  |  |
| R3 Domain Strategy / Solution Owner |  |  |  |
| R4 Data / Research / Analysis Owner |  |  |  |
| R5 Execution / Implementation Owner |  |  |  |
| R6 Quality Review Owner |  |  |  |
| R7 Closure / Knowledge Backflow Owner |  |  |  |
| R8 Final Decision Owner |  |  |  |

Then add a RACI-style matrix:

| Work Item | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W01 | 主 | 协 | - | - | - | - | - | 确 |

Use Chinese markers when helpful:

- `主`: owns the result.
- `协`: provides key input or execution.
- `审`: reviews quality.
- `确`: confirms scope or conclusion.
- `拍`: final decision for disputes.
- `-`: normally not involved.

## 11. Project Workspace

Provide the recommended directory or tool-space structure.

```text
team-project-system/
  00-system-rules/
  01-team-context/
  02-workflow/
  03-role-matrix/
  04-deliverable-standards/
  05-templates/
    project-workspace-template/
  06-sandbox/
  07-source-and-evidence/
  08-knowledge-base/
  09-governance/
```

Define repository/workspace placement:

| Layer | Default Location | Contains | Does Not Contain |
| --- | --- | --- | --- |
| Mother system repo/toolspace | `team-project-system/` | Standards, workflow, gates, templates, governance, reusable knowledge | Long-running formal project facts and drafts |
| Template source | `team-project-system/05-templates/project-workspace-template/` | Copy-ready project skeleton | Active project work |
| Sandbox / pilot | `team-project-system/06-sandbox/` | Temporary trials | Permanent formal project archive |
| Formal project | Independent repo/workspace generated from `_template/` | Project control, facts, drafts, evidence, reviews, releases, archive | Generic method changes unless approved for backflow |

For reusable file-based systems, also define the system version, contract version, template version, project registry, runtime template source, and migration location.

Do not treat the suggested directory tree as mandatory. Materialize only the objects required by the selected digitization slice and preserve working tools that do not need replacement.

Then define project-level truth source:

```text
<independent-project-repo-or-workspace>/<project-id>/
  project-control.md
  00-brief/
  01-context/
  02-stage-state/
  03-work-records/
  04-deliverables/
  05-evidence/
  06-decisions-risks-changes/
  07-archive-backflow/
```

## 12. Deliverable Standards

| Deliverable | Purpose | Minimum Contents | Review Owner | Send/Release Gate |
| --- | --- | --- | --- | --- |
| Project brief |  |  |  |  |
| Project plan |  |  |  |  |
| Review report |  |  |  |  |
| Closure package |  |  |  |  |

Adjust deliverables to the team.

## 13. Gates And Escalation

| Gate | When To Check | Pass Condition | Required Evidence | If Not Passed |
| --- | --- | --- | --- | --- |
| Intake gate | Before project starts |  |  |  |
| Planning gate | Before execution |  |  |  |
| Delivery gate | Before internal handoff |  |  |  |
| Release gate | Before external release |  |  |  |
| Closure gate | Before archive |  |  |  |

Escalation rules:

- Missing material: request material and keep the node open.
- No response from collaborator: remind once, then escalate to governance owner.
- Scope/KPI/acceptance change: record change, then escalate to final decision owner.
- Quality risk: return to owner with review comments and do not release.

## 14. Collaboration Cadence

| Cadence | Participants | Purpose | Required Output |
| --- | --- | --- | --- |
| Intake sync |  |  |  |
| Weekly project review |  |  |  |
| Gate review |  |  |  |
| Retrospective |  |  |  |

Avoid meetings that have no required output.

## 15. Governance Rules

### Source Governance

- New source enters a source register before it becomes a formal fact.
- Unverified sources can be referenced as context, not as confirmed conclusions.

### Version Governance

- Each deliverable type has only one active version at a time.
- Old versions are frozen, replaced, or archived with a reason.
- Candidate, frozen, and released are artifact states, not Gate results or proof of human approval.

### State And Gate Governance

- Define Gate results, artifact states, approval requirements, human approval results, decision sources, and escalation actions independently.
- Keep stable Gate IDs and names in one canonical contract.
- Use `QA-*` for project-specific checks instead of reusing system Gate IDs.

### Template And Migration Governance

- Declare one runtime template source.
- Record system/template/contract versions in each generated project.
- Migrate templates and existing projects through a recorded, reversible change.

###口径 Governance

- Metrics, terms, scope, and assumptions must have a current accepted definition.
- Conflicts are recorded as pending decision, not silently resolved.

### Decision Governance

- Decisions that affect scope, KPI, delivery, budget, acceptance, or external commitment require an explicit decision owner.

## 16. Knowledge Backflow

Define what must return to the team system after closure:

- Reusable template improvement.
- Case or example.
- SOP update.
- Failure lesson.
- Metric benchmark.
- Decision rule.

Use a table:

| Backflow Item | Source Project Evidence | Where It Goes | Owner | Deadline |
| --- | --- | --- | --- | --- |

## 17. MVP Rollout Plan

### Week 1

- Recover one real AS-IS case and freeze accepted versus unresolved rules.
- Implement the smallest required structured workflow slice on the chosen execution surface.

### Week 2

- Run one or two active cases through the digital operating slice.
- Record fidelity gaps, bypasses, missing decisions, and unnecessary controls.

### Week 3-4

- Stabilize the digital operating model and migration rule.
- Only then AI-enable named work items with clear human boundaries and evals.

Adjust timeline to the user's team.

## 18. First Implementation Slice

List only the assets required by the selected digitization-profile change:

| Asset / Mechanism | Existing Work Source | Why It Is Required Now | Human Owner | AI Role | Validation |
| --- | --- | --- | --- | --- | --- |

Do not create a complete template pack by default. Add an asset only when it represents an accepted work object or protects a frequent/high-risk boundary.

## 19. Next Step

State the next concrete action:

- If the AS-IS is unclear: recover one real case.
- If the AS-IS is accepted but not structured: build the minimum digital operating model and only its required assets.
- If the digital operating model exists: run one pilot case.
- If the pilot exists: fix fidelity and adoption friction before AI automation.
- If the digital operating slice is stable: AI-enable one bounded task only when requested.
- If the capability is stable: hand packaging to a dedicated Skill builder or tool workflow.
