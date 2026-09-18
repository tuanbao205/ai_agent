# P0 Foundation Contracts

- **Phiên bản:** 0.1
- **Trạng thái:** Local design baseline
- **Phạm vi:** Các hợp đồng tối thiểu để triển khai P1 Customer Care Pilot
- **Không bao gồm:** Marketing, Sales, thanh toán, tự động giảm giá và connector production

Tài liệu này là bản chuẩn hóa triển khai đầu tiên. Các tài liệu SRS và platform blueprint vẫn là nguồn yêu cầu cấp cao; khi có xung đột, SRS được ưu tiên.

## 1. Nguyên tắc bất biến

1. Mọi bản ghi nghiệp vụ đều thuộc đúng một `tenant_id`.
2. ERP/POS/CRM vẫn là nguồn sự thật cho giá, tồn kho, khách hàng và đơn hàng.
3. Local chỉ dùng fake connector hoặc dữ liệu đã ẩn danh.
4. Thiếu quyền, thiếu nguồn hoặc connector lỗi thì hệ thống từ chối hoặc báo lỗi trung thực; không suy diễn thành công.
5. Mọi request xử lý phải có `trace_id`; mọi external action phải có `execution_id` và `idempotency_key`.
6. P1 chỉ bật Customer Care. Agent Marketing và Sales không được route trong P1.

## 2. Tenant boundary

Mọi request nội bộ phải mang context đã xác thực:

```json
{
  "tenant_id": "tenant-demo",
  "actor_type": "customer|agent|human|system",
  "actor_id": "actor-001",
  "request_id": "req-001",
  "trace_id": "trace-001"
}
```

Quy tắc bắt buộc:

- `tenant_id` không được lấy từ nội dung hội thoại của khách hàng.
- Repository/query phải lọc theo `tenant_id` ở server-side.
- Không cho phép dùng ID của tenant khác để đọc Customer, Conversation, Case, Event hoặc Evidence.
- Mỗi lần từ chối truy cập chéo tenant phải sinh audit event.

## 3. P1 canonical entities

### Customer

