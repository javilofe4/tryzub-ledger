from fastapi.testclient import TestClient

from ..main import app


def test_admin_endpoint_protection() -> None:
    app.dependency_overrides = {}
    client = TestClient(app)
    response = client.get("/api/v1/admin/raw-items")
    assert response.status_code == 401

    from ..core.config import settings

    previous_token = settings.ADMIN_TOKEN
    settings.ADMIN_TOKEN = "correct-token"
    try:
        response = client.get(
            "/api/v1/admin/raw-items",
            headers={"Authorization": "Bearer wrong-token"},
        )
        assert response.status_code == 403
    finally:
        settings.ADMIN_TOKEN = previous_token
