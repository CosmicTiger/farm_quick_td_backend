from uuid import uuid4

import pytest
from pytest_mock import MockFixture
from fastapi.testclient import TestClient

from app.domain.entities.task import Task
from app.domain.entities.user import User
from app.domain.entities.task_enum import Priority, TaskStatus


@pytest.fixture
def mock_task() -> Task:
    return Task(
        id=str(uuid4()),
        title="Test Task",
        description="This is a test task",
        status=TaskStatus.DRAFT,
        priority=Priority.NO_PRIORITY,
        sub_tasks=[],
        due_date=None,
        created_by_id=str(uuid4()),
    )


def test_create_task_protected(
    test_client: TestClient,
    auth_headers: dict[str, str],
    mock_user: User,
    mock_task: Task,
    mocker: MockFixture,
) -> None:
    mocker.patch(
        "app.services.user_service.UserService.get_user_by_id",
        return_value=mock_user,
    )

    response = test_client.post(
        "/api/v1/task/create",
        headers=auth_headers,
        json=mock_task.model_dump(mode="json", exclude_unset=True),
    )
    assert response.status_code == 200
    assert response.json()
