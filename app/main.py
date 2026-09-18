from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.connectors.fake_erp import FakeErpConnector
from app.core.audit import InMemoryAuditStore
from app.core.policy import PolicyDenied
from app.core.tenant import TenantContextError, require_tenant_context

app = FastAPI(title="AgentOS Customer360", version="0.1.0")
erp_connector = FakeErpConnector()
audit_store = InMemoryAuditStore()


class TenantContextRequest(BaseModel):
    tenant_id: str = Field(min_length=1)
    actor_type: str = Field(min_length=1)
    actor_id: str = Field(min_length=1)
    request_id: str = Field(min_length=1)
    trace_id: str = Field(min_length=1)


class OrderLookupRequest(TenantContextRequest):
    customer_id: str = Field(min_length=1)
    order_id: str = Field(min_length=1)
    verified_customer_id: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "agentos-customer360"}


@app.post("/p1/orders/lookup")
def lookup_order(request: OrderLookupRequest) -> dict[str, object]:
    run_id = None
    try:
        context = require_tenant_context(request.model_dump())
        audit_record = audit_store.record(
            tenant_id=context.tenant_id,
            trace_id=context.trace_id,
            agent_id="CS-01",
            trigger="order.lookup.requested",
            authority="AUTH-3",
            execution_status="executing",
        )
        run_id = audit_record.run_id
        order = erp_connector.lookup_order(
            context,
            request.customer_id,
            request.order_id,
            request.verified_customer_id,
        )
        audit_store.record(
            tenant_id=context.tenant_id,
            trace_id=context.trace_id,
            agent_id="CS-01",
            trigger="order.lookup.completed",
            authority="AUTH-3",
            execution_status="success",
            evidence={"source": "fake-erp", "order_id": order.order_id},
        )
    except TenantContextError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except PolicyDenied as error:
        if run_id is not None:
            audit_store.record(
                tenant_id=request.tenant_id,
                trace_id=request.trace_id,
                agent_id="CS-01",
                trigger="order.lookup.denied",
                authority="AUTH-3",
                execution_status="denied",
                error_code="IDENTITY_VERIFICATION_REQUIRED",
            )
        raise HTTPException(
            status_code=403,
            detail={"message": str(error), "trace_id": request.trace_id, "run_id": run_id},
        ) from error
    except LookupError as error:
        audit_store.record(
            tenant_id=request.tenant_id,
            trace_id=request.trace_id,
            agent_id="CS-01",
            trigger="order.lookup.failed",
            authority="AUTH-3",
            execution_status="failed",
            error_code="ORDER_NOT_FOUND",
        )
        raise HTTPException(
            status_code=404,
            detail={"message": str(error), "trace_id": request.trace_id, "run_id": run_id},
        ) from error

    return {
        "trace_id": request.trace_id,
        "run_id": run_id,
        "tenant_id": order.tenant_id,
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "status": order.status,
        "delivery_summary": order.delivery_summary,
        "source": "fake-erp",
        "evidence": {"source": "fake-erp", "order_id": order.order_id},
    }
