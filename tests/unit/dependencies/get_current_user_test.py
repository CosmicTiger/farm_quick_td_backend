from uuid import uuid4
from datetime import UTC, datetime, timedelta

import pytest
from jose import jwt
from pytest_mock import MockerFixture

from app.core import get_settings
from app.domain.entities.user import User
from app.services.user_service import UserService
from app.api.routers.dependencies.user_deps import get_current_user


@pytest.mark.asyncio
async def test_get_current_user_valid_token(mocker: MockerFixture) -> None:
    # Arrange
    settings = get_settings()
    raw_mock_id = uuid4()
    user_id = str(raw_mock_id)
    now = datetime.now(tz=UTC)
    exp = int((now + timedelta(minutes=30)).timestamp())

    token = jwt.encode(
        {"sub": user_id, "exp": exp},
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    mock_user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed123",
        is_active=True,
    )

    mock_service = mocker.Mock(spec=UserService)
    mock_service.get_user_by_id.return_value = mock_user

    # Mocking the JWT decode function
    result = await get_current_user(mock_service, token)

    # Assert
    assert result.id == raw_mock_id
    assert result.username == "testuser"
    mock_service.get_user_by_id.assert_called_once_with(user_id)
