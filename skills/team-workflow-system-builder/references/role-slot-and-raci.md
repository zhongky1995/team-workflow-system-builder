# Role Slots And RACI Patterns

## Contents

1. Role-slot principle
2. Default slots
3. Responsibility markers and matrix
4. Merge and separation rules
5. Decision and escalation rights

Use this reference when designing team responsibilities, owner boundaries, handoffs, and overload protection.

## Principle

Role slots are not job titles.

A role slot describes a result responsibility. One person can hold multiple slots in a light project, but complex projects should separate high-conflict slots.

## Default Role Slots

| Slot | Name | Main Responsibility | Failure Risk If Missing |
| --- | --- | --- | --- |
| R1 | Demand / Business Interface | Intake, stakeholder expectation, scope signal, external communication | Vague requests become work; stakeholder promises are not translated |
| R2 | Project Governance Owner | Timeline, stage state, handoff, blockers, meeting outputs, project control page | Project runs on memory and reminders |
| R3 | Domain Strategy / Solution Owner | Problem definition, solution logic, strategic judgment, deliverable storyline | Team executes before knowing the real problem |
| R4 | Data / Research / Analysis Owner | Source quality, analysis, metrics, evidence, insight reliability | Conclusions and metrics drift across stages |
| R5 | Execution / Implementation Owner | Concrete task execution, production, publishing, build, operation, delivery actions | Plans do not become action or action cannot be traced |
| R6 | Quality Review Owner | Independent review, release readiness, deliverable standards, defect/issue closure | Low-quality outputs reach stakeholders |
| R7 | Closure / Knowledge Backflow Owner | Archive, acceptance evidence, retrospective, reusable case/SOP/template update | Projects finish but do not become assets |
| R8 | Final Decision Owner | Scope, KPI, acceptance, budget/resource, priority, major conflict decisions | Disputes linger or daily owners make decisions beyond authority |

## Responsibility Markers

Use simple markers instead of overcomplicated RACI labels when working in Chinese:

| Marker | Meaning |
| --- | --- |
| 主 | Owns the result and drives completion |
| 协 | Provides key input or execution support |
| 审 | Reviews quality or readiness |
| 确 | Confirms scope, conclusion, or acceptance |
| 拍 | Makes final decision when risk or dispute exists |
| 外 | External dependency |
| - | Normally not involved |

## Default Matrix Skeleton

| Work Item | R1 Demand | R2 Governance | R3 Strategy | R4 Analysis | R5 Execution | R6 Review | R7 Backflow | R8 Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| W01 Intake | 主 | 协 | 协 | - | - | - | - | 确 |
| W02 Problem Definition | 协 | 协 | 主 | 协 | - | - | - | 确 |
| W03 Planning | 协 | 主 | 协 | 协 | 协 | - | - | 确 |
| W04 Execution | - | 协 | 协 | 协 | 主 | - | - | - |
| W05 Review / Release | 协 | 主 | 协 | 协 | 协 | 审 | - | 确 / 拍 |
| W06 Change / Exception | 协 | 主 | 协 | 协 | 协 | 审 | - | 拍 |
| W07 Closure | 协 | 协 | 协 | 协 | 协 | 审 | 主 | 确 |
| W08 Knowledge Backflow | - | 协 | 协 | 协 | 协 | - | 主 | 确 |

Adjust work items to the team's lifecycle.

## Slots That Are Risky To Combine In Complex Projects

Avoid combining these for standard or complex projects unless there is a clear reason:

| Combination | Risk |
| --- | --- |
| R1 Demand + R8 Final Decision | Stakeholder pressure can bypass project reality |
| R2 Governance + R5 Execution | Coordination work gets swallowed by daily execution |
| R3 Strategy + R6 Quality Review | The author reviews their own logic too leniently |
| R4 Analysis + R6 Quality Review | Data creator may miss independent evidence issues |
| R5 Execution + R7 Backflow | Closure and reuse get skipped under delivery pressure |
| R8 Final Decision + high-frequency execution | Decision owner becomes a bottleneck and loses oversight |

## Slots That Can Merge In Light Projects

These can merge when project risk is low:

| Merge | Condition |
| --- | --- |
| R2 Governance + R5 Execution | Small project, few dependencies, short timeline |
| R3 Strategy + R4 Analysis | Same person has enough domain and evidence control |
| R6 Review + R8 Decision | Low-risk internal deliverable |
| R7 Backflow + R2 Governance | Closure is part of project management routine |

Always state the merge explicitly so the team knows which risk it is accepting.

## Project-Type Adjustments

### Client Delivery

Important separations:

- R1 external expectation vs R2 delivery governance.
- R3 solution logic vs R6 review.
- R7 closure/backflow should start before final acceptance.

### Product / R&D

Rename slots:

- R1 = request/product interface.
- R3 = product/solution owner.
- R5 = engineering/design/implementation.
- R6 = QA/release review.
- R8 = product/business decision owner.

### Operations / Content / Campaign

Important separations:

- R3 campaign logic.
- R5 production/publishing.
- R4 performance monitoring.
- R6 brand/compliance/release review.

### Data / AI Project

Important separations:

- R4 data/source/evaluation owner.
- R6 model/output review owner.
- R8 human decision boundary owner.

## Overload Signals

Flag the system as overloaded when:

- One person holds more than 4 active slots in a standard project.
- The same person owns execution and final decision for high-risk changes.
- Review is performed only by the artifact author.
- Closure/backflow has no named owner.
- Project governance depends on whoever remembers to update status.
