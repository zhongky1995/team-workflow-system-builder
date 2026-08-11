# Workflow And Gate Map

## 1. Project Workflow

| Stage | Goal | Main Actions | Main Output | Owner Slot |
| --- | --- | --- | --- | --- |
| 01 |  |  |  |  |
| 02 |  |  |  |  |
| 03 |  |  |  |  |
| 04 |  |  |  |  |

## 2. Gates

| Gate ID | Gate Name | Node | Pass Condition | Required Evidence | If Not Passed |
| --- | --- | --- | --- | --- | --- |
| `WF-G1` | Intake Gate | Intake | Goal, boundary, project type, owners, and gaps are visible | Intake card and project control | Request material or return |
| `WF-G2` | Planning Gate | Planning | Work items, owners, dependencies, evidence, and review criteria are visible | Plan, baselines, and state | Return or escalate |
| `WF-G3` | Delivery Gate | Internal handoff | Deliverable standard, evidence, terminology, and open comments are controlled | Review record and candidate version | Return for revision |
| `WF-G4` | Release Gate | External release | Immutable version, accepted risks, approval, recipient/channel, and rollback are recorded | Release evidence | Block release |
| `WF-G5` | Closure Gate | Archive/backflow | Final and unresolved items, archive, retrospective, and provenance-aware backflow are complete | Archive and backflow records | Return to closure owner |

## 3. Handoffs

| From | To | Handoff Package | Risk If Missing |
| --- | --- | --- | --- |
|  |  |  |  |

## 4. Decisions

| Decision | Decision Owner | Trigger | Record Location |
| --- | --- | --- | --- |
|  |  |  |  |

## 5. Review Points

| Review Point | Reviewer Slot | Review Object | Gate Result | Artifact State | Approval Requirement | Human Approval |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  | not-checked / pass / conditional-pass / return / blocked | not-recorded / draft / reviewed / revised / candidate / frozen / released / replaced / archived / paused | undetermined / not-required / required | not-recorded / not-requested / pending / approved / rejected |
