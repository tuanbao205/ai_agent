# Implementation Plan — AgentOS Customer360

- **Phiên bản:** 0.1
- **Trạng thái:** Dự thảo trình Lead
- **Mục tiêu:** Chuyển SRS và bộ kế hoạch hiện có thành kế hoạch triển khai có thể phê duyệt, chưa bao gồm viết mã nguồn.

## 1. Quyết định định hướng

### 1.1. Sản phẩm

Xây một nền tảng AI SaaS dùng chung cho doanh nghiệp vừa và nhỏ:

- Core Platform dùng chung.
- Cấu hình riêng theo từng doanh nghiệp.
- Adapter kết nối hệ thống sẵn có.
- Dữ liệu cô lập tuyệt đối theo tenant.
- Tính năng được mở dần theo quyền và gói dịch vụ.

### 1.2. Phương án triển khai khuyến nghị

**Modular monolith trước, microservices sau.**

Lý do:

- Phù hợp nhóm phát triển nhỏ.
- Dễ kiểm thử xuyên luồng.
- Chi phí hạ tầng thấp hơn.
- Giảm rủi ro phân tán trạng thái workflow và audit.
- Có thể tách service sau khi có tải và ranh giới ổn định.

**Fake connector trước, connector thật sau.**

Lý do:

- Chưa có pilot và quyền API.
- Cho phép kiểm chứng workflow, policy và dữ liệu mà không dùng dữ liệu thật.
- Giảm rủi ro bảo mật và phụ thuộc bên ngoài.

**P1 Customer Care trước Sales/Marketing.**

Lý do:

- Rủi ro tài chính thấp hơn.
- Kiểm chứng được Customer360, identity, knowledge, handoff và audit.
- Tạo nền tảng dùng lại cho Sales và Marketing.

## 2. Các phần đề bài còn thiếu cần hoàn thiện

### GAP-01 — Thiếu thông tin pilot

Cần chốt:

- Doanh nghiệp thử nghiệm.
- Ngành và sản phẩm.
- Website/app/kênh đầu tiên.
- Một hành trình khách hàng ưu tiên.
- Người nghiệm thu nghiệp vụ.
- KPI baseline.

**Đầu ra:** Pilot Charter được Lead và đại diện nghiệp vụ xác nhận.

### GAP-02 — Chưa có phạm vi MVP được phê duyệt

Cần phân biệt rõ:

- Bắt buộc trong P0/P1.
- Để P2/P3.
- Ý tưởng thương mại dài hạn.
- Những tính năng không làm trong MVP.

**Đầu ra:** Scope baseline và danh sách out-of-scope.

### GAP-03 — Chưa khóa yêu cầu thành backlog

SRS đã có mã yêu cầu nhưng chưa có đầy đủ:

- User story.
- Acceptance criteria.
- Priority.
- Dependency.
- Owner.
- Estimate.
- Trạng thái.

**Đầu ra:** Product backlog liên kết `OBJ`, `FR`, `BR`, `NFR`, `TC-E2E`.

### GAP-04 — Chưa chốt kiến trúc triển khai

Cần ra quyết định về:

- Backend framework.
- Database.
- Queue/workflow engine.
- LLM provider và chính sách thay thế.
- Vector/search store.
- Authentication/RBAC.
- Observability.
- Hạ tầng và region dữ liệu.

**Đầu ra:** Architecture Decision Record, không chỉ là mô tả ý tưởng.

### GAP-05 — Chưa có canonical API/data contract triển khai

Cần khóa:

- Customer, Identity, Consent.
- Conversation, Case, Event.
- Agent, Skill, Workflow.
- Decision, Action, Approval.
- Execution, Evidence, Outcome.
- Error model, idempotency và trace context.

**Đầu ra:** Contract version 0.1 có schema, owner, source of truth và policy dữ liệu.

### GAP-06 — Chưa có mô hình bảo mật và tuân thủ thực thi

Cần xác định:

- Tenant isolation.
- RBAC và quyền nhân viên.
- PII classification/masking.
- Consent và opt-out.
- Data retention/deletion.
- Secret management.
- Audit access.
- Incident response.

**Đầu ra:** Security and Data Protection Checklist cho pilot.

### GAP-07 — Chưa có chiến lược kiểm thử có thể nghiệm thu

Cần chuẩn hóa:

- Unit test.
- Contract test.
- Integration test với fake connector.
- Negative/security test.
- E2E test theo `TC-E2E-001..009`.
- Load/performance test ở production-like.
- Regression test sau thay đổi prompt, policy, knowledge và connector.

**Đầu ra:** Test Plan và Definition of Done.

### GAP-08 — Chưa có kế hoạch vận hành production

Cần chốt:

- Environments: local, dev, staging, production.
- CI/CD.
- Migration/rollback.
- Monitoring và alerting.
- Cost/token budget.
- On-call và escalation.
- Backup/restore.
- Runbook.

**Đầu ra:** Production Readiness Checklist.

### GAP-09 — Chưa có mô hình thương mại SaaS khả thi

Cần làm rõ:

- Gói dịch vụ theo module.
- Phí setup/configuration.
- Phí subscription.
- Chi phí AI và connector.
- Giới hạn usage.
- SLA theo gói.
- Chi phí onboarding và hỗ trợ.
- Cách chứng minh ROI.

**Đầu ra:** Pricing and Packaging baseline, tách khỏi platform core.

## 3. Lộ trình đề xuất

### Phase 0 — Decision and Scope

**Mục tiêu:** có quyết định chính thức trước khi code.

