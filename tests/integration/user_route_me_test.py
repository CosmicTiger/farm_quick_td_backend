from pytest_mock import MockFixture
from fastapi.testclient import TestClient

from app.domain.entities.user import User


def test_protected_route(
    test_client: TestClient,
    auth_headers: dict[str, str],
    mock_user: User,
    mocker: MockFixture,
) -> None:
    mocker.patch(
        "app.services.user_service.UserService.get_user_by_id",
        return_value=mock_user,
    )

    response = test_client.get("/api/v1/user/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
