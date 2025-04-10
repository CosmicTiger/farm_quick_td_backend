from uuid import uuid4
from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt
from fastapi.testclient import TestClient

from app.main import app
from app.core.settings import settings
from app.domain.entities.user import User


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def mock_user() -> User:
    return User(
        id=str(uuid4()),
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed1234",
        is_active=True,
    )


@pytest.fixture
def access_token(mock_user: User) -> str:
    exp = int((datetime.now(tz=UTC) + timedelta(minutes=15)).timestamp())
    payload = {"sub": str(mock_user.id), "exp": exp}

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


@pytest.fixture
def auth_headers(access_token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {access_token}"}