Công việc:

1. Chốt Pilot Charter.
2. Chốt P1 journey.
3. Chốt KPI baseline.
4. Chốt scope/out-of-scope.
5. Chốt owner và người nghiệm thu.
6. Phê duyệt architecture direction.

**Điều kiện hoàn thành:** Lead ký duyệt scope, owner, KPI và phương án kiến trúc cấp cao.

### Phase 1 — Foundation Design

**Mục tiêu:** biến yêu cầu thành hợp đồng triển khai.

Công việc:

1. Canonical data model.
2. API/event contracts.
3. Tenant and RBAC model.
4. Authority/policy matrix.
5. Evidence/audit specification.
6. Test plan.
7. Threat model.

**Điều kiện hoàn thành:** mọi requirement P1 có owner, acceptance criteria và traceability.

### Phase 2 — P1 Customer Care Design

**Mục tiêu:** thiết kế đầy đủ một sản phẩm có thể pilot.

Phạm vi:

- FAQ có nguồn và version.
- Intent classification.
- Identity verification.
- Order lookup read-only.
- Service Case.
- Human handoff.
- Audit/evidence.
- Dashboard vận hành tối thiểu.

**Không làm:** payment, refund tự động, discount, Sales Agent, Marketing campaign.

**Điều kiện hoàn thành:** có sequence diagram, API contract, test cases, risk controls và runbook nháp.

### Phase 3 — Build Readiness

**Mục tiêu:** chuẩn bị đủ điều kiện để đội kỹ thuật bắt đầu code.

Công việc:

- Chọn stack cuối cùng.
- Chọn database và workflow persistence.
- Chọn LLM provider strategy.
- Tạo repository structure.
- Thiết lập CI và quality gates.
- Chuẩn bị seed data/fake connectors.
- Chuẩn bị môi trường dev/staging.

**Điều kiện hoàn thành:** không còn dependency chưa có owner làm chặn việc bắt đầu P1.

### Phase 4 — P1 Pilot

Chỉ thực hiện sau khi Phase 0–3 được duyệt.

- Build theo vertical slice.
- Test local.
- Test integration.
- Deploy production-like.
- Security review.
- UAT với nghiệp vụ.
- Pilot có giám sát.

### Phase 5 — Mở rộng có điều kiện

Chỉ mở P2 Sales khi P1 đạt:

- Không có lỗi nghiêm trọng về rò dữ liệu/quyền.
- Connector lookup ổn định.
- Human handoff hoạt động.
- KPI có baseline và số liệu đủ tin cậy.
- Có quyết định thương mại tiếp tục.

## 4. Backlog ưu tiên để Lead xem xét

| ID | Hạng mục | Ưu tiên | Phụ thuộc | Đầu ra |
|---|---|---:|---|---|
| PLAN-001 | Pilot Charter | P0 | Business owner | Tài liệu pilot được duyệt |
| PLAN-002 | MVP scope baseline | P0 | PLAN-001 | In/out scope |
| PLAN-003 | KPI baseline | P0 | PLAN-001 | Bộ chỉ số nguồn |
| PLAN-004 | Architecture Decision Record | P0 | PLAN-002 | Quyết định kiến trúc |
| PLAN-005 | Canonical data model | P0 | PLAN-004 | Schema v0.1 |
| PLAN-006 | API/event contract | P0 | PLAN-005 | Contract package |
| PLAN-007 | Security/threat model | P0 | PLAN-005 | Risk controls |
| PLAN-008 | P1 sequence and state model | P1 | PLAN-002 | Workflow specification |
| PLAN-009 | Test plan and DoD | P1 | PLAN-006 | Acceptance package |
| PLAN-010 | Production readiness plan | P1 | PLAN-004 | Runbook/checklist |
| PLAN-011 | Pricing and packaging | P1 | PLAN-002 | Commercial baseline |
| PLAN-012 | Go/no-go review | P0 | PLAN-001..011 | Quyết định bắt đầu build |

## 5. Quyết định cần Lead phê duyệt

1. Có chọn một pilot cụ thể trong giai đoạn đầu hay tiếp tục nghiên cứu tổng quát?
2. P1 ưu tiên FAQ, tra cứu đơn hàng hay khiếu nại/handoff?
3. Có cho phép dùng fake connector để hoàn thiện thiết kế trước khi có API thật không?
4. Stack nào phù hợp năng lực đội ngũ và hạ tầng công ty?
5. Mức độ multi-tenant cần có trong P1: schema isolation hay database isolation?
6. Ai là owner của dữ liệu, policy, security, KPI và nghiệm thu?
7. Ngân sách/thời gian tối đa cho Phase 0–3 là bao nhiêu?
8. Điều kiện nào bắt buộc phải đạt trước khi demo cho khách hàng?

## 6. Tiêu chí Go/No-Go trước khi viết code

### Go

- Có Pilot Charter và owner.
- Có scope P1 được duyệt.
- Có dữ liệu thử hoặc fake data hợp lệ.
- Có contract P1 versioned.
- Có security baseline.
- Có test plan và người nghiệm thu.
- Có ngân sách và môi trường phát triển.

### No-Go

- Chưa biết doanh nghiệp hoặc hành trình sẽ thử.
- Chưa có owner dữ liệu/API.
- Chưa có cách xác minh khách hàng.
- Chưa có chính sách retention/PII.
- Chưa có người nhận handoff.
- Muốn demo bằng dữ liệu thật nhưng chưa có quyền.
- Muốn mở Sales/Marketing trước khi P1 và policy nền ổn định.
