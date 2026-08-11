# Discovery Question Pack

## Contents

1. Usage rule
2. Progressive questions
3. Scenario and project boundary
4. Workflow, Gates, roles, and handoffs
5. Sources, versions, decisions, and knowledge gaps
6. Output, rollout, and material boundary

Use this pack when the team context is not clear enough to design a workflow system.

Ask at most 1-2 questions in one round by default. Prefer the next question that directly changes the scenario, workflow, gates, or knowledge-gap map.

Do not open with a 5-8 question checklist unless the user explicitly asks for a questionnaire.

For a new or unclear system, do not read detailed client/stakeholder materials until the goal, scope, output, decision owner, and material boundary are clear enough. Start with the progressive questions below.

Skip zero-start discovery when the user explicitly requests a read-only audit of the current repository or continues an already confirmed task. Audit governance surfaces first and request a client-material boundary only if deep content is required.

When the user explicitly says to use current repository/materials for整理, first record the整理目标、使用范围、输出形态 and reading boundary.

## Progressive Zero-Start Questions

Use these step by step before designing a new system from customer materials:

1. Scenario: 这套项目制管理主要服务哪个业务场景或使用场景？
2. Workflow: 一个典型项目从需求进入到完成/复盘，大概经历哪些步骤？
3. Gates: 哪些节点必须确认、评审、交接或拍板？
4. Knowledge gaps: 团队还缺哪些专业知识、判断标准、模板、案例或 SOP？
5. Output: 第一版希望输出蓝图、流程门禁表、模板包、项目工作区结构，还是完整方案？
6. Materials: 是否允许读取现有材料？如果允许，读取范围是什么？

## Minimum Questions

Use these only after the scenario is known:

1. What are the 2-3 most common project types the team runs in this scenario?
2. Where do projects most often break: unclear input, slow decision, handoff loss, version chaos, quality review, delivery delay, or no复盘?
3. Who currently owns intake, planning, execution, review, client/stakeholder communication, and final decision?
4. What artifacts already exist: briefs, plans, dashboards, meeting notes, decks, reports, tickets, SOPs, source files?
5. Which tools are already used: Feishu/Lark, Notion, GitHub, Jira, Excel, shared drive, Slack/IM, local folders, or custom systems?
6. What does "project done" mean: delivered, accepted, paid, launched, reviewed, archived, or turned into reusable knowledge?

## Deep-Dive Questions By Dimension

### Project Boundary

- Is the system for one team, multiple teams, or external collaborators too?
- Does it manage pre-sale/sales work, delivery work, internal operations, or the full chain?
- Are projects short-cycle repeated work or long-cycle complex work?
- Does the same project produce client-facing artifacts, internal plans, data outputs, code, content, or operational actions?

### Intake And Scoping

- Where does a new request enter?
- What minimum information must exist before work starts?
- Who can reject, pause, or re-scope a request?
- What often gets assumed but later causes rework?

### Roles And Decision

- Which person is overloaded today?
- Which decisions are reversible and which need explicit approval?
- Who can decide scope, KPI, resource, delivery quality, and验收?
- Which responsibilities are currently hidden inside "project owner"?

### Deliverables And Quality

- What are the recurring deliverables?
- Which deliverables need independent review before being sent or released?
- What evidence proves a deliverable is reliable?
- Which output type has the most version confusion?

### Rhythm And Handoff

- Which meetings already exist?
- Which meetings produce decisions, and which only produce discussion?
- What should be updated after every meeting?
- Where do handoffs happen: sales to delivery, strategy to execution, data to reporting, design to engineering, project to operations, delivery to archive?

### Source, Version, And口径

- Do projects rely on many source files, client materials, data exports, or changing references?
- Is there a current "active version" for each deliverable?
- Are metrics, terminology, scope, and assumptions aligned across documents?
- What is the rule for accepting a new source into formal conclusions?

### Knowledge Backflow

- What should be reusable after a project ends?
- Does the team need cases, SOPs, templates, failure lessons, benchmark data, or decision records?
- Who is responsible for turning a project into reusable knowledge?
- How soon after closure should backflow happen?

## Pain -> Mechanism Mapping

| Pain | Usually Needed |
| --- | --- |
| Work starts with vague requests | Intake card, qualification gate, missing-info list |
| People disagree about scope | Scope freeze, change log, decision owner |
| Handoff depends on memory | Handoff package, stage state, required evidence |
| Many files, no truth source | Project control page, active-version index, source register |
| Metrics or terms conflict |口径 alignment table, metric owner, freeze card |
| Review happens too late | Node gate, deliverable checklist, independent review |
| One owner does everything | Role slots, RACI matrix, overload warning |
| Project ends with no learning | Closure package, retrospective, knowledge backflow card |
| Old projects are messy | Rescue sequence: navigation, source register, version timeline,口径 table, archive |

## Project Type Presets

### Client Delivery / Consulting

Common lifecycle:

`lead/intake -> diagnosis -> proposal/plan -> kickoff -> delivery -> review/reporting -> acceptance -> archive/backflow`

High-risk gates:

- Scope and expectation freeze.
- Client material and source verification.
- Proposal or report review.
- Acceptance evidence and dispute handling.

### Product / R&D

Common lifecycle:

`problem intake -> requirement shaping -> design -> build -> test -> release -> observe -> retrospective`

High-risk gates:

- Problem and success metric alignment.
- Requirement acceptance criteria.
- Release readiness.
- Incident and learning backflow.

### Operations / Content / Campaign

Common lifecycle:

`theme/request -> plan -> asset preparation -> execution -> monitoring -> optimization -> report -> asset reuse`

High-risk gates:

- Asset readiness.
- Launch checklist.
- Monitoring and change response.
- Reusable playbook extraction.

### Data / AI Project

Common lifecycle:

`use case intake -> data/source check -> baseline -> solution design -> build/run -> evaluation -> deployment/use -> monitoring/backflow`

High-risk gates:

- Data/source permission and reliability.
- Evaluation metric definition.
- Model/output review.
- Human decision boundary.

### Sales-To-Delivery Chain

Common lifecycle:

`opportunity -> pre-sale diagnosis -> proposal -> quote/scope -> contract/handoff -> kickoff -> delivery -> acceptance/settlement -> case backflow`

High-risk gates:

- Sales promise to delivery translation.
- Contract impact summary.
- Handoff package.
- Acceptance and settlement status tracking.
