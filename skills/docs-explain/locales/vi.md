# Vocabulary: Tiếng Việt (vi)

Language: Vietnamese · Native name: Tiếng Việt · Code: vi

Same keys, English column and `{placeholders}` as `en.md`. Render template headings and labels by looking them up in the English column. Values joined by ` / ` in `phrase.none` and `ref.joiners` are alternatives.

## Conventions

- Numbers: `1.234,5` (dot for thousands, comma for decimals); units after a space (`10 giây`, `500 ms`, `2,5 GB`).
- Dates: ISO `2026-10-05` in metadata and tables; the SDD byline stays `Oct 5, 2026`.
- Quotation marks: `"…"`. UI strings are quoted exactly as shown on screen, usually in English.
- Keep established English technical terms when the Vietnamese one is awkward (reservation, webhook, consumer lag, chunk); put code names in backticks.
- Register: short active sentences; avoid hedges such as "có thể cân nhắc", "nên xem xét"; no marketing words.

## Terms

| Key | English | Tiếng Việt |
| --- | --- | --- |
| meta.status | Status | Trạng thái |
| meta.updated | Updated | Cập nhật |
| meta.depends_on | Depends on | Phụ thuộc |
| meta.main_readers | Main readers | Người dùng chính |
| meta.related | Related | Liên quan |
| meta.date | Date | Ngày |
| meta.source | Source | Nguồn |
| meta.accompanies | Accompanies | Đi kèm |
| meta.original_sdd | original SDD | SDD gốc |
| meta.alert | Alert | Alert |
| meta.dashboard | Dashboard | Dashboard |
| heading.open_questions | Open questions | Câu hỏi còn mở |
| phrase.none | None. | Không có. / Không còn. |
| ref.section | section {n} | mục {n} |
| ref.joiners | and / or / to | và / hoặc / đến / tới |
| dr.title | Decision Register | Sổ quyết định mở |
| dr.how_to_use | How to use | Cách dùng |
| dr.log | Decision log | Nhật ký chốt |
| dr.by_impact | Summary by impact | Tổng hợp theo mức ảnh hưởng |
| dr.blocks | Blocks {phase} | Chặn {phase} |
| dr.proposed | Proposed | Đề xuất |
| dr.decided | Decided | Chốt |
| dr.changed | Changed | Đổi |
| dr.problem | Problem | Vấn đề |
| dr.options | Options | Các phương án |
| dr.decision | Decision | Quyết định |
| dr.consequences | Consequences | Hệ quả |
| dr.write_to | Write to | Ghi vào |
| dr.deviates | deviates from the original SDD | lệch SDD gốc |
| dr.spike | spike | spike |
| dr.owner | Owner | Owner |
| dr.delegated | Claude (delegated by Owner) | Claude (Owner ủy quyền) |
| dr.accept_rest | Accept all remaining proposals | Chấp nhận toàn bộ các đề xuất còn lại |
| dr.revised | Revised {date} | Sửa {date} |
| plan.title | Master Plan: building {project} end to end | Master Plan: xây dựng {project} từ đầu đến cuối |
| plan.how_to_use | How to use this document | Cách dùng tài liệu này |
| plan.language | Language | Ngôn ngữ |
| plan.analysis | Analysis of the original SDD | Phân tích SDD gốc |
| plan.keep | What is already good and stays | Những gì đã tốt, giữ nguyên |
| plan.gaps | Main gaps | Khoảng trống chính |
| plan.adjustments | Adjustments to the plan in the original SDD | Điều chỉnh so với kế hoạch trong SDD gốc |
| plan.principles | Working principles | Nguyên tắc thực hiện |
| plan.docs | Documents to write | Bộ tài liệu cần viết |
| plan.tree | The docs/ tree | Cây thư mục docs/ |
| plan.required | Required content of each document | Nội dung bắt buộc của từng tài liệu |
| plan.approved_def | Definition of "Approved" for a document | Định nghĩa "Approved" cho một tài liệu |
| plan.use_cases | Use cases to write | Danh sách use case cần viết |
| plan.roadmap | Roadmap | Lộ trình |
| plan.phase_overview | Phase overview | Tổng quan các phase |
| plan.phase_deps | Phase dependencies | Phụ thuộc giữa các phase |
| plan.cut_order | Cut order when time runs short | Thứ tự cắt giảm khi thiếu thời gian |
| plan.tasks | Tasks per phase | Chi tiết công việc từng phase |
| plan.phase | Phase {n}: {name} | Phase {n}: {name} |
| plan.goal | Goal | Mục tiêu |
| plan.exit | Exit criteria ({milestone}) | Tiêu chí thoát ({milestone}) |
| plan.reached | {milestone} reached on {date}. | {milestone} đạt ngày {date}. |
| plan.trace | Traceability matrix | Ma trận truy vết |
| plan.conventions | Working conventions | Quy ước làm việc |
| plan.dor | Definition of Ready | Definition of Ready |
| plan.dod | Definition of Done | Definition of Done |
| plan.git | Git and code | Git và code |
| plan.risks | Additional risks (beyond the original SDD) | Rủi ro bổ sung (ngoài SDD gốc) |
| plan.first_tasks | Start now: the first 10 tasks | Bắt đầu ngay: 10 việc đầu tiên |
| plan.templates | Appendix A: Shared templates | Phụ lục A: Template dùng chung |
| plan.vocabulary | Appendix B: Vocabulary | Phụ lục B: Từ vựng |
| plan.done | Done {date} | Xong {date} |
| plan.total | Total | Tổng |
| readme.title | Project documentation: {project} | Tài liệu dự án: {project} |
| readme.start_here | Start here | Bắt đầu từ đây |
| readme.documents | Documents | Tài liệu |
| readme.structure | Structure | Cấu trúc |
| readme.conventions | Conventions | Quy ước |
| readme.not_written | Not written | Chưa viết |
| col.id | ID | ID |
| col.task | Task | Việc |
| col.output | Output and acceptance | Đầu ra và tiêu chí nghiệm thu |
| col.depends | Depends on | Phụ thuộc |
| col.documents | Documents | Tài liệu |
| col.document | Document | Tài liệu |
| col.gate | Gate | Gate |
| col.required | Required content | Nội dung bắt buộc |
| col.estimate | Estimate (1 person, full time) | Ước lượng (1 người, toàn thời gian) |
| col.milestone | Milestone | Milestone |
| col.requirement | Requirement | Yêu cầu |
| col.design_docs | Design documents | Tài liệu thiết kế |
| col.tasks | Tasks | Công việc |
| col.verification | Verification | Kiểm chứng |
| col.priority | Priority | Ưu tiên |
| col.acceptance | Acceptance criteria | Tiêu chí nghiệm thu |
| col.target | Target | Chỉ tiêu |
| col.how_measured | How measured | Cách đo |
| col.risk | Risk | Rủi ro |
| col.early_sign | Early sign | Dấu hiệu sớm |
| col.mitigation | Mitigation | Xử lý |
| col.impact | Impact | Ảnh hưởng |
| col.scenario | Scenario | Kịch bản |
| col.expected | Expected | Kỳ vọng |
| col.term | Term | Thuật ngữ |
| col.local_name | Local name | Tiếng Việt |
| col.definition | Definition | Định nghĩa |
| col.key | Key | Key |
| col.type | Type | Kiểu |
| col.default | Default | Mặc định |
| col.description | Description | Mô tả |
| col.metric | Metric | Metric |
| col.label | Label | Label |
| col.situation | Situation | Tình huống |
| col.behavior | Behavior | Hành vi |
| col.from | From | Từ |
| col.to | To | Sang |
| col.triggered_by | Triggered by | Kích hoạt bởi |
| col.module | Module | Module |
| col.role | Role | Vai trò |
| col.investment | Investment level | Mức độ đầu tư |
| col.item | Item | Hạng mục |
| col.handled_now | How this phase handles it | Giai đoạn này xử lý thế nào |
| col.failure | Failure | Sự cố |
| col.detection | Detection | Phát hiện |
| col.system_behavior | System behavior | Hành vi hệ thống |
| col.recovery | Recovery | Phục hồi |
| col.object | Object | Đối tượng |
| col.invariant | Invariant | Bất biến |
| col.enforced_by | Enforced by | Được ép bằng |
| col.experiment | Experiment | Thực nghiệm |
| col.method | Method | Cách làm |
| col.metrics | Metrics | Chỉ số |
| col.stage | Stage | Giai đoạn |
| col.content | Content | Nội dung |
| col.results | Results | Kết quả đầu ra |
| col.date | Date | Ngày |
| col.decided_by | Decided by | Người chốt |
| col.affected | Affected items | Mục bị ảnh hưởng |
| col.level | Level | Mức |
| col.reason | Reason | Lý do |
| col.participant | Participant | Thành phần tham gia |
| col.kind | Kind | Loại |
| col.code | Code | Code |
| col.defined_in | Defined in | Định nghĩa tại |
| col.step | Step | Bước |
| col.from_to | From → To | Từ → Đến |
| col.call | Call | Lời gọi |
| col.data | Data | Dữ liệu |
| col.rules_checks | Rules and checks | Quy tắc và kiểm tra |
| col.error_handling | Error → handling | Lỗi → xử lý |
| col.http_problem | HTTP status / problem type | HTTP status / problem type |
| col.ui_behavior | UI behavior and message | Hành vi UI và thông báo |
| col.flow | Flow | Luồng |
| col.screens | Screens | Màn hình |
| col.endpoints | Endpoints | Endpoint |
| col.file | File | File |
| adr.title | ADR-{n}: {title} | ADR-{n}: {title} |
| adr.context | Context | Bối cảnh |
| adr.options | Options considered | Các phương án |
| adr.decision | Decision | Quyết định |
| adr.consequences | Consequences | Hệ quả |
| adr.positive | Positive | Tích cực |
| adr.negative | Negative | Tiêu cực |
| adr.followups | Follow-up work | Việc phát sinh |
| uc.actor | Actor | Actor |
| uc.trigger | Trigger | Trigger |
| uc.preconditions | Preconditions | Tiền điều kiện |
| uc.main_flow | Main flow | Luồng chính |
| uc.alt_flows | Alternative flows | Luồng thay thế |
| uc.error_flows | Error flows | Luồng lỗi |
| uc.postconditions | Postconditions | Hậu điều kiện |
| uc.rules | Business rules | Quy tắc |
| uc.diagram | Use case overview | Sơ đồ tổng |
| req.conventions | Conventions | Quy ước |
| req.functional | Functional requirements | Yêu cầu chức năng |
| req.non_functional | Non-functional requirements | Yêu cầu phi chức năng |
| req.matrix | FR → UC → feature → design matrix | Ma trận FR → UC → tính năng → thiết kế |
| req.added | added | bổ sung |
| ep.purpose | Purpose / UC | Mục đích / UC |
| ep.auth | Authorization | Quyền |
| ep.params | Parameters | Tham số |
| ep.response | Response | Response |
| ep.errors | Errors | Lỗi |
| ep.data_source | Data source | Nguồn dữ liệu |
| ep.cache | Cache | Cache |
| ep.performance | Performance | Hiệu năng |
| ep.events | Related real-time events | Sự kiện real-time liên quan |
| scr.title | Screen: {name} | Màn hình: {name} |
| scr.persona | Persona, use cases, permissions | Persona, use case, quyền |
| scr.url | URL and search params | URL và search params |
| scr.wireframe | Wireframe | Wireframe |
| scr.regions | Regions and components | Vùng và component |
| scr.data | Data | Dữ liệu |
| scr.interactions | Interactions | Tương tác |
| scr.states | States | Trạng thái |
| scr.copy | Microcopy | Microcopy |
| scr.acceptance | Acceptance criteria | Tiêu chí nghiệm thu |
| scr.e2e | E2E test cases | Ca kiểm thử E2E |
| exp.hypothesis | Hypothesis | Giả thuyết |
| exp.variables | Variables | Biến |
| exp.baseline | Baseline | Baseline |
| exp.environment | Environment | Môi trường |
| exp.steps | Steps | Các bước |
| exp.metrics | Metrics and formulas | Chỉ số và công thức |
| exp.pass | Pass criteria | Tiêu chí đạt |
| exp.analysis | Analysis | Phân tích |
| exp.result_table | Result table template | Mẫu bảng kết quả |
| exp.threats | Threats to validity | Mối đe dọa tới tính hợp lệ |
| exp.results | Results | Kết quả |
| rb.symptoms | Symptoms and impact | Triệu chứng và ảnh hưởng |
| rb.checks | Checks | Kiểm tra |
| rb.remediation | Remediation | Xử lý |
| rb.on_env | On {environment} | Trên {environment} |
| rb.verify | Confirm it is resolved | Xác nhận đã xong |
| rb.prevention | Prevention and follow-up | Phòng ngừa và việc sau sự cố |
| des.purpose | Purpose and scope | Mục đích và phạm vi |
| des.components | Components and interfaces | Thành phần và interface |
| des.algorithm | Algorithm | Thuật toán |
| des.concurrency | Transactions and concurrency | Transaction và đồng thời |
| des.config | Configuration | Cấu hình |
| des.metrics | Metrics and logs | Metrics và log |
| des.errors | Errors and handling | Lỗi và cách xử lý |
| des.tests | Required tests | Test bắt buộc |
| des.not_here | Not in this document | Không thuộc tài liệu này |
| flow.index | Detailed flows | Luồng chi tiết |
| flow.title | Detailed flows: {area} | Luồng chi tiết: {area} |
| flow.screen | Screen | Màn hình |
| flow.events | Events | Sự kiện |
| flow.participants | Participants | Thành phần tham gia |
| flow.sequence | Sequence diagram | Sơ đồ tuần tự |
| flow.steps | Step details | Chi tiết từng bước |
| persona.overview | Overview | Tổng quan |
| persona.goals | Goals | Mục tiêu |
| persona.pains | Pain points | Nỗi đau |
| persona.needs | Needs from {system} | Cần từ {system} |
| persona.not_needed | Does not need | Không cần |
| persona.screens | Screens | Màn hình |
| persona.journey | Journey | Hành trình |
| sdd.title | {name} — System Design | {name} — Thiết kế hệ thống |
| sdd.intro | Introduction | Giới thiệu |
| sdd.context | Context | Bối cảnh |
| sdd.problems | Real-world problems | Vấn đề thực tế |
| sdd.vision | Vision | Tầm nhìn |
| sdd.goals | Goals, scope and focus | Mục tiêu, phạm vi và trọng tâm |
| sdd.research_question | Research question | Câu hỏi nghiên cứu |
| sdd.core_problem | Core problem | Bài toán cốt lõi |
| sdd.investment | Investment by module | Mức độ đầu tư theo module |
| sdd.scope | Scope | Phạm vi |
| sdd.in_scope | In scope | Trong phạm vi |
| sdd.later | Later | Để sau |
| sdd.out_of_scope | Out of scope | Ngoài phạm vi |
| sdd.users | Users, use cases and requirements | Người dùng, use case và yêu cầu |
| sdd.user_groups | User groups | Nhóm người dùng |
| sdd.use_cases | Use cases | Use case |
| sdd.fr | Functional requirements | Yêu cầu chức năng |
| sdd.nfr | Non-functional requirements | Yêu cầu phi chức năng |
| sdd.architecture | Overall architecture and technology | Kiến trúc tổng thể và công nghệ |
| sdd.components | Components | Các thành phần |
| sdd.principles | Cross-cutting principles | Nguyên tắc xuyên suốt |
| sdd.data_flow | Data flow | Luồng dữ liệu |
| sdd.technology | Technology | Công nghệ |
| sdd.data_model | Data model | Mô hình dữ liệu |
| sdd.entities | Entities | Thực thể |
| sdd.constraints | Required constraints | Ràng buộc bắt buộc |
| sdd.api | Backend API | Backend API |
| sdd.endpoints | Endpoints | Endpoint |
| sdd.conventions | Conventions | Quy ước |
| sdd.ui | User interface | Giao diện |
| sdd.screens | Screens | Màn hình |
| sdd.ui_tech | Technical notes | Kỹ thuật |
| sdd.ops | Deployment and fault tolerance | Triển khai và chịu lỗi |
| sdd.deployment | Deployment | Triển khai |
| sdd.failures | Behavior under failure | Hành vi khi có sự cố |
| sdd.invariant_checks | Invariant checks | Kiểm tra bất biến |
| sdd.security | Minimum security | Bảo mật tối thiểu |
| sdd.testing | Testing and evaluation | Kiểm thử và đánh giá |
| sdd.test_strategy | Test strategy | Chiến lược kiểm thử |
| sdd.experiments | Experiments | Thực nghiệm |
| sdd.plan | Implementation plan | Kế hoạch triển khai |
| sdd.demo | Demo script | Kịch bản demo |
| sdd.risks | Risks and limitations | Rủi ro và giới hạn |
| sdd.open_points | Open points | Điểm còn mở |
| sdd.repo | Appendix: Repository layout | Phụ lục: Cấu trúc repo |
| sdd.alternatives | {problem}: options and rationale | {problem}: các phương án và lý do chọn |
| sdd.option | Option {x}: {name} | Phương án {x}: {name} |
| sdd.chosen | chosen | chọn |
| sdd.pros | Pros | Ưu điểm |
| sdd.cons | Cons | Nhược điểm |
| sdd.verdict | Verdict | Kết luận |
| sdd.comparison | Comparison and rationale | So sánh và lý do chọn |
| sdd.parameters | Parameters | Tham số |
| sdd.text_version | Text version of the figure above, for Markdown export | Bản chữ của hình trên, dùng khi xuất Markdown |