```json
{
  "tenant_id": "tenant-demo",
  "customer_id": "customer-001",
  "display_name": "string",
  "contact": { "email": "string|null", "phone_hash": "string|null" },
  "lifecycle_status": "new|active|at_risk|inactive",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

### Customer Identity

```json
{
  "tenant_id": "tenant-demo",
  "identity_id": "identity-001",
  "customer_id": "customer-001",
  "identity_type": "session|email|phone|external_id",
  "identity_hash": "string",
  "verified_at": "ISO-8601|null",
  "verification_method": "otp|signed_session|manual|null"
}
```

Không lưu plaintext phone/email trong audit log. Chỉ identity đã xác minh mới được dùng để tra cứu dữ liệu riêng tư.

### Consent

```json
{
  "tenant_id": "tenant-demo",
  "customer_id": "customer-001",
  "purpose": "service|marketing",
  "status": "granted|denied|withdrawn|unknown",
  "source": "web|import|operator",
  "updated_at": "ISO-8601"
}
```

P1 chỉ dùng `service` consent cho hỗ trợ. Không phát sinh marketing consent từ việc khách cung cấp số điện thoại giao hàng.

### Conversation

```json
{
  "tenant_id": "tenant-demo",
  "conversation_id": "conversation-001",
  "channel": "web|line|fake",
  "customer_id": "customer-001|null",
  "control_mode": "ai|human|waiting_human",
  "status": "open|waiting_customer|waiting_human|resolved|closed",
  "trace_id": "trace-001",
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

Một conversation chỉ có một bên được phép gửi phản hồi nghiệp vụ tại một thời điểm. `control_mode=human` phải chặn AI reply.

### Service Case

```json
{
  "tenant_id": "tenant-demo",
  "case_id": "case-001",
  "conversation_id": "conversation-001",
  "customer_id": "customer-001",
  "intent": "faq|order_status|delivery|return|complaint|human_request|unknown",
  "priority": "low|normal|high|urgent",
  "status": "new|classified|assigned|in_progress|waiting_customer|resolved|closed",
  "owner_id": "human-001|null",
  "evidence_ids": ["evidence-001"],
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

### Evidence

```json
{
  "tenant_id": "tenant-demo",
  "evidence_id": "evidence-001",
  "run_id": "run-001",
  "kind": "fact|signal|hypothesis|decision|action",
  "source_type": "faq|erp|wms|operator|system",
  "source_ref": "faq-version-001|order-001",
  "payload_hash": "sha256:...",
  "observed_at": "ISO-8601",
  "created_at": "ISO-8601"
}
```

`HYPOTHESIS` không được ghi đè thành `FACT`. Connector lỗi không tạo evidence loại `fact`.

### Agent Run

```json
{
  "tenant_id": "tenant-demo",
  "run_id": "run-001",
  "trace_id": "trace-001",
  "agent_id": "CS-01",
  "trigger": "message.received",
  "authority": "AUTH-0|AUTH-1|AUTH-2|AUTH-3|AUTH-4|AUTH-5",
  "execution_status": "pending|executing|success|failed|denied|aborted",
  "skill_id": "skill.care.classify_intent",
  "error_code": "string|null",
  "started_at": "ISO-8601",
  "completed_at": "ISO-8601|null"
}
```

## 4. P1 skill contracts

### `skill.care.classify_intent`

- **Allowed agent:** `CS-01`
- **Authority:** `AUTH-1`
- **Input:** `tenant_id`, `conversation_id`, `message_text`
- **Output:** `intent`, `confidence`, `reason`, `evidence_ids`
- **Deny conditions:** missing tenant context, empty message, unsupported conversation
- **Side effect:** none

### `skill.care.verify_identity`

- **Allowed agent:** `CS-01`
- **Authority:** `AUTH-3`
- **Input:** `tenant_id`, `conversation_id`, `verification_method`, `verification_value`
- **Output:** `verified`, `customer_id|null`, `evidence_id`
- **Deny conditions:** mismatched tenant, expired session, failed verification
- **Side effect:** records verification attempt; never exposes order data by itself

### `skill.care.lookup_order`

- **Allowed agent:** `CS-01`
- **Authority:** `AUTH-3`
- **Input:** `tenant_id`, `customer_id`, `order_id`
- **Output:** `status`, `delivery_summary`, `source_ref`, `evidence_id`
- **Precondition:** identity verified for the same tenant and customer
- **Failure rule:** ERP/WMS error returns `failed`; it never returns a guessed status

### `skill.care.create_case`

- **Allowed agent:** `CS-01`
- **Authority:** `AUTH-3`
- **Input:** `tenant_id`, `conversation_id`, `customer_id`, `intent`, `priority`, `summary`
- **Output:** `case_id`, `status`, `owner_id|null`
- **Idempotency:** same `tenant_id + conversation_id + unresolved intent` does not create duplicate active cases

### `skill.care.human_handoff`

- **Allowed agent:** `CS-01`
- **Authority:** `AUTH-3`
- **Input:** `tenant_id`, `conversation_id`, `case_id`, `reason`, `summary`
- **Output:** `control_mode=waiting_human`, `queue_item_id`
- **Safety rule:** AI must stop sending operational replies after handoff until explicit human resume

## 5. Minimum P0 acceptance checks

| ID | Check | Expected result |
|---|---|---|
| P0-001 | Request không có `tenant_id` | `DENY`, audit event được ghi |
| P0-002 | Đọc Customer của tenant khác | `DENY`, không trả dữ liệu |
| P0-003 | Lookup order chưa verify | `DENY`, không gọi connector |
| P0-004 | Connector trả lỗi | `failed`, không ghi success/fact giả |
| P0-005 | Retry cùng idempotency key | Không tạo case hoặc external effect thứ hai |
| P0-006 | Conversation ở human control mode | AI không được gửi reply nghiệp vụ |
| P0-007 | Route yêu cầu Sales trong P1 | Từ chối hoặc chuyển human, không gọi Sales |
| P0-008 | Evidence hypothesis | Không được lưu dưới loại `fact` |

## 6. Trạng thái và bước tiếp theo

- **Đã khóa local:** tenant boundary, P1 entity contract, skill boundary và acceptance checks tối thiểu.
- **Chưa khóa:** công nghệ triển khai, database engine, API transport, pilot tenant và connector thật.
- **Bước kế tiếp:** chốt stack và tạo local skeleton có health check, test runner và fake connector; không kết nối production.
