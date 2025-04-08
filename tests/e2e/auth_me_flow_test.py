import pytest

from tests.utils.test_client import lifespan_test_client
from app.services.user_service import UserService
from app.schemas.pydantic.user_schemas import UserCreate


@pytest.mark.asyncio
async def test_get_current_user_authenticated() -> None:
    test_user_data = UserCreate(
        username="testuser",
        email="testuser@example.com",
        password="strongpassword123",
        first_name="Test",
        last_name="User",
    )

    async with lifespan_test_client() as client:
        # 1. Create user in the database
        user_service = UserService()

        try:
            await user_service.user_repository.find_user_by_email(
                test_user_data.email,
            )
        except ValueError:
            # User does not exist, so we can create it
            await user_service.create_user(test_user_data)

        # 2. Log in to get token
        login_response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user_data.email,
                "password": test_user_data.password,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert login_response.status_code == 200
        tokens = login_response.json()
        assert "access_token" in tokens

        # 3. Call protected route
        me_response = await client.get(
            "/api/v1/user/me",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
        )

        assert me_response.status_code == 200
        user_data = me_response.json()
        assert user_data["email"] == test_user_data.email
