# Vocabulary: 简体中文 (zh)

Language: Chinese (Simplified) · Native name: 简体中文 · Code: zh

Same keys, English column and `{placeholders}` as `en.md`. Render template headings and labels by looking them up in the English column. Values joined by ` / ` in `phrase.none` and `ref.joiners` are alternatives.

## Conventions

- Numbers: `1,234.5`; SI units after a space (`500 ms`, `2.5 GB`), Chinese units without a space (`10秒`).
- Dates: ISO `2026-10-05` in metadata and tables; `2026年10月5日` in running text; the SDD byline stays `Oct 5, 2026`.
- Punctuation: full-width `，。：；（）` in prose, half-width in code; put a space between Chinese and Latin words or numbers.
- Quotation marks: `“…”` in prose; UI strings are quoted exactly as shown on screen.
- Keep established English technical terms when the Chinese term is uncommon; put code names in backticks.

## Terms

| Key | English | 简体中文 |
| --- | --- | --- |
| meta.status | Status | 状态 |
| meta.updated | Updated | 更新 |
| meta.depends_on | Depends on | 依赖 |
| meta.main_readers | Main readers | 主要读者 |
| meta.related | Related | 相关 |
| meta.date | Date | 日期 |
| meta.source | Source | 来源 |
| meta.accompanies | Accompanies | 配套文档 |
| meta.original_sdd | original SDD | 原始 SDD |
| meta.alert | Alert | 告警 |
| meta.dashboard | Dashboard | 仪表盘 |
| heading.open_questions | Open questions | 待解决问题 |
| phrase.none | None. | 无。 |
| ref.section | section {n} | 第 {n} 节 |
| ref.joiners | and / or / to | 和 / 或 / 至 / 到 |
| dr.title | Decision Register | 决策登记簿 |
| dr.how_to_use | How to use | 使用方法 |
| dr.log | Decision log | 决策日志 |
| dr.by_impact | Summary by impact | 按影响汇总 |
| dr.blocks | Blocks {phase} | 阻塞 {phase} |
| dr.proposed | Proposed | 提议 |
| dr.decided | Decided | 已定 |
| dr.changed | Changed | 已改 |
| dr.problem | Problem | 问题 |
| dr.options | Options | 可选方案 |
| dr.decision | Decision | 决定 |
| dr.consequences | Consequences | 影响 |
| dr.write_to | Write to | 写入 |
| dr.deviates | deviates from the original SDD | 偏离原始 SDD |
| dr.spike | spike | 技术验证 |
| dr.owner | Owner | 负责人 |
| dr.delegated | Claude (delegated by Owner) | Claude（负责人授权） |
| dr.accept_rest | Accept all remaining proposals | 接受其余全部提议 |
| dr.revised | Revised {date} | {date} 修订 |
| plan.title | Master Plan: building {project} end to end | 总体计划：从头到尾构建 {project} |
| plan.how_to_use | How to use this document | 本文档使用方法 |
| plan.language | Language | 语言 |
| plan.analysis | Analysis of the original SDD | 原始 SDD 分析 |
| plan.keep | What is already good and stays | 已经做得好、保持不变的部分 |
| plan.gaps | Main gaps | 主要缺口 |
| plan.adjustments | Adjustments to the plan in the original SDD | 对原始 SDD 计划的调整 |
| plan.principles | Working principles | 实施原则 |
| plan.docs | Documents to write | 需要编写的文档 |
| plan.tree | The docs/ tree | docs/ 目录结构 |
| plan.required | Required content of each document | 各文档的必备内容 |
| plan.approved_def | Definition of "Approved" for a document | 文档“Approved”的定义 |
| plan.use_cases | Use cases to write | 需要编写的用例 |
| plan.roadmap | Roadmap | 路线图 |
| plan.phase_overview | Phase overview | 阶段概览 |
| plan.phase_deps | Phase dependencies | 阶段依赖 |
| plan.cut_order | Cut order when time runs short | 时间不足时的削减顺序 |
| plan.tasks | Tasks per phase | 各阶段任务详情 |
| plan.phase | Phase {n}: {name} | 阶段 {n}：{name} |
| plan.goal | Goal | 目标 |
| plan.exit | Exit criteria ({milestone}) | 退出标准（{milestone}） |
| plan.reached | {milestone} reached on {date}. | {milestone} 于 {date} 达成。 |
| plan.trace | Traceability matrix | 追溯矩阵 |
| plan.conventions | Working conventions | 工作约定 |
| plan.dor | Definition of Ready | Definition of Ready |
| plan.dod | Definition of Done | Definition of Done |
| plan.git | Git and code | Git 与代码 |
| plan.risks | Additional risks (beyond the original SDD) | 补充风险（原始 SDD 之外） |
| plan.first_tasks | Start now: the first 10 tasks | 立即开始：前 10 项任务 |
| plan.templates | Appendix A: Shared templates | 附录 A：通用模板 |
| plan.vocabulary | Appendix B: Vocabulary | 附录 B：词汇表 |
| plan.done | Done {date} | {date} 完成 |
| plan.total | Total | 合计 |
| readme.title | Project documentation: {project} | 项目文档：{project} |
| readme.start_here | Start here | 从这里开始 |
| readme.documents | Documents | 文档 |
| readme.structure | Structure | 结构 |
| readme.conventions | Conventions | 约定 |
| readme.not_written | Not written | 未编写 |
| col.id | ID | ID |
| col.task | Task | 任务 |
| col.output | Output and acceptance | 产出与验收标准 |
| col.depends | Depends on | 依赖 |
| col.documents | Documents | 文档 |
| col.document | Document | 文档 |
| col.gate | Gate | 关卡 |
| col.required | Required content | 必备内容 |
| col.estimate | Estimate (1 person, full time) | 估算（1 人，全职） |
| col.milestone | Milestone | 里程碑 |
| col.requirement | Requirement | 需求 |
| col.design_docs | Design documents | 设计文档 |
| col.tasks | Tasks | 任务 |
| col.verification | Verification | 验证方式 |
| col.priority | Priority | 优先级 |
| col.acceptance | Acceptance criteria | 验收标准 |
| col.target | Target | 指标 |
| col.how_measured | How measured | 测量方法 |
| col.risk | Risk | 风险 |
| col.early_sign | Early sign | 早期信号 |
| col.mitigation | Mitigation | 应对措施 |
| col.impact | Impact | 影响 |
| col.scenario | Scenario | 场景 |
| col.expected | Expected | 预期结果 |
| col.term | Term | 术语 |
| col.local_name | Local name | 中文名 |
| col.definition | Definition | 定义 |
| col.key | Key | 键 |
| col.type | Type | 类型 |
| col.default | Default | 默认值 |
| col.description | Description | 说明 |
| col.metric | Metric | 指标 |
| col.label | Label | 标签 |
| col.situation | Situation | 情况 |
| col.behavior | Behavior | 行为 |
| col.from | From | 起始 |
| col.to | To | 目标 |
| col.triggered_by | Triggered by | 触发方 |
| col.module | Module | 模块 |
| col.role | Role | 角色 |
| col.investment | Investment level | 投入程度 |
| col.item | Item | 事项 |
| col.handled_now | How this phase handles it | 本阶段如何处理 |
| col.failure | Failure | 故障 |
| col.detection | Detection | 发现方式 |
| col.system_behavior | System behavior | 系统行为 |
| col.recovery | Recovery | 恢复 |
| col.object | Object | 对象 |
| col.invariant | Invariant | 不变量 |
| col.enforced_by | Enforced by | 保证手段 |
| col.experiment | Experiment | 实验 |
| col.method | Method | 方法 |
| col.metrics | Metrics | 指标 |
| col.stage | Stage | 阶段 |
| col.content | Content | 内容 |
| col.results | Results | 产出 |
| col.date | Date | 日期 |
| col.decided_by | Decided by | 决定人 |
| col.affected | Affected items | 受影响项 |
| col.level | Level | 级别 |
| col.reason | Reason | 原因 |
| adr.title | ADR-{n}: {title} | ADR-{n}：{title} |
| adr.context | Context | 背景 |
| adr.options | Options considered | 考虑过的方案 |
| adr.decision | Decision | 决定 |
| adr.consequences | Consequences | 后果 |
| adr.positive | Positive | 正面 |
| adr.negative | Negative | 负面 |
| adr.followups | Follow-up work | 后续工作 |
| uc.actor | Actor | 参与者 |
| uc.trigger | Trigger | 触发条件 |
| uc.preconditions | Preconditions | 前置条件 |
| uc.main_flow | Main flow | 主流程 |
| uc.alt_flows | Alternative flows | 备选流程 |
| uc.error_flows | Error flows | 异常流程 |
| uc.postconditions | Postconditions | 后置条件 |
| uc.rules | Business rules | 业务规则 |
| uc.diagram | Use case overview | 用例总览 |
| req.conventions | Conventions | 约定 |
| req.functional | Functional requirements | 功能需求 |
| req.non_functional | Non-functional requirements | 非功能需求 |
| req.matrix | FR → UC → feature → design matrix | FR → UC → 功能 → 设计 矩阵 |
| req.added | added | 新增 |
| ep.purpose | Purpose / UC | 目的 / UC |
| ep.auth | Authorization | 权限 |
| ep.params | Parameters | 参数 |
| ep.response | Response | 响应 |
| ep.errors | Errors | 错误 |
| ep.data_source | Data source | 数据来源 |
| ep.cache | Cache | 缓存 |
| ep.performance | Performance | 性能 |
| ep.events | Related real-time events | 相关实时事件 |
| scr.title | Screen: {name} | 页面：{name} |
| scr.persona | Persona, use cases, permissions | 角色画像、用例、权限 |
| scr.url | URL and search params | URL 与查询参数 |
| scr.wireframe | Wireframe | 线框图 |
| scr.regions | Regions and components | 区域与组件 |
| scr.data | Data | 数据 |
| scr.interactions | Interactions | 交互 |
| scr.states | States | 状态 |
| scr.copy | Microcopy | 界面文案 |
| scr.acceptance | Acceptance criteria | 验收标准 |
| scr.e2e | E2E test cases | E2E 测试用例 |
| exp.hypothesis | Hypothesis | 假设 |
| exp.variables | Variables | 变量 |
| exp.baseline | Baseline | 基线 |
| exp.environment | Environment | 环境 |
| exp.steps | Steps | 步骤 |
| exp.metrics | Metrics and formulas | 指标与公式 |
| exp.pass | Pass criteria | 通过标准 |
| exp.analysis | Analysis | 分析 |
| exp.result_table | Result table template | 结果表模板 |
| exp.threats | Threats to validity | 有效性威胁 |
| exp.results | Results | 结果 |
| rb.symptoms | Symptoms and impact | 症状与影响 |
| rb.checks | Checks | 检查 |
| rb.remediation | Remediation | 处理 |
| rb.on_env | On {environment} | 在 {environment} 上 |
| rb.verify | Confirm it is resolved | 确认已解决 |
| rb.prevention | Prevention and follow-up | 预防与后续 |
| des.purpose | Purpose and scope | 目的与范围 |
| des.components | Components and interfaces | 组件与接口 |
| des.algorithm | Algorithm | 算法 |
| des.concurrency | Transactions and concurrency | 事务与并发 |
| des.config | Configuration | 配置 |
| des.metrics | Metrics and logs | 指标与日志 |
| des.errors | Errors and handling | 错误与处理 |
| des.tests | Required tests | 必备测试 |
| des.not_here | Not in this document | 不在本文档范围内 |
| persona.overview | Overview | 概览 |
| persona.goals | Goals | 目标 |
| persona.pains | Pain points | 痛点 |
| persona.needs | Needs from {system} | 对 {system} 的需求 |
| persona.not_needed | Does not need | 不需要 |
| persona.screens | Screens | 页面 |
| persona.journey | Journey | 用户旅程 |
| sdd.title | {name} — System Design | {name} — 系统设计 |
| sdd.intro | Introduction | 引言 |
| sdd.context | Context | 背景 |
| sdd.problems | Real-world problems | 现实问题 |
| sdd.vision | Vision | 愿景 |
| sdd.goals | Goals, scope and focus | 目标、范围与重点 |
| sdd.research_question | Research question | 研究问题 |
| sdd.core_problem | Core problem | 核心问题 |
| sdd.investment | Investment by module | 各模块投入程度 |
| sdd.scope | Scope | 范围 |
| sdd.in_scope | In scope | 范围内 |
| sdd.later | Later | 以后再做 |
| sdd.out_of_scope | Out of scope | 范围外 |
| sdd.users | Users, use cases and requirements | 用户、用例与需求 |
| sdd.user_groups | User groups | 用户群体 |
| sdd.use_cases | Use cases | 用例 |
| sdd.fr | Functional requirements | 功能需求 |
| sdd.nfr | Non-functional requirements | 非功能需求 |
| sdd.architecture | Overall architecture and technology | 总体架构与技术 |
| sdd.components | Components | 组成部分 |
| sdd.principles | Cross-cutting principles | 贯穿原则 |
| sdd.data_flow | Data flow | 数据流 |
| sdd.technology | Technology | 技术 |
| sdd.data_model | Data model | 数据模型 |
| sdd.entities | Entities | 实体 |
| sdd.constraints | Required constraints | 必备约束 |
| sdd.api | Backend API | 后端 API |
| sdd.endpoints | Endpoints | 接口 |
| sdd.conventions | Conventions | 约定 |
| sdd.ui | User interface | 用户界面 |
| sdd.screens | Screens | 页面 |
| sdd.ui_tech | Technical notes | 技术要点 |
| sdd.ops | Deployment and fault tolerance | 部署与容错 |
| sdd.deployment | Deployment | 部署 |
| sdd.failures | Behavior under failure | 故障时的行为 |
| sdd.invariant_checks | Invariant checks | 不变量检查 |
| sdd.security | Minimum security | 基本安全 |
| sdd.testing | Testing and evaluation | 测试与评估 |
| sdd.test_strategy | Test strategy | 测试策略 |
| sdd.experiments | Experiments | 实验 |
| sdd.plan | Implementation plan | 实施计划 |
| sdd.demo | Demo script | 演示脚本 |
| sdd.risks | Risks and limitations | 风险与局限 |
| sdd.open_points | Open points | 未决事项 |
| sdd.repo | Appendix: Repository layout | 附录：仓库结构 |
| sdd.alternatives | {problem}: options and rationale | {problem}：方案与选择理由 |
| sdd.option | Option {x}: {name} | 方案 {x}：{name} |
| sdd.chosen | chosen | 选用 |
| sdd.pros | Pros | 优点 |
| sdd.cons | Cons | 缺点 |
| sdd.verdict | Verdict | 结论 |
| sdd.comparison | Comparison and rationale | 对比与选择理由 |
| sdd.parameters | Parameters | 参数 |
| sdd.text_version | Text version of the figure above, for Markdown export | 上图的文字版本（用于导出 Markdown） |
