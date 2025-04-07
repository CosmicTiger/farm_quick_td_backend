from uuid import UUID, uuid4
from datetime import datetime

from pydantic import Field, BaseModel

from app.domain.entities.task_enum import Priority, TaskStatus, SubTaskRelationType


class SubTask(BaseModel):
    """SubTask entity."""

    id: UUID = Field(default_factory=lambda: uuid4())
    relation_type: str = Field(default=SubTaskRelationType.RELATES_TO)


class Task(BaseModel):
    """Task entity."""

    id: UUID = Field(default_factory=lambda: uuid4())
    title: str = Field(..., min_length=2, max_length=100)
    description: str = Field(
        ...,
        min_length=2,
        max_length=500,
        description="Task description",
    )
    status: TaskStatus = Field(default=TaskStatus.DRAFT)
    priority: Priority = Field(default=Priority.NO_PRIORITY)
    is_archived: bool = Field(default=False)
    user_id: UUID = Field(...)
    assigned_user_id: UUID = Field(default=None)
    sub_tasks: list[SubTask] = Field(default_factory=list[SubTask])
    due_date: datetime = Field(...)
    created_at: datetime = Field(...)
    updated_at: datetime = Field(...)

    def __repr__(self) -> str:
        """__repr__ _summary_

        _extended_summary_

        :return: _description_
        :rtype: str
        """
        return f"<Task(uuid={self.id}, title={self.title}, status={self.status})>"

    def __str__(self) -> str:
        """__str__ _summary_

        _extended_summary_

        :return: _description_
        :rtype: str
        """
        return self.title

    def __hash__(self) -> int:
        """__hash__ _summary_

        _extended_summary_

        :return: _description_
        :rtype: int
        """
        return hash(self.title)

    def __eq__(self, other: object) -> bool:
        """__eq__ _summary_

        _extended_summary_

        :param other: _description_
        :type other: object
        :return: _description_
        :rtype: bool
        """
        if isinstance(other, Task):
            return self.title == other.title
        return False
