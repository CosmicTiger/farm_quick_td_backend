from uuid import uuid4
from datetime import UTC, datetime

import pytest

from app.domain.entities.task_enum import Priority, TaskStatus, SubTaskRelationType
from app.infrastructure.models.odm.beanie_task_model import BeanieTask, BeanieSubTask
from app.infrastructure.models.odm.beanie_user_model import BeanieUser

now = datetime.now(tz=UTC)


@pytest.fixture
def mock_user() -> BeanieUser:
    return BeanieUser(
        id=uuid4(),
        email="test@example.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password="hashed1234",
        is_active=True,
    )


@pytest.fixture
def mock_subtask() -> BeanieTask:
    return BeanieTask(
        title="Example SubTask",
        description="This is a test sub task",
        status=TaskStatus.DRAFT,
        priority=Priority.HIGH,
        is_archived=False,
        assigned_user_id=mock_user,
        sub_tasks=[],
        due_date=now,
        created_by=mock_user,
        updated_by_id=mock_user,
        created_at=now,
        updated_at=now,
    )


def test_beanie_subtask_creation() -> None:
    subtask = BeanieSubTask(relation_type=SubTaskRelationType.BLOCKS)
    assert subtask.relation_type == SubTaskRelationType.BLOCKS
    assert isinstance(subtask.id, uuid4().__class__)


def test_beanie_task_creation(mock_user: BeanieUser) -> None:
    task = BeanieTask(
        title="Example Task",
        description="This is a test task",
        status=TaskStatus.DRAFT,
        priority=Priority.HIGH,
        is_archived=False,
        assigned_user_id=mock_user,
        sub_tasks=[BeanieSubTask()],
        due_date=now,
        created_by=mock_user,
        updated_by_id=mock_user,
        created_at=now,
        updated_at=now,
    )

    assert task.title == "Example Task"
    assert task.status == TaskStatus.DRAFT
    assert isinstance(task.sub_tasks, list)
    assert isinstance(task.created_by, BeanieUser)
    assert isinstance(task.updated_by_id, BeanieUser)
    assert task.created_at.tzinfo == UTC
    assert task.updated_at.tzinfo == UTC

    task.save()
