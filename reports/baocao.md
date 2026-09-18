# Báo cáo điều hành dự án AgentOS Customer360

 **Ngày cập nhật:** 18/09/2026
 **Phiên bản báo cáo:** 0.2
 **Trạng thái:** Đã khóa P0 contract local; chưa có runtime
 Đã tạo bản contract P0/P1 độc lập tại [plans/platform/p0-contracts.md](../plans/platform/p0-contracts.md).
- **Tài liệu nguồn chính:** `De_bai_Xay_dung_He_thong_AI_Agent_Marketing_Sales_CSKH_v0.1.md`, `plans/`, `reports/AUDIT_DE_BAI_VS_KE_HOACH.md`

### 2.4. Luồng contract P0 đã khóa local

```text
Request có tenant context
  -> Kiểm tra tenant boundary
  -> Kiểm tra authority và điều kiện P1
  -> Chạy skill CSKH được phép
  -> Ghi run/evidence/audit
  -> Trả kết quả hoặc DENY/FAILED trung thực
```

Contract chi tiết gồm tenant boundary, Customer, Identity, Consent, Conversation, Service Case, Evidence, Agent Run và 5 skill P1. Tám acceptance checks tối thiểu đã được ghi trong tài liệu P0.
 Chưa có API transport và connector thật với ERP/WMS, website hoặc kênh chat; contract nghiệp vụ P0 đã có bản local đầu tiên.
 Giữ contract P0 độc lập công nghệ; chỉ chốt framework sau khi kiểm tra môi trường và yêu cầu triển khai.
 [ ] Chốt phiếu đầu vào pilot trong `plans/delivery/mvp-and-roadmap.md` (chưa đủ thông tin từ chủ dự án).
 [x] Tạo contract/schema nghiệp vụ P0/P1 đầu tiên tại `plans/platform/p0-contracts.md`.
 Đã khóa local các ranh giới tenant, entity P1, skill P1 và 8 acceptance checks tại `plans/platform/p0-contracts.md`.
- Chưa có doanh nghiệp pilot, website/app cụ thể, bộ dữ liệu thật, API credential hoặc KPI baseline.
 Sau khi contract P0 đã được khóa, có thể tạo skeleton local bằng fake connector mà không cần chờ dữ liệu production. Tuy nhiên vẫn cần chốt stack kỹ thuật trước khi sinh mã nguồn.
- Chưa có môi trường local chạy ứng dụng và chưa có môi trường production để kiểm chứng.
- Đã có tài liệu kiến trúc, nghiệp vụ, lộ trình, mã yêu cầu, pilot và bộ kiểm thử đề xuất.

### 1.2. Kiến trúc đích đã thống nhất

Dự án hướng tới nền tảng **Core Platform + Industry Template + Customer Configuration**:

1. **Platform:** Customer360, Revenue Orchestrator, Knowledge Base, Policy/Authority, Evidence, Audit và Connector Framework.
2. **Commercial Engine:** giá sàn, ngân sách ưu đãi, chi phí AI và các quy tắc bảo toàn biên lợi nhuận.
3. **Domain Playbooks:** Mobility, FMCG, thị trường Đài Loan và các adapter mở rộng.

Ba nhóm sản phẩm bên ngoài là Marketing, Sales và Customer Care. Bên trong có 13 sub-agent chuyên môn, không phải 13 sản phẩm độc lập.

## 2. Luồng xử lý hiện tại

### 2.1. Luồng đang có trong tài liệu

```text
Tín hiệu khách hàng
  -> Customer Intelligence 360
  -> Marketing / Sales / Customer Care
  -> Revenue Orchestrator
  -> Policy + Authority + Approval
  -> Connector / hệ thống nguồn ERP-POS-Web-App
  -> Evidence
  -> Outcome
  -> Learning
```

### 2.2. Luồng thực tế trong workspace hiện nay

```text
Tài liệu SRS
  -> Bộ kế hoạch plans/
  -> Audit và phân lớp 3 tầng
  -> Roadmap P0-P5
  -> Chưa có bước triển khai runtime
```

Đây là luồng thiết kế, **chưa phải luồng xử lý dữ liệu thật**. Chưa thể kết luận hệ thống đã đáp ứng các hành vi như tra cứu đơn hàng, chuyển nhân viên, chống gửi trùng hoặc kiểm soát giá.

### 2.3. Luồng MVP được ưu tiên

