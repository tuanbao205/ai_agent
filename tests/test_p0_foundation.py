from fastapi.testclient import TestClient

from app.main import app, audit_store

client = TestClient(app)


BASE_CONTEXT = {
    "tenant_id": "tenant-demo",
    "actor_type": "customer",
    "actor_id": "customer-001",
    "request_id": "request-001",
    "trace_id": "trace-001",
    "customer_id": "customer-001",
    "order_id": "order-001",
}


def test_health_check() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_order_lookup_requires_identity_verification() -> None:
    response = client.post("/p1/orders/lookup", json=BASE_CONTEXT)

    assert response.status_code == 403
    assert response.json()["detail"]["message"] == "Identity verification is required"
    assert response.json()["detail"]["trace_id"] == "trace-001"
    assert audit_store.find_by_trace("trace-001")[-1].execution_status == "denied"


def test_order_lookup_succeeds_after_identity_verification() -> None:
    response = client.post(
        "/p1/orders/lookup",
        json={**BASE_CONTEXT, "verified_customer_id": "customer-001"},
    )

    assert response.status_code == 200
    assert response.json()["trace_id"] == "trace-001"
    assert response.json()["run_id"].startswith("run-")
    assert response.json()["evidence"]["source"] == "fake-erp"
    assert response.json()["source"] == "fake-erp"
    assert response.json()["status"] == "in_transit"


def test_order_lookup_cannot_cross_tenant() -> None:
    response = client.post(
        "/p1/orders/lookup",
        json={
            **BASE_CONTEXT,
            "tenant_id": "tenant-other",
            "verified_customer_id": "customer-001",
        },
    )

    assert response.status_code == 404
