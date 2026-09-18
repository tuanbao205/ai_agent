from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass(frozen=True)
class AuditRecord:
    run_id: str
    tenant_id: str
    trace_id: str
    agent_id: str
    trigger: str
    authority: str
    execution_status: str
    evidence: dict[str, str] = field(default_factory=dict)
    error_code: str | None = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )


class InMemoryAuditStore:
    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def record(
        self,
        *,
        tenant_id: str,
        trace_id: str,
        agent_id: str,
        trigger: str,
        authority: str,
        execution_status: str,
        evidence: dict[str, str] | None = None,
        error_code: str | None = None,
    ) -> AuditRecord:
        audit_record = AuditRecord(
            run_id=f"run-{uuid4().hex}",
            tenant_id=tenant_id,
            trace_id=trace_id,
            agent_id=agent_id,
            trigger=trigger,
            authority=authority,
            execution_status=execution_status,
            evidence=evidence or {},
            error_code=error_code,
        )
        self._records.append(audit_record)
        return audit_record

    def find_by_trace(self, trace_id: str) -> list[AuditRecord]:
        return [record for record in self._records if record.trace_id == trace_id]
