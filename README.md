# Team Workflow System Builder

把团队已经接受的工作方式，转化为可运行、可治理、可验证、可迁移的数字化协作系统，并只在边界清晰、安全可验的节点加入 AI 协助或执行。

这是一个面向 Codex 的开源 Skill。它适合团队流程线上化、项目工作区治理、流程仓库审计与修复、角色与门禁设计、版本和信源管理、AI 工作边界设计，以及成熟流程的复用打包。

## 它解决什么问题

许多团队的流程散落在口头约定、文档、聊天记录、模板和个人经验里。直接叠加自动化或 AI，往往会放大职责不清、状态失真、版本混乱和审批失控。

本 Skill 提供一条更稳健的转换路径：

```text
已接受的工作方式
  -> 显式化与结构化
  -> 在合适的本地、共享仓库、协作工具或平台上运行
  + 与风险相称的治理
  + 仅在可验证边界内加入 AI
```

## 核心能力

- 恢复 AS-IS 实际工作流，并区分正式规则、真实做法、历史偶然和未决问题。
- 建立项目、阶段、工作项、角色、信源、产物、版本、门禁、审批和异常处理模型。
- 分别记录表达结构、执行载体、治理程度、AI 覆盖和实际采用证据。
- 为复杂工作识别合适的专业能力，同时保留统一的流程治理结果。
- 分离“建设系统时的专业能力路由”与“目标工作流上线后的工作项/Skill 调度”，避免把候选 Skill 误报成已安装能力。
- 对启用 AI 的目标流程建立完整工作项清单：每项必须明确为运行期路由或人工排除，并保留验证、失败回退与状态写回。
- 创建文件型母系统和项目工作区，并验证注册表、项目状态、版本和审批数据的一致性。
- 安全审计、修复、迁移、归档并打包已经验证的工作流系统。
- 防止把业务决策、人类审批或外部发布误当作 AI 可以自行完成的动作。

## 安装

```bash
git clone https://github.com/zhongky1995/team-workflow-system-builder.git
mkdir -p ~/.codex/skills
cp -R team-workflow-system-builder/skills/team-workflow-system-builder ~/.codex/skills/
```

重新打开 Codex 会话后，可用自然语言触发，例如：

- “把我们现有的团队协作流程整理成一个可运行的数字化系统。”
- “审计并修复这个项目管理仓库，但不要改变业务方法。”
- “为这个流程设计项目工作区、阶段状态、Gate 和版本规则。”
- “判断哪些工作节点适合 AI 辅助，哪些必须由人审批。”

## 快速使用

创建一个新的文件型母系统：

```bash
python3 ~/.codex/skills/team-workflow-system-builder/scripts/create_system.py \
  /path/to/my-workflow-system \
  --profile standard
```

创建并登记一个正式项目：

```bash
python3 ~/.codex/skills/team-workflow-system-builder/scripts/create_project.py \
  /path/to/my-workflow-system \
  --id PRJ-2026-001 \
  --name "示例项目" \
  --workspace /path/to/projects
```

验证母系统和项目：

```bash
python3 ~/.codex/skills/team-workflow-system-builder/scripts/validate_workflow_system.py \
  /path/to/my-workflow-system \
  --project /path/to/projects/PRJ-2026-001-示例项目
```

脚本默认不会擅自创建 Git 历史。需要初始化项目 Git 仓库时，请在 `create_project.py` 命令中显式加入 `--init-git`。

## 目录结构

```text
skills/team-workflow-system-builder/
├── SKILL.md                 # Skill 的核心边界与执行协议
├── agents/                  # Codex 展示与调用元数据
├── assets/templates/        # 母系统与项目工作区模板
├── references/              # 按任务路由的治理参考资料
├── scripts/                 # 创建、验证、基线和打包工具
├── tests/                   # 回归测试
└── evals/                   # 行为评测用例
```

## 设计原则

- 保留已接受的业务语义，不为补齐系统而虚构规则。
- 人类的政策、授权、审批、发布和外部承诺仍由人类负责。
- 先让流程与状态可运行，再为合适节点增加 AI。
- 所有目标工作项都应有明确去向，但不要求每个阶段或工作项都拆成独立 Skill。
- 一个可治理的本地或文件型系统也是有效结果，不强迫所有团队平台化。
- 通过小范围试点、验证证据和可回滚基线推进迁移。

## 开发与验证

运行回归测试：

```bash
python3 -m unittest discover \
  -s skills/team-workflow-system-builder/tests \
  -v
```

检查专业能力路由表：

```bash
python3 skills/team-workflow-system-builder/scripts/validate_specialist_routing_registry.py \
  skills/team-workflow-system-builder/references/specialist-routing-registry.json
```

当前发布版本：`0.7.0`。

`0.7.0` 新增目标运行期调度契约、`ai-work-item-dispatch.json` 模板，以及完整工作项覆盖、人工决策保护和选定能力安装状态的机器校验。结构校验只证明契约完整，不等于真实团队已经采用。

## License

[MIT License](LICENSE)
