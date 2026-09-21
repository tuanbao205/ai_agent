# Pilot Charter — AgentOS Customer360

- **Phiên bản:** 0.1
- **Trạng thái:** Dự thảo cần Lead và đại diện nghiệp vụ phê duyệt
- **Mục đích:** Chốt một phạm vi pilot đủ nhỏ để kiểm chứng giá trị và rủi ro trước khi phát triển sản phẩm.

## 1. Khuyến nghị chính

### Pilot được khuyến nghị

**P1 Customer Care cho một doanh nghiệp SME có website bán hàng và dữ liệu đơn hàng truy cập được ở chế độ read-only.**

Hành trình ưu tiên:

```text
Khách hỏi trạng thái đơn hàng
  -> Xác minh danh tính
  -> Tra cứu đơn từ hệ thống nguồn
  -> Trả lời có nguồn và mã vận đơn
  -> Tạo case nếu lỗi hoặc khách yêu cầu người thật
  -> Nhân viên tiếp quản
  -> Ghi nhận kết quả
```

### Vì sao đây là lựa chọn tối ưu

- Có giá trị rõ ràng và dễ giải thích với doanh nghiệp SME.
- Ít rủi ro tài chính hơn tư vấn bán hàng hoặc tự động khuyến mãi.
- Có thể đo bằng chỉ số vận hành: thời gian phản hồi, tỷ lệ tự xử lý, tỷ lệ chuyển người, tỷ lệ giải quyết.
- Kiểm chứng được những nền tảng bắt buộc cho toàn bộ sản phẩm: Customer360, identity, knowledge, policy, connector, audit và handoff.
- Có thể chạy bằng dữ liệu giả lập trước khi kết nối hệ thống thật.

## 2. Các phương án để Lead lựa chọn

| Phương án | Phạm vi | Ưu điểm | Hạn chế | Đánh giá |
|---|---|---|---|---|
| **A — Order Status + Handoff** | Xác minh khách, tra cứu đơn, chuyển nhân viên | Giá trị rõ, rủi ro thấp, đo được, đặt nền cho P1 | Cần API đơn hàng hoặc dữ liệu mẫu hợp lệ | **Khuyến nghị** |
| B — FAQ thuần túy | Trả lời FAQ/policy có nguồn | Làm nhanh, ít tích hợp | Khó chứng minh giá trị vận hành và Customer360 | Chỉ dùng làm bước chuẩn bị |
| C — Complaint + Handoff | Nhận diện khiếu nại, tạo case, chuyển người | Kiểm chứng authority và human takeover | Rủi ro nghiệp vụ cao, cần đội CSKH trực | Chỉ chọn khi doanh nghiệp có nhu cầu cấp thiết |
| D — Sales Advisor | Tư vấn, gợi ý sản phẩm | Dễ tạo ấn tượng demo và gần doanh thu | Rủi ro giá, tồn kho, hallucination, consent | Không nên làm đầu tiên |

## 3. Phạm vi đề xuất cho phương án A

### In scope

- Một tenant doanh nghiệp.
- Một kênh đầu vào: Web Chat hoặc kênh doanh nghiệp đã có sẵn.
- Một loại yêu cầu: tra cứu trạng thái đơn hàng.
- Xác minh khách hàng trước khi trả dữ liệu riêng tư.
- Tra cứu read-only từ fake connector ở giai đoạn thiết kế/test.
- Thay thế bằng API thật ở production-like sau khi có quyền.
- Trả lời dựa trên dữ liệu nguồn, có `source_ref`/evidence.
- Tạo Service Case khi không tra cứu được, dữ liệu mơ hồ hoặc khách yêu cầu nhân viên.
- Handoff cho nhân viên và không để AI trả lời chồng.
- Audit log cho request, policy decision, connector result và outcome.
- Báo cáo KPI cơ bản.

### Out of scope

- Tạo hoặc sửa đơn hàng.
- Thanh toán, hoàn tiền, đổi trả tự động.
- Tư vấn bán hàng, recommendation, upsell/cross-sell.
- Marketing campaign, broadcast và lead nurturing.
- Tự động giảm giá hoặc giá sàn.
- Tích hợp đồng thời nhiều kênh.
- Tự động hóa toàn bộ CRM/ERP.
- Multi-tenant production với nhiều khách hàng thật.
- Tự chủ AUTH-4 hoặc các hành động tài chính.

## 4. Đầu vào bắt buộc cần điền

