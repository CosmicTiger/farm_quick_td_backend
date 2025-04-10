import pytest_asyncio
from fastapi import status

from tests.utils.test_client import lifespan_test_client
from app.domain.entities.user import User
from app.services.user_service import UserService
from tests.__mocks__.test_users_mocks import DEFAULT_TEST_USER
from app.schemas.pydantic.auth_schemas import TokenSchema
from app.schemas.pydantic.user_schemas import UserCreate


@pytest_asyncio.fixture(scope="module")
async def test_user_data() -> User:
    test_user_data = UserCreate(**DEFAULT_TEST_USER)
    test_user = None

    async with lifespan_test_client() as client:
        # User Database Instance
        user_service = UserService()

        try:
            test_user = await user_service.user_repository.find_user_by_email(
                test_user_data.email,
            )
        except ValueError:
            # User does not exist, so we can create it
            test_user = await user_service.create_user(test_user_data)

    return test_user


@pytest_asyncio.fixture(scope="module")
async def mock_tokens(test_user_data: User) -> TokenSchema:
    tokens = None

    async with lifespan_test_client() as client:
        login_response = await client.post(
            "/api/v1/auth/login",
            data={
                "username": test_user_data.email,
                "password": DEFAULT_TEST_USER["password"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert login_response.status_code == status.HTTP_200_OK
        tokens = login_response.json()
        assert "access_token" in tokens
    return TokenSchema(**tokens)
