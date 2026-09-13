from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_service_info() -> None:
    response = client.get("/api/v1/info")
    assert response.status_code == 200
    assert response.json()["runtime"] == "Python + FastAPI"


def test_item_endpoint() -> None:
    response = client.get("/api/v1/items/42")
    assert response.status_code == 200
    assert response.json()["id"] == 42


def test_invalid_item_id() -> None:
    response = client.get("/api/v1/items/0")
    assert response.status_code == 400


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests_total" in response.text
