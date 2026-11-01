from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from api.main import app


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def _login_for_token(client: TestClient, username: str, password: str) -> str:
    response = client.post(
        "/auth/token",
        data={"username": username, "password": password},
    )
    assert response.status_code == 200, response.text
    return response.json()["access_token"]


def test_health_endpoint(client: TestClient) -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_games_list_returns_page_shape(client: TestClient) -> None:
    response = client.get("/games", params={"limit": 5, "offset": 0})

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"items", "total", "limit", "offset"}
    assert payload["limit"] == 5
    assert payload["offset"] == 0
    assert isinstance(payload["items"], list)
    assert len(payload["items"]) <= 5


def test_auth_token_success_includes_expiry_fields(client: TestClient) -> None:
    response = client.post(
        "/auth/token",
        data={"username": "fakeuser", "password": "password"},
    )

    assert response.status_code == 200
    payload = response.json()

    assert "access_token" in payload
    assert payload["token_type"] == "bearer"
    assert isinstance(payload["expires_in"], int)
    assert 1 <= payload["expires_in"] <= 3600

    expires_at = datetime.fromisoformat(payload["expires_at"].replace("Z", "+00:00"))
    seconds_left = (expires_at - datetime.now(timezone.utc)).total_seconds()
    assert seconds_left > 0


def test_auth_token_invalid_credentials(client: TestClient) -> None:
    response = client.post(
        "/auth/token",
        data={"username": "fakeuser", "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_delete_requires_token(client: TestClient) -> None:
    response = client.delete("/games/999999")

    assert response.status_code == 401


def test_delete_requires_admin_role(client: TestClient) -> None:
    token = _login_for_token(client, "fakeuser", "password")

    response = client.delete(
        "/games/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"


def test_delete_with_admin_token_returns_404(client: TestClient) -> None:
    login = client.post(
        "/auth/token",
        data={"username": "admin", "password": "adminpassword"},
    )
    if login.status_code != 200:
        pytest.skip("Admin seed user not available; run database/reset.py to create it.")

    token = login.json()["access_token"]
    response = client.delete(
        "/games/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    # 404 confirms auth/authorization passed and endpoint logic executed.
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"
