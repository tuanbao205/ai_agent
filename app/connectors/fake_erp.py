from dataclasses import dataclass

from app.core.policy import PolicyDenied
from app.core.tenant import TenantContext


@dataclass(frozen=True)
class FakeOrder:
    tenant_id: str
    order_id: str
    customer_id: str
    status: str
    delivery_summary: str


class FakeErpConnector:
    def __init__(self) -> None:
        self._orders = {
            ("tenant-demo", "order-001"): FakeOrder(
                tenant_id="tenant-demo",
                order_id="order-001",
                customer_id="customer-001",
                status="in_transit",
                delivery_summary="Expected delivery tomorrow",
            )
        }

    def lookup_order(
        self,
        context: TenantContext,
        customer_id: str,
        order_id: str,
        verified_customer_id: str | None,
    ) -> FakeOrder:
        if verified_customer_id != customer_id:
            raise PolicyDenied("Identity verification is required")

        order = self._orders.get((context.tenant_id, order_id))
        if order is None or order.customer_id != customer_id:
            raise LookupError("Order not found")
        return order
