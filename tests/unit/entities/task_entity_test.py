from uuid import uuid4
from datetime import UTC, datetime, timedelta

import pytest

from app.domain.entities.task import Task, Priority, TaskStatus


def test_create_valid_task() -> None:
    task = Task(
        title="Write tests",
        description="Write unit tests for Task entity",
        user_id=uuid4(),
        due_date=datetime.now(tz=UTC) + timedelta(days=2),
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )

    assert task.status == TaskStatus.DRAFT
    assert task.priority == Priority.NO_PRIORITY
    assert isinstance(task.id, uuid4().__class__)
    assert task.title == "Write tests"


def test_invalid_title_too_short() -> None:
    with pytest.raises(ValueError) as exc_info:  # noqa: PT011
        Task(
            title="A",
            description="Too short title",
            user_id=uuid4(),
            due_date=datetime.now(tz=UTC),
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )
    errors = str(exc_info.value)
    assert "title" in errors
    assert "at least 2 characters" in errors


def test_invalid_description_too_long() -> None:
    with pytest.raises(ValueError) as exc_info:  # noqa: PT011
        Task(
            title="Valid Title",
            description="x" * 501,
            user_id=uuid4(),
            due_date=datetime.now(tz=UTC),
            created_at=datetime.now(tz=UTC),
            updated_at=datetime.now(tz=UTC),
        )

    errors = str(exc_info.value)
    assert "description" in errors
    assert "should have at most 500 characters" in errors


def test_task_equality_and_hash() -> None:
    uid = uuid4()
    now = datetime.now(tz=UTC)

    task1 = Task(
        title="Same title",
        description="desc 1",
        user_id=uid,
        due_date=now,
        created_at=now,
        updated_at=now,
    )

    task2 = Task(
        title="Same title",
        description="desc 2",
        user_id=uid,
        due_date=now,
        created_at=now,
        updated_at=now,
    )

    assert task1 == task2
    assert hash(task1) == hash(task2)
