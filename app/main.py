from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.connectors.fake_erp import FakeErpConnector
from app.core.policy import PolicyDenied
from app.core.tenant import TenantContextError, require_tenant_context

app = FastAPI(title="AgentOS Customer360", version="0.1.0")
erp_connector = FakeErpConnector()


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
    try:
        context = require_tenant_context(request.model_dump())
        order = erp_connector.lookup_order(
            context,
            request.customer_id,
            request.order_id,
            request.verified_customer_id,
        )
    except TenantContextError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except PolicyDenied as error:
        raise HTTPException(status_code=403, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error

    return {
        "tenant_id": order.tenant_id,
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "status": order.status,
        "delivery_summary": order.delivery_summary,
        "source": "fake-erp",
    }
