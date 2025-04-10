from uuid import UUID, uuid4
from datetime import UTC, datetime

from pydantic import Field, BaseModel

from app.domain.entities.task_enum import Priority, TaskStatus, SubTaskRelationType


class SubTask(BaseModel):
    """SubTask entity"""

    id: UUID = Field(
        default_factory=lambda: uuid4(),
        title="SubTask ID",
        description="Original ID of the task in the db",
    )
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
        title="SubTask title",
        description="Original title of the task in the db",
    )
    description: str | None = Field(
        default=None,
        min_length=2,
        max_length=500,
        title="Task description",
        description="Original description of the task in the db",
    )
    due_date: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        title="Due Date",
        description="Original due date of the task in the db",
    )
    relation_type: SubTaskRelationType = Field(
        default=SubTaskRelationType.RELATES_TO,
        title="Relation Type",
        description=(
            "Relation Type:\n"
            "- block: BLOCKS - The sub task blocks the main task\n"
            "- depends_on: DEPENDS_ON - The sub task depends on the main task\n"
            "- relates_to: RELATES_TO - The sub task relates to the main task\n"
            "- duplicate: DUPLICATE - The sub task is a duplicate of the main task"
        ),
    )


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
    assigned_to: UUID = Field(default=None)
    sub_tasks: list[SubTask] = Field(default_factory=list[SubTask])
    due_date: datetime | None = Field(default_factory=lambda: datetime.now(tz=UTC))
    created_by: UUID = Field(...)
    updated_by: UUID | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

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
