# Vocabulary: 日本語 (ja)

Language: Japanese · Native name: 日本語 · Code: ja

Same keys, English column and `{placeholders}` as `en.md`. Render template headings and labels by looking them up in the English column. Values joined by ` / ` in `phrase.none` and `ref.joiners` are alternatives.

## Conventions

- Numbers: `1,234.5`; units after the number without a space for Japanese units (`10秒`, `500ミリ秒`) and with a space for SI symbols (`500 ms`, `2.5 GB`).
- Dates: ISO `2026-10-05` in metadata and tables; `2026年10月5日` in running text; the SDD byline stays `Oct 5, 2026`.
- Style: plain form (である調) for technical documents; full-width punctuation `、。` in prose, half-width for code and numbers.
- Quotation marks: `「…」` in prose; UI strings are quoted exactly as shown on screen.
- Keep established technical terms in katakana or English (トランザクション, webhook); put code names in backticks.

## Terms

| Key | English | 日本語 |
| --- | --- | --- |
| meta.status | Status | ステータス |
| meta.updated | Updated | 更新日 |
| meta.depends_on | Depends on | 依存 |
| meta.main_readers | Main readers | 主な読者 |
| meta.related | Related | 関連 |
| meta.date | Date | 日付 |
| meta.source | Source | 出典 |
| meta.accompanies | Accompanies | 付随文書 |
| meta.original_sdd | original SDD | 元のSDD |
| meta.alert | Alert | アラート |
| meta.dashboard | Dashboard | ダッシュボード |
| heading.open_questions | Open questions | 未解決の質問 |
| phrase.none | None. | なし。 |
| ref.section | section {n} | {n} 節 |
| ref.joiners | and / or / to | と / または / から / まで |
| dr.title | Decision Register | 意思決定記録簿 |
| dr.how_to_use | How to use | 使い方 |
| dr.log | Decision log | 決定ログ |
| dr.by_impact | Summary by impact | 影響度別まとめ |
| dr.blocks | Blocks {phase} | {phase} をブロック |
| dr.proposed | Proposed | 提案 |
| dr.decided | Decided | 決定 |
| dr.changed | Changed | 変更 |
| dr.problem | Problem | 問題 |
| dr.options | Options | 選択肢 |
| dr.decision | Decision | 決定内容 |
| dr.consequences | Consequences | 影響 |
| dr.write_to | Write to | 反映先 |
| dr.deviates | deviates from the original SDD | 元のSDDと異なる |
| dr.spike | spike | スパイク |
| dr.owner | Owner | オーナー |
| dr.delegated | Claude (delegated by Owner) | Claude（オーナーから委任） |
| dr.accept_rest | Accept all remaining proposals | 残りの提案をすべて承認 |
| dr.revised | Revised {date} | {date} 改訂 |
| plan.title | Master Plan: building {project} end to end | マスタープラン：{project} の構築（最初から最後まで） |
| plan.how_to_use | How to use this document | 本書の使い方 |
| plan.language | Language | 言語 |
| plan.analysis | Analysis of the original SDD | 元のSDDの分析 |
| plan.keep | What is already good and stays | 良い点（そのまま維持） |
| plan.gaps | Main gaps | 主なギャップ |
| plan.adjustments | Adjustments to the plan in the original SDD | 元のSDDの計画からの調整 |
| plan.principles | Working principles | 実施原則 |
| plan.docs | Documents to write | 作成するドキュメント |
| plan.tree | The docs/ tree | docs/ ディレクトリ構成 |
| plan.required | Required content of each document | 各ドキュメントの必須内容 |
| plan.approved_def | Definition of "Approved" for a document | ドキュメントの「Approved」の定義 |
| plan.use_cases | Use cases to write | 作成するユースケース一覧 |
| plan.roadmap | Roadmap | ロードマップ |
| plan.phase_overview | Phase overview | フェーズ概要 |
| plan.phase_deps | Phase dependencies | フェーズ間の依存関係 |
| plan.cut_order | Cut order when time runs short | 時間不足時の削減順序 |
| plan.tasks | Tasks per phase | フェーズ別タスク詳細 |
| plan.phase | Phase {n}: {name} | フェーズ {n}：{name} |
| plan.goal | Goal | 目標 |
| plan.exit | Exit criteria ({milestone}) | 完了条件（{milestone}） |
| plan.reached | {milestone} reached on {date}. | {milestone} は {date} に達成。 |
| plan.trace | Traceability matrix | トレーサビリティマトリクス |
| plan.conventions | Working conventions | 作業規約 |
| plan.dor | Definition of Ready | Definition of Ready |
| plan.dod | Definition of Done | Definition of Done |
| plan.git | Git and code | Git とコード |
| plan.risks | Additional risks (beyond the original SDD) | 追加リスク（元のSDD以外） |
| plan.first_tasks | Start now: the first 10 tasks | すぐに着手：最初の10タスク |
| plan.templates | Appendix A: Shared templates | 付録A：共通テンプレート |
| plan.vocabulary | Appendix B: Vocabulary | 付録B：用語集（語彙） |
| plan.done | Done {date} | {date} 完了 |
| plan.total | Total | 合計 |
| readme.title | Project documentation: {project} | プロジェクトドキュメント：{project} |
| readme.start_here | Start here | はじめに |
| readme.documents | Documents | ドキュメント |
| readme.structure | Structure | 構成 |
| readme.conventions | Conventions | 規約 |
| readme.not_written | Not written | 未作成 |
| col.id | ID | ID |
| col.task | Task | タスク |
| col.output | Output and acceptance | 成果物と受け入れ基準 |
| col.depends | Depends on | 依存 |
| col.documents | Documents | ドキュメント |
| col.document | Document | ドキュメント |
| col.gate | Gate | ゲート |
| col.required | Required content | 必須内容 |
| col.estimate | Estimate (1 person, full time) | 見積もり（1人・フルタイム） |
| col.milestone | Milestone | マイルストーン |
| col.requirement | Requirement | 要件 |
| col.design_docs | Design documents | 設計ドキュメント |
| col.tasks | Tasks | タスク |
| col.verification | Verification | 検証方法 |
| col.priority | Priority | 優先度 |
| col.acceptance | Acceptance criteria | 受け入れ基準 |
| col.target | Target | 目標値 |
| col.how_measured | How measured | 測定方法 |
| col.risk | Risk | リスク |
| col.early_sign | Early sign | 早期兆候 |
| col.mitigation | Mitigation | 対応 |
| col.impact | Impact | 影響 |
| col.scenario | Scenario | シナリオ |
| col.expected | Expected | 期待結果 |
| col.term | Term | 用語 |
| col.local_name | Local name | 日本語名 |
| col.definition | Definition | 定義 |
| col.key | Key | キー |
| col.type | Type | 型 |
| col.default | Default | デフォルト |
| col.description | Description | 説明 |
| col.metric | Metric | メトリクス |
| col.label | Label | ラベル |
| col.situation | Situation | 状況 |
| col.behavior | Behavior | 動作 |
| col.from | From | 遷移元 |
| col.to | To | 遷移先 |
| col.triggered_by | Triggered by | トリガー |
| col.module | Module | モジュール |
| col.role | Role | 役割 |
| col.investment | Investment level | 投資レベル |
| col.item | Item | 項目 |
| col.handled_now | How this phase handles it | 本フェーズでの扱い |
| col.failure | Failure | 障害 |
| col.detection | Detection | 検知 |
| col.system_behavior | System behavior | システムの動作 |
| col.recovery | Recovery | 復旧 |
| col.object | Object | 対象 |
| col.invariant | Invariant | 不変条件 |
| col.enforced_by | Enforced by | 強制手段 |
| col.experiment | Experiment | 実験 |
| col.method | Method | 方法 |
| col.metrics | Metrics | 指標 |
| col.stage | Stage | 段階 |
| col.content | Content | 内容 |
| col.results | Results | 成果 |
| col.date | Date | 日付 |
| col.decided_by | Decided by | 決定者 |
| col.affected | Affected items | 影響を受ける項目 |
| col.level | Level | レベル |
| col.reason | Reason | 理由 |
| col.participant | Participant | 参加者 |
| col.kind | Kind | 種別 |
| col.code | Code | コード |
| col.defined_in | Defined in | 定義元 |
| col.step | Step | ステップ |
| col.from_to | From → To | 送信元 → 送信先 |
| col.call | Call | 呼び出し |
| col.data | Data | データ |
| col.rules_checks | Rules and checks | ルールとチェック |
| col.error_handling | Error → handling | エラー → 処理 |
| col.http_problem | HTTP status / problem type | HTTP ステータス / problem type |
| col.ui_behavior | UI behavior and message | UI の動作とメッセージ |
| col.flow | Flow | フロー |
| col.screens | Screens | 画面 |
| col.endpoints | Endpoints | エンドポイント |
| col.file | File | ファイル |
| adr.title | ADR-{n}: {title} | ADR-{n}：{title} |
| adr.context | Context | 背景 |
| adr.options | Options considered | 検討した選択肢 |
| adr.decision | Decision | 決定 |
| adr.consequences | Consequences | 結果 |
| adr.positive | Positive | 良い影響 |
| adr.negative | Negative | 悪い影響 |
| adr.followups | Follow-up work | 派生タスク |
| uc.actor | Actor | アクター |
| uc.trigger | Trigger | トリガー |
| uc.preconditions | Preconditions | 事前条件 |
| uc.main_flow | Main flow | 基本フロー |
| uc.alt_flows | Alternative flows | 代替フロー |
| uc.error_flows | Error flows | 例外フロー |
| uc.postconditions | Postconditions | 事後条件 |
| uc.rules | Business rules | 業務ルール |
| uc.diagram | Use case overview | ユースケース全体図 |
| req.conventions | Conventions | 規約 |
| req.functional | Functional requirements | 機能要件 |
| req.non_functional | Non-functional requirements | 非機能要件 |
| req.matrix | FR → UC → feature → design matrix | FR → UC → 機能 → 設計 マトリクス |
| req.added | added | 追加 |
| ep.purpose | Purpose / UC | 目的 / UC |
| ep.auth | Authorization | 権限 |
| ep.params | Parameters | パラメータ |
| ep.response | Response | レスポンス |
| ep.errors | Errors | エラー |
| ep.data_source | Data source | データソース |
| ep.cache | Cache | キャッシュ |
| ep.performance | Performance | 性能 |
| ep.events | Related real-time events | 関連するリアルタイムイベント |
| scr.title | Screen: {name} | 画面：{name} |
| scr.persona | Persona, use cases, permissions | ペルソナ・ユースケース・権限 |
| scr.url | URL and search params | URL と検索パラメータ |
| scr.wireframe | Wireframe | ワイヤーフレーム |
| scr.regions | Regions and components | 領域とコンポーネント |
| scr.data | Data | データ |
| scr.interactions | Interactions | 操作 |
| scr.states | States | 状態 |
| scr.copy | Microcopy | マイクロコピー |
| scr.acceptance | Acceptance criteria | 受け入れ基準 |
| scr.e2e | E2E test cases | E2E テストケース |
| exp.hypothesis | Hypothesis | 仮説 |
| exp.variables | Variables | 変数 |
| exp.baseline | Baseline | ベースライン |
| exp.environment | Environment | 環境 |
| exp.steps | Steps | 手順 |
| exp.metrics | Metrics and formulas | 指標と計算式 |
| exp.pass | Pass criteria | 合格基準 |
| exp.analysis | Analysis | 分析 |
| exp.result_table | Result table template | 結果表のテンプレート |
| exp.threats | Threats to validity | 妥当性への脅威 |
| exp.results | Results | 結果 |
| rb.symptoms | Symptoms and impact | 症状と影響 |
| rb.checks | Checks | 確認 |
| rb.remediation | Remediation | 対処 |
| rb.on_env | On {environment} | {environment} の場合 |
| rb.verify | Confirm it is resolved | 解決の確認 |
| rb.prevention | Prevention and follow-up | 再発防止とフォローアップ |
| des.purpose | Purpose and scope | 目的と範囲 |
| des.components | Components and interfaces | コンポーネントとインターフェース |
| des.algorithm | Algorithm | アルゴリズム |
| des.concurrency | Transactions and concurrency | トランザクションと並行性 |
| des.config | Configuration | 設定 |
| des.metrics | Metrics and logs | メトリクスとログ |
| des.errors | Errors and handling | エラーと処理 |
| des.tests | Required tests | 必須テスト |
| des.not_here | Not in this document | 本書の対象外 |
| flow.index | Detailed flows | 詳細フロー |
| flow.title | Detailed flows: {area} | 詳細フロー: {area} |
| flow.screen | Screen | 画面 |
| flow.events | Events | イベント |
| flow.participants | Participants | 参加者 |
| flow.sequence | Sequence diagram | シーケンス図 |
| flow.steps | Step details | ステップ詳細 |
| persona.overview | Overview | 概要 |
| persona.goals | Goals | 目標 |
| persona.pains | Pain points | 課題 |
| persona.needs | Needs from {system} | {system} に求めること |
| persona.not_needed | Does not need | 不要なもの |
| persona.screens | Screens | 画面 |
| persona.journey | Journey | ジャーニー |
| sdd.title | {name} — System Design | {name} — システム設計 |
| sdd.intro | Introduction | はじめに |
| sdd.context | Context | 背景 |
| sdd.problems | Real-world problems | 現実の課題 |
| sdd.vision | Vision | ビジョン |
| sdd.goals | Goals, scope and focus | 目標・範囲・重点 |
| sdd.research_question | Research question | 研究課題 |
| sdd.core_problem | Core problem | 中核となる問題 |
| sdd.investment | Investment by module | モジュール別の投資レベル |
| sdd.scope | Scope | 範囲 |
| sdd.in_scope | In scope | 範囲内 |
| sdd.later | Later | 後回し |
| sdd.out_of_scope | Out of scope | 範囲外 |
| sdd.users | Users, use cases and requirements | ユーザー・ユースケース・要件 |
| sdd.user_groups | User groups | ユーザーグループ |
| sdd.use_cases | Use cases | ユースケース |
| sdd.fr | Functional requirements | 機能要件 |
| sdd.nfr | Non-functional requirements | 非機能要件 |
| sdd.architecture | Overall architecture and technology | 全体アーキテクチャと技術 |
| sdd.components | Components | 構成要素 |
| sdd.principles | Cross-cutting principles | 横断的な原則 |
| sdd.data_flow | Data flow | データフロー |
| sdd.technology | Technology | 技術 |
| sdd.data_model | Data model | データモデル |
| sdd.entities | Entities | エンティティ |
| sdd.constraints | Required constraints | 必須の制約 |
| sdd.api | Backend API | バックエンド API |
| sdd.endpoints | Endpoints | エンドポイント |
| sdd.conventions | Conventions | 規約 |
| sdd.ui | User interface | ユーザーインターフェース |
| sdd.screens | Screens | 画面 |
| sdd.ui_tech | Technical notes | 技術的事項 |
| sdd.ops | Deployment and fault tolerance | デプロイと耐障害性 |
| sdd.deployment | Deployment | デプロイ |
| sdd.failures | Behavior under failure | 障害時の動作 |
| sdd.invariant_checks | Invariant checks | 不変条件のチェック |
| sdd.security | Minimum security | 最低限のセキュリティ |
| sdd.testing | Testing and evaluation | テストと評価 |
| sdd.test_strategy | Test strategy | テスト戦略 |
| sdd.experiments | Experiments | 実験 |
| sdd.plan | Implementation plan | 実装計画 |
| sdd.demo | Demo script | デモシナリオ |
| sdd.risks | Risks and limitations | リスクと制約 |
| sdd.open_points | Open points | 未決事項 |
| sdd.repo | Appendix: Repository layout | 付録：リポジトリ構成 |
| sdd.alternatives | {problem}: options and rationale | {problem}：選択肢と選定理由 |
| sdd.option | Option {x}: {name} | 案 {x}：{name} |
| sdd.chosen | chosen | 採用 |
| sdd.pros | Pros | 長所 |
| sdd.cons | Cons | 短所 |
| sdd.verdict | Verdict | 結論 |
| sdd.comparison | Comparison and rationale | 比較と選定理由 |
| sdd.parameters | Parameters | パラメータ |
| sdd.text_version | Text version of the figure above, for Markdown export | 上図のテキスト版（Markdown 出力用） |
