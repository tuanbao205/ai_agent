from dataclasses import dataclass


@dataclass(frozen=True)
class TenantContext:
    tenant_id: str
    actor_type: str
    actor_id: str
    request_id: str
    trace_id: str


class TenantContextError(ValueError):
    pass


def require_tenant_context(payload: dict[str, object]) -> TenantContext:
    required_fields = ("tenant_id", "actor_type", "actor_id", "request_id", "trace_id")
    missing_fields = [field for field in required_fields if not payload.get(field)]
    if missing_fields:
        raise TenantContextError(
            f"Missing tenant context: {', '.join(missing_fields)}"
        )

    return TenantContext(
        tenant_id=str(payload["tenant_id"]),
        actor_type=str(payload["actor_type"]),
        actor_id=str(payload["actor_id"]),
        request_id=str(payload["request_id"]),
        trace_id=str(payload["trace_id"]),
    )