Bắt đầu bằng **P0 Foundation**, sau đó triển khai **P1 Customer Care Pilot**:

```text
Khách gửi câu hỏi
  -> Nhận diện intent
  -> Xác minh danh tính
  -> Tra cứu FAQ hoặc ERP/WMS
  -> Trả lời có evidence
  -> Tạo/đóng Service Case
  -> Chuyển người nếu ngoài phạm vi hoặc vượt quyền
  -> Ghi audit log và outcome
```

Trong P1, Marketing và Sales phải tắt hoàn toàn. Không tạo giỏ hàng, không chốt đơn, không tự giảm giá, không hoàn tiền.

## 3. Vấn đề gặp phải

1. Chưa có hệ thống thực thi để kiểm chứng các thiết kế trong `plans/`.
2. Chưa khóa doanh nghiệp pilot, hành trình đầu tiên và kết quả cần đo.
3. Chưa có canonical data model cho Customer360, Conversation, Case, Evidence, Action và Approval.
4. Chưa có API contract và connector thật với ERP/WMS, website hoặc kênh chat.
5. Chưa có cơ chế runtime cho policy, authority, idempotency, retry và audit.
6. Chưa có bộ dữ liệu thử, test fixture và acceptance test có thể chạy tự động.
7. Roadmap hiện chứa nhiều ý tưởng thương mại nâng cao, dễ làm phạm vi bị phình trước khi P1 hoạt động.
8. Chưa có tiêu chí phân biệt rõ tính năng đã chạy local, đã chạy production-like và đã được doanh nghiệp nghiệm thu.

## 4. Nguyên nhân

- Dự án đang ở giai đoạn chuyển từ **đề bài/SRS và kế hoạch** sang **sản phẩm có thể chạy**.
- Thiếu các đầu vào bắt buộc: pilot, API, dữ liệu, người phụ trách nghiệp vụ, quyền truy cập và KPI baseline.
- Phần thương mại Mobility/FMCG và Đài Loan được mô tả rộng hơn phần nền tảng thực thi.
- Chưa có source code nên chưa thể đánh giá lỗi runtime, hiệu năng, bảo mật hoặc chất lượng tích hợp.

## 5. Phương án xử lý tối ưu

### 5.1. Quyết định phạm vi

Chọn chiến lược **P0 nhỏ, P1 có thể chạy, rồi mới mở rộng**. Không xây đồng thời cả 13 agent và tất cả connector.

MVP đầu tiên chỉ cần:

- Một tenant thử nghiệm.
- Một kênh vào, ưu tiên Web Chat hoặc một kênh đã có quyền truy cập.
- Một nguồn tri thức FAQ đã duyệt.
- Một API đọc đơn hàng giả lập hoặc thật có quyền read-only.
- Một luồng xác minh danh tính.
- Một luồng chuyển nhân viên.
- Audit log và bộ test phủ định.

### 5.2. Thứ tự triển khai từng bước nhỏ

| Bước | Mục tiêu | Kết quả bắt buộc để chuyển bước |
|---|---|---|
| 0 | Chốt đầu vào pilot | Có tenant, hành trình, nguồn dữ liệu, người nghiệm thu và KPI |
| 1 | Khóa P0 contracts | Có schema/API contract version đầu tiên và quy tắc tenant |
| 2 | Dựng local skeleton | Server, database, cấu hình và test runner chạy được local |
| 3 | Xây policy nền | AUTH-0..5, BR-001..010 quan trọng cho P1 và cơ chế DENY |
| 4 | Xây Customer360 tối thiểu | Customer, Identity, Consent, Conversation, Case, Event, Evidence |
| 5 | Xây Knowledge/FAQ | Trả lời theo nguồn, phiên bản, trạng thái duyệt; không có nguồn thì từ chối |
| 6 | Xây P1 Care flow | Intent, identity verification, lookup, response, escalation, takeover |
| 7 | Chạy test local | Các ca P1 và test bảo mật/idempotency/retry đạt trên fixture |
| 8 | Dựng production-like | Container/config/log/secret/monitoring và dữ liệu test riêng |
| 9 | Pilot có giám sát | Chạy với dữ liệu/quyền được phê duyệt, có rollback và người trực |
| 10 | Đánh giá P1 | Đối chiếu KPI, lỗi, chi phí, quyết định mở P2 hoặc sửa P1 |

