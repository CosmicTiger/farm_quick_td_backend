from datetime import datetime
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from fastapi import status
from fastapi.encoders import jsonable_encoder

from tests.utils.test_client import lifespan_test_client
from app.domain.entities.task import Priority
from app.domain.entities.user import User
from tests.__mocks__.test_task import TEST_TASK_1
from app.domain.entities.task_enum import TaskStatus
from app.schemas.pydantic.auth_schemas import TokenSchema
from app.schemas.pydantic.task_schemas import TaskCreate, TaskUpdate

endpoint_rooth_path = "/api/v1/task"
endpoint_responses = None


@pytest_asyncio.fixture(scope="module")
async def created_task_flow(test_user_data: User, mock_tokens: TokenSchema) -> AsyncGenerator[dict, None]:
    test_task = TaskCreate(**TEST_TASK_1)
    endpoint_rooth_path = "/api/v1/task"
    endpoint_responses = None

    async with lifespan_test_client() as client:
        encoding_payload = jsonable_encoder(test_task)
        endpoint_responses = await client.post(
            f"{endpoint_rooth_path}/create",
            headers={"Authorization": f"Bearer {mock_tokens.access_token}"},
            json=encoding_payload,
        )
        assert endpoint_responses.status_code == status.HTTP_200_OK
        endpoint_responses = endpoint_responses.json()
        assert endpoint_responses["message"] == "Task created successfully."
        assert endpoint_responses["result"]["title"] == test_task.title
        assert endpoint_responses["result"]["description"] == test_task.description
        assert endpoint_responses["result"]["status"] == test_task.status
        assert endpoint_responses["result"]["priority"] == test_task.priority
        assert isinstance(endpoint_responses["result"]["sub_tasks"], list)
        assert endpoint_responses["result"]["due_date"] == test_task.due_date.strftime(
            "%Y-%m-%dT%H:%M:%S.%fZ",
        )
        assert endpoint_responses["result"]["assigned_to"] == test_task.assigned_to
        assert endpoint_responses["result"]["created_by"]["username"] == test_user_data.username
        assert endpoint_responses["result"]["created_by"]["email"] == test_user_data.email
        assert endpoint_responses["result"]["updated_by"] is None
        assert endpoint_responses["result"]["created_at"] is not None
        assert endpoint_responses["result"]["updated_at"] is not None

        yield {
            "task_data": endpoint_responses["result"],
            "task_id": endpoint_responses["result"]["id"],
        }

    async with lifespan_test_client() as client:
        delete_response = await client.delete(
            f"{endpoint_rooth_path}/{endpoint_responses['result']['id']}",
            headers={"Authorization": f"Bearer {mock_tokens.access_token}"},
        )
        assert delete_response.status_code == status.HTTP_200_OK
        delete_response = delete_response.json()
        assert delete_response["message"] == "Task deleted successfully."


@pytest.mark.asyncio
async def test_get_retrieve_task_endpoint(
    test_user_data: User,
    mock_tokens: TokenSchema,
    created_task_flow: dict,
) -> None:
    task_id = created_task_flow["task_id"]

    async with lifespan_test_client() as client:
        endpoint_responses = await client.get(
            f"{endpoint_rooth_path}/read/{task_id}",
            headers={"Authorization": f"Bearer {mock_tokens.access_token}"},
        )
        assert endpoint_responses.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_put_update_task_endpoint(
    test_user_data: User,
    mock_tokens: TokenSchema,
    created_task_flow: dict,
) -> None:
    task_id = created_task_flow["task_id"]
    new_data = {
        "title": "🗄️ Backend - E2E Updated Test Task A",
        "description": "Updated description",
        "status": TaskStatus.IN_PROGRESS.value,
        "priority": Priority.HIGH.value,
        "due_date": None,
        "assigned_to": test_user_data.id,
    }
    test_task = TaskUpdate(**new_data)

    async with lifespan_test_client() as client:
        encoding_payload = jsonable_encoder(test_task)
        endpoint_responses = await client.put(
            f"{endpoint_rooth_path}/{task_id}",
            headers={"Authorization": f"Bearer {mock_tokens.access_token}"},
            json=encoding_payload,
        )
        assert endpoint_responses.status_code == status.HTTP_200_OK
        endpoint_responses = endpoint_responses.json()
        assert endpoint_responses["message"] == "Task updated successfully."
        assert endpoint_responses["result"]["title"] != created_task_flow["task_data"]["title"]
        assert endpoint_responses["result"]["title"] == test_task.title
        assert endpoint_responses["result"]["description"] == test_task.description
        assert endpoint_responses["result"]["status"] == test_task.status
        assert endpoint_responses["result"]["priority"] == test_task.priority
        assert endpoint_responses["result"]["sub_tasks"] == test_task.sub_tasks
        assert not isinstance(endpoint_responses["result"]["due_date"], datetime)
        assert endpoint_responses["result"]["due_date"] is None
        assert endpoint_responses["result"]["assigned_to"] != test_task.assigned_to
        assert endpoint_responses["result"]["created_by"]["username"] == test_user_data.username
        assert endpoint_responses["result"]["created_by"]["email"] == test_user_data.email
        assert endpoint_responses["result"]["updated_by"] is not None
        assert endpoint_responses["result"]["created_by"]["username"] == test_user_data.username
        assert endpoint_responses["result"]["created_by"]["email"] == test_user_data.email
        assert endpoint_responses["result"]["created_at"] is not None
        assert endpoint_responses["result"]["updated_at"] is not None
