from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import secrets
import uuid

import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from api.dependencies import require_admin
from api.main import app
from database.db import get_db


@dataclass
class MockIdentity:
    username: str
    password: str
    admin_username: str
    admin_password: str


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_identity() -> MockIdentity:
    return MockIdentity(
        username=f"user_{uuid.uuid4().hex[:8]}",
        password=secrets.token_urlsafe(12),
        admin_username=f"admin_{uuid.uuid4().hex[:8]}",
        admin_password=secrets.token_urlsafe(14),
    )


@pytest.fixture
def mock_users(mocker, mock_identity: MockIdentity):
    non_admin = mocker.Mock(
        username=mock_identity.username,
        hashed_password="mock-hash-user",
        full_name="Mock User",
        disabled=False,
        is_admin=False,
    )
    admin = mocker.Mock(
        username=mock_identity.admin_username,
        hashed_password="mock-hash-admin",
        full_name="Mock Admin",
        disabled=False,
        is_admin=True,
    )
    return {"user": non_admin, "admin": admin}


@pytest.fixture(autouse=True)
# Clear dependency overrides before and after each test so that tests do not interfere with each other and reset after each test
def clear_dependency_overrides():
    app.dependency_overrides.clear()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def mock_db(mocker, mock_users):
    db = mocker.Mock()

    # Used by games endpoint
    games = [
        SimpleNamespace(id=i, title=f"Mock Game {i}", console="Mock Console")
        for i in range(1, 6)
    ]
    # mocks rows in a database
    db.scalar.return_value = len(games)

    # mocks the result of db.scalars().all()
    scalar_result = mocker.Mock()
    scalar_result.all.return_value = games
    db.scalars.return_value = scalar_result

    # Used by auth endpoint
    query_result = mocker.Mock()
    # mocks the result of db.query().filter().first()
    query_result.filter.return_value = query_result
    query_result.first.return_value = mock_users["user"]
    db.query.return_value = query_result

    # Used by delete endpoint
    # mocks the result of db.get()
    db.get.return_value = None

    return db


@pytest.fixture
def override_db(mock_db):
    def _override_get_db():
        # yield allows the function to return a value and later resume where it left off
        yield mock_db

    # Override the get_db dependency from database.db with the mock database instead
    app.dependency_overrides[get_db] = _override_get_db


@pytest.fixture
def mock_auth_functions(mocker, mock_identity: MockIdentity):
    def _verify_password(raw: str, _hashed: str) -> bool:
        return raw in {mock_identity.password, mock_identity.admin_password}

    def _create_access_token(subject: str) -> str:
        return f"token-for-{subject}"

    def _decode_access_token(token: str) -> dict:
        username = token.replace("token-for-", "")
        exp = int((datetime.now(timezone.utc) + timedelta(minutes=30)).timestamp())
        return {"sub": username, "exp": exp}

    # mocker.patch replaces the specified function with a mock that can have its behavior controlled in tests
    mocker.patch("api.routers.auth.verify_password", side_effect=_verify_password)
    mocker.patch("api.routers.auth.create_access_token", side_effect=_create_access_token)
    mocker.patch("api.routers.auth.decode_access_token", side_effect=_decode_access_token)


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


def test_games_list_returns_page_shape(client: TestClient, override_db) -> None:
    response = client.get("/games", params={"limit": 5, "offset": 0})

    assert response.status_code == 200
    payload = response.json()
    assert set(payload.keys()) == {"items", "total", "limit", "offset"}
    assert payload["limit"] == 5
    assert payload["offset"] == 0
    assert isinstance(payload["items"], list)
    assert len(payload["items"]) <= 5


def test_auth_token_success_includes_expiry_fields(
    client: TestClient,
    override_db,
    mock_auth_functions,
    mock_identity: MockIdentity,
) -> None:
    response = client.post(
        "/auth/token",
        data={"username": mock_identity.username, "password": mock_identity.password},
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


def test_auth_token_invalid_credentials(
    client: TestClient,
    override_db,
    mock_auth_functions,
    mock_identity: MockIdentity,
) -> None:
    response = client.post(
        "/auth/token",
        data={"username": mock_identity.username, "password": "definitely-not-correct"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_delete_requires_token(client: TestClient) -> None:
    response = client.delete("/games/999999")

    assert response.status_code == 401


def test_delete_requires_admin_role(
    client: TestClient,
    override_db,
    mock_auth_functions,
    mock_identity: MockIdentity,
    mock_users,
):
    token = _login_for_token(client, mock_identity.username, mock_identity.password)

    def _deny_admin():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )

    app.dependency_overrides[require_admin] = _deny_admin

    response = client.delete(
        "/games/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin privileges required"


def test_delete_with_admin_token_returns_404(
    client: TestClient,
    override_db,
    mock_auth_functions,
    mock_identity: MockIdentity,
    mock_users,
):
    token = _login_for_token(
        client,
        mock_identity.admin_username,
        mock_identity.admin_password,
    )

    def _allow_admin():
        return mock_users["admin"]

    app.dependency_overrides[require_admin] = _allow_admin

    response = client.delete(
        "/games/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    # 404 confirms auth/authorization passed and endpoint logic executed
    assert response.status_code == 404
    assert response.json()["detail"] == "Game not found"