### 5.3. Phương án kỹ thuật khuyến nghị

- Dùng **modular monolith** cho P0/P1 để giảm độ phức tạp; chưa tách microservice khi chưa có tải thực tế.
- Dùng adapter/interface cho ERP, chat, LLM và knowledge store để thay thế được connector.
- Tách rõ các lớp: domain contracts, policy, orchestration, integration, persistence và presentation.
- Mọi action bên ngoài phải có `trace_id`, `execution_id`, `idempotency_key`, authority và evidence.
- Mặc định **fail closed**: thiếu quyền, thiếu nguồn hoặc connector lỗi thì không tự đoán và không ghi thành công.
- Dùng fake connector trong local; production chỉ bật connector thật sau khi đã có quyền, secret và test hợp đồng.
- Viết test cùng lúc với từng capability, không đợi đến cuối mới kiểm thử.

## 6. Phương pháp luận làm việc

Mỗi vòng triển khai sẽ theo chu trình:

```text
Đọc tài liệu liên quan
  -> Chốt một giả thuyết và phạm vi nhỏ
  -> Sửa/xây một lát cắt có thể chạy
  -> Chạy kiểm tra hẹp nhất
  -> Ghi kết quả vào báo cáo này
  -> Chỉ mở rộng khi điều kiện bước trước đạt
```

Nguyên tắc kiểm soát:

- Mỗi thay đổi phải gắn với yêu cầu, pilot hoặc test cụ thể.
- Không đánh dấu hoàn thành khi mới có tài liệu hoặc mock chưa chạy.
- Tách trạng thái `planned`, `local`, `production-like`, `production`, `accepted`.
- Không dùng dữ liệu thật trong local nếu chưa có phê duyệt và cơ chế ẩn danh.
- Ưu tiên an toàn dữ liệu, quyền hạn, truy vết và tính đúng đắn trước tính năng thương mại nâng cao.

## 7. Hành động

### 7.1. Local

- [x] Tạo báo cáo điều hành trung tâm tại `reports/baocao.md`.
- [ ] Chốt phiếu đầu vào pilot trong `plans/delivery/mvp-and-roadmap.md`.
- [ ] Kiểm kê chính xác source code, công cụ build và môi trường hiện có.
- [ ] Chốt stack kỹ thuật cho P0/P1.
- [ ] Tạo skeleton chạy được và health check.
- [ ] Tạo contract/schema đầu tiên và test runner.

### 7.2. Production

- [ ] Chưa triển khai production.
- [ ] Chưa có tenant/website pilot được phê duyệt.
- [ ] Chưa cấp connector, secret hoặc quyền truy cập dữ liệu thật.
- [ ] Chưa có kế hoạch rollback, giám sát và người trực production.

## 8. Kết quả

### 8.1. Local

- Đã xác nhận workspace hiện chứa tài liệu thiết kế, chưa có runtime để chạy kiểm thử chức năng.
- Đã xác định P0/P1 là phạm vi triển khai an toàn và có giá trị kiểm chứng cao nhất.
- Đã tạo file báo cáo trung tâm để cập nhật sau mỗi thay đổi: `reports/baocao.md`.

### 8.2. Production

- Chưa có kết quả production.
- Chưa được phép ghi nhận KPI, doanh thu, độ ổn định hoặc mức tự động hóa production.

## 9. Điều kiện cần chốt trước bước viết code

1. Tên hoặc loại doanh nghiệp pilot.
2. Hành trình P1 đầu tiên: FAQ, tra cứu đơn, hay khiếu nại/chuyển nhân viên.
3. Kênh giao tiếp đầu tiên.
4. Có API ERP/WMS thật hay dùng fake connector trước.
5. Stack kỹ thuật hoặc giới hạn hạ tầng của dự án.
6. Người có quyền nghiệm thu nghiệp vụ.

## 10. Quy ước cập nhật báo cáo

Mỗi lần có thay đổi đáng kể, báo cáo này phải được cập nhật các mục liên quan, đặc biệt:

- Hiện trạng hệ thống.
- Luồng xử lý hiện tại.
- Vấn đề và nguyên nhân mới.
- Phương án xử lý đã chọn.
- Hành động local và production.
- Kết quả local và production.

Các mục hành động và kết quả sẽ chỉ được đánh dấu hoàn thành khi có bằng chứng chạy được, log, test hoặc xác nhận nghiệm thu tương ứng.