| Hạng mục | Giá trị hiện tại | Người chốt | Hạn chốt |
|---|---|---|---|
| Doanh nghiệp pilot | **Chưa chọn** | Business owner | Chưa đặt |
| Ngành/sản phẩm | **Chưa chọn** | Business owner | Chưa đặt |
| Website/app/kênh đầu tiên | **Chưa chọn** | Product/IT | Chưa đặt |
| Hệ thống nguồn đơn hàng | **Chưa xác nhận** | IT/Data owner | Chưa đặt |
| Phương thức xác minh khách | **Đề xuất: OTP hoặc signed session** | Security/Product | Chưa đặt |
| Người nhận bàn giao | **Chưa phân công** | Operations/CS lead | Chưa đặt |
| Giờ trực và SLA | **Chưa chốt** | Operations lead | Chưa đặt |
| KPI baseline | **Chưa có** | Business/Analytics | Chưa đặt |
| Chính sách lưu/xóa dữ liệu | **Chưa rà soát** | Legal/Data owner | Chưa đặt |
| Người nghiệm thu | **Chưa phân công** | Lead | Chưa đặt |

Không dùng dữ liệu khách thật cho local hoặc tài liệu demo nếu chưa có phê duyệt, masking và phạm vi truy cập rõ ràng.

## 5. KPI và cách đo

### KPI bắt buộc trước pilot

- FRT: thời gian từ message nhận đến phản hồi đầu tiên.
- Tỷ lệ xác minh thành công.
- Tỷ lệ tra cứu đúng dữ liệu nguồn.
- Tỷ lệ AI tự xử lý có xác nhận.
- Tỷ lệ chuyển nhân viên.
- Thời gian tạo case và thời gian nhận case.
- Tỷ lệ trả lời sai hoặc không có nguồn.
- Tỷ lệ lỗi connector được báo trung thực.
- Tỷ lệ truy cập chéo tenant: phải bằng 0.
- Chi phí mỗi phiên: chỉ đo sau khi có dữ liệu chi phí thực.

### Nguyên tắc đo

- Chốt baseline trước khi bật AI.
- Không ghi `0` khi chưa có dữ liệu; ghi `unknown` hoặc `not available`.
- Phân biệt kết quả AI tham gia với doanh thu hoặc kết quả tự nhiên.
- Mọi KPI phải có nguồn dữ liệu, công thức, owner và khoảng thời gian đo.

## 6. Tiêu chí nghiệm thu pilot

Pilot chỉ được xem là đạt khi:

1. Khách chưa xác minh không xem được thông tin đơn hàng.
2. Dữ liệu trả lời khớp nguồn được phê duyệt.
3. Connector lỗi không tạo phản hồi thành công giả.
4. Yêu cầu ngoài phạm vi được chuyển người hoặc trả lời giới hạn rõ ràng.
5. Nhân viên nhận đủ context và AI không trả lời chồng.
6. Mọi request có trace, policy decision, evidence và outcome phù hợp.
7. Không có lỗi nghiêm trọng về rò dữ liệu hoặc vượt quyền trong bộ test được duyệt.
8. Có rollback và người trực trong thời gian pilot.

## 7. Rủi ro và cách giảm thiểu

| Rủi ro | Mức độ | Biện pháp |
|---|---|---|
| Không có API đơn hàng | Cao | Dùng fake connector để hoàn thiện thiết kế; không cam kết production |
| Dữ liệu khách không đủ để xác minh | Cao | Chốt identity flow trước, cho phép human handoff |
| AI trả lời sai policy | Cao | FAQ có version/owner, evidence bắt buộc, fail closed |
| Nhân viên không nhận handoff | Cao | Chốt owner, giờ trực, SLA và escalation trước pilot |
| Lộ dữ liệu tenant/khách khác | Rất cao | Test âm tính bắt buộc, tenant filter server-side, không dùng dữ liệu thật local |
| Chi phí LLM vượt dự kiến | Trung bình | Giới hạn token, cache FAQ, đặt budget alert và quyền ngắt |
| Phạm vi phình sang Sales/Marketing | Cao | Giữ out-of-scope và Go/No-Go gate |

## 8. Quyết định cần Lead ký

- [ ] Chọn phương án pilot: A / B / C / D.
- [ ] Chọn doanh nghiệp và owner nghiệp vụ.
- [ ] Chọn kênh và hệ thống nguồn.
- [ ] Duyệt in/out scope.
- [ ] Duyệt KPI và người cung cấp baseline.
- [ ] Duyệt chính sách dữ liệu và người nhận handoff.
- [ ] Duyệt ngân sách/thời lượng Phase 0–3.
- [ ] Cho phép chuyển sang thiết kế chi tiết sau khi đủ đầu vào.

## 9. Kết luận đề xuất

Đề xuất Lead chọn **Phương án A — Order Status + Human Handoff** làm pilot đầu tiên. Đây là điểm cân bằng tốt nhất giữa giá trị thương mại, độ an toàn, khả năng tích hợp và khả năng tái sử dụng cho Sales/Marketing sau này.

Chưa bắt đầu code cho đến khi các mục bắt buộc ở mục 8 được chốt hoặc có quyết định ngoại lệ bằng văn bản.
