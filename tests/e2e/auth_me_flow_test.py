import pytest
from fastapi import status

from tests.utils.test_client import lifespan_test_client
from app.domain.entities.user import User
from app.schemas.pydantic.auth_schemas import TokenSchema


@pytest.mark.asyncio
async def test_get_current_user_authenticated(test_user_data: User, mock_tokens: TokenSchema) -> None:
    async with lifespan_test_client() as client:
        me_response = await client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {mock_tokens.access_token}"},
        )

        assert me_response.status_code == status.HTTP_200_OK
        user_data = me_response.json()
        assert user_data["email"] == test_user_data.email
