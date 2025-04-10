from uuid import UUID
from datetime import UTC, datetime

from pydantic import Field, BaseModel

from app.domain.entities.task import SubTask
from app.domain.entities.task_enum import Priority, TaskStatus
from app.schemas.pydantic.user_schemas import UserRead
from app.schemas.pydantic.common_schemas import ValueDescriptionToFilter
from app.utils.enums.filter_capabilities_enum import (
    FilterOperatorsNumberEnum,
    FilterOperatorsStringAndBooleanEnum,
)
from app.infrastructure.models.odm.beanie_task_model import BeanieSubTask
from app.infrastructure.models.odm.beanie_user_model import BeanieUser


class TaskCreate(BaseModel):
    """TaskCreate schema

    Schema that handles the creation of the task.

    :param BaseModel: based on the pydantic BaseModel
    """

    title: str = Field(..., title="Title", max_length=55, min_length=1, description="Title of the task")
    description: str = Field(..., title="Title", max_length=755, min_length=1, description="Description of the task")
    status: TaskStatus = Field(
        default=TaskStatus.DRAFT,
        title="Status",
        description=(
            "Enum to represent the current state of the Task:\n"
            "- 0: DRAFT - The task is in draft state in order to be edited later\n"
            "- 1: BACKLOG - The task is in the backlog and should be done later\n"
            "- 2: TODO - The task is in the TODO list and should be done\n"
            "- 3: IN_PROGRESS - The task is in progress and should be done\n"
            "- 4: BLOCKER - The task is blocked and should be done later\n"
            "- 5: DONE - The task is done and should be archived\n"
            "- 6: CANCELLED - The task is cancelled and should be archived\n"
            "- 7: DUPLICATE - The task is a duplicate of another task and should be archived"
        ),
    )
    priority: Priority = Field(
        default=Priority.NO_PRIORITY,
        title="Priority",
        description=(
            "Enum to represent the priority that the Task has:\n"
            "- 0: NO_PRIORITY - The task has no priority over the board\n"
            "- 1: URGENT - The task is urgent and should be done as soon as possible\n"
            "- 2: HIGH - The task is high priority and should be done as soon as possible\n"
            "- 3: MEDIUM - The task is medium priority and should be done as soon as possible\n"
            "- 4: LOW - The task is low priority and should be done as soon as possible"
        ),
    )
    sub_tasks: list[SubTask] = Field(
        default=[],
        title="Sub Tasks",
        description="List of sub tasks",
    )
    due_date: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        title="Due Date",
        description="Due date for the task",
    )
    assigned_to: UUID | None = Field(
        default=None,
        title="Assigned To",
        description="User ID to whom the task is assigned",
    )


class TaskCreateWithMetadata(BaseModel):
    """TaskCreateWithMetadata schema

    Schema that handles the creation of the task parsed within the process.

    :param BaseModel: based on the pydantic BaseModel
    """

    title: str = Field(..., title="Title", max_length=55, min_length=1)
    description: str = Field(..., title="Title", max_length=755, min_length=1)
    status: TaskStatus = Field(default=TaskStatus.DRAFT, title="Status")
    priority: Priority = Field(default=Priority.NO_PRIORITY, title="Priority")
    is_archived: bool = Field(default=False, title="Is Archived")
    sub_tasks: list[BeanieSubTask] = Field(
        default=[],
        title="Sub Tasks",
        description="List of sub tasks",
    )
    due_date: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        title="Due Date",
        description="Due date for the task",
    )
    assigned_to: BeanieUser | None = Field(
        default=None,
        title="Assigned To",
        description="User ID to whom the task is assigned",
    )
    created_by: BeanieUser = Field(
        ...,
        title="Created By",
        description="User ID of the creator",
    )
    updated_by: BeanieUser | None = Field(
        default=None,
        title="Updated By",
        description="User ID of the last updater",
    )


class TaskUpdate(BaseModel):
    """TaskUpdate schema

    Schema that handles the update of the task.

    :param BaseModel: based on the pydantic BaseModel
    """

    title: str = Field(default=None, title="Title", max_length=55, min_length=1, description="Title of the task")
    description: str | None = Field(
        default=None,
        title="Description",
        max_length=755,
        min_length=1,
        description="Description of the task",
    )
    status: TaskStatus | None = Field(
        default=None,
        title="Status",
        description=(
            "Enum to represent the current state of the Task:\n"
            "- 0: DRAFT - The task is in draft state in order to be edited later\n"
            "- 1: BACKLOG - The task is in the backlog and should be done later\n"
            "- 2: TODO - The task is in the TODO list and should be done\n"
            "- 3: IN_PROGRESS - The task is in progress and should be done\n"
            "- 4: BLOCKER - The task is blocked and should be done later\n"
            "- 5: DONE - The task is done and should be archived\n"
            "- 6: CANCELLED - The task is cancelled and should be archived\n"
            "- 7: DUPLICATE - The task is a duplicate of another task and should be archived"
        ),
    )
    priority: Priority | None = Field(
        default=None,
        title="Priority",
        description=(
            "Enum to represent the priority that the Task has:\n"
            "- 0: NO_PRIORITY - The task has no priority over the board\n"
            "- 1: URGENT - The task is urgent and should be done as soon as possible\n"
            "- 2: HIGH - The task is high priority and should be done as soon as possible\n"
            "- 3: MEDIUM - The task is medium priority and should be done as soon as possible\n"
            "- 4: LOW - The task is low priority and should be done as soon as possible"
        ),
    )
    sub_tasks: list[SubTask] | None = Field(
        default=[],
        title="Sub Tasks",
        description="List of sub tasks",
    )
    due_date: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        title="Due Date",
        description="Due date for the task",
    )
    assigned_to: UUID | None = Field(
        default=None,
        title="Assigned To",
        description="User ID to whom the task is assigned",
    )


class TaskRead(BaseModel):
    """TaskRead schema."""

    id: UUID = Field(..., title="Task ID", description="Task ID")
    title: str = Field(..., title="Title", max_length=55, min_length=1, description="Title of the task")
    description: str = Field(..., title="Title", max_length=755, min_length=1, description="Description of the task")
    status: TaskStatus = Field(
        default=TaskStatus.DRAFT,
        title="Status",
        description=(
            "Enum to represent the current state of the Task:\n"
            "- 0: DRAFT - The task is in draft state in order to be edited later\n"
            "- 1: BACKLOG - The task is in the backlog and should be done later\n"
            "- 2: TODO - The task is in the TODO list and should be done\n"
            "- 3: IN_PROGRESS - The task is in progress and should be done\n"
            "- 4: BLOCKER - The task is blocked and should be done later\n"
            "- 5: DONE - The task is done and should be archived\n"
            "- 6: CANCELLED - The task is cancelled and should be archived\n"
            "- 7: DUPLICATE - The task is a duplicate of another task and should be archived"
        ),
    )
    priority: Priority = Field(
        default=Priority.NO_PRIORITY,
        title="Priority",
        description=(
            "Enum to represent the priority that the Task has:\n"
            "- 0: NO_PRIORITY - The task has no priority over the board\n"
            "- 1: URGENT - The task is urgent and should be done as soon as possible\n"
            "- 2: HIGH - The task is high priority and should be done as soon as possible\n"
            "- 3: MEDIUM - The task is medium priority and should be done as soon as possible\n"
            "- 4: LOW - The task is low priority and should be done as soon as possible"
        ),
    )
    is_archived: bool = Field(default=False, title="Is Archived", description="If the task is archived")
    sub_tasks: list[SubTask] = Field(
        default_factory=list,
        title="Sub Tasks",
        description="List of sub tasks",
    )
    due_date: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        title="Due Date",
        description="Due date for the task",
    )
    assigned_to: UserRead | None = Field(
        default=None,
        title="Assigned To",
        description="User ID to whom the task is assigned",
    )
    created_by: UserRead = Field(
        ...,
        title="Created By",
        description="User ID of the creator",
    )
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        title="Date of creation",
        description="Date of creation of the task",
    )
    updated_by: UserRead | None = Field(
        default=None,
        title="Updated By",
        description="User ID of the last updater",
    )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=UTC),
        title="Date of last update",
        description="Date of last update of the task",
    )


class TaskFilters(BaseModel):
    """TaskFilters schema

    Schema that handles the filters for the task.
    It is used in the pagination options to filter the tasks.

    :param BaseModel: based on the pydantic BaseModel
    """

    status: (
        ValueDescriptionToFilter[
            TaskStatus | list[TaskStatus],
            FilterOperatorsNumberEnum,
        ]
        | None
    ) = Field(
        default=None,
        title="Status",
        description="Filter tasks by status",
    )
    priority: (
        ValueDescriptionToFilter[
            Priority | list[Priority],
            FilterOperatorsNumberEnum,
        ]
        | None
    ) = Field(
        default=None,
        title="Priority",
        description="Filter tasks by priority",
    )
    assigned_to: (
        ValueDescriptionToFilter[
            UUID | list[UUID],
            FilterOperatorsStringAndBooleanEnum,
        ]
        | None
    ) = Field(
        default=None,
        title="Assigned To",
        description="User ID to whom the task is assigned",
    )
    is_archived: ValueDescriptionToFilter[bool, FilterOperatorsStringAndBooleanEnum] | None = Field(
        default=None,
        title="Is Archived",
        description="Filter tasks by archived status",
    )
    # due_date: (
    #     FilterCapabilities[datetime, FilterOperatorsDateEnum, datetime | None, FilterOperatorsDateEnum | None] | None
    # ) = Field(
    #     default=None,
    #     title="Status",
    # )
    # created_by: (
    #     FilterCapabilities[
    #         UUID | list[UUID],
    #         FilterOperatorsStringAndBooleanEnum,
    #         UUID | list[UUID] | None,
    #         FilterOperatorsStringAndBooleanEnum | None,
    #     ]
    #     | None
    # ) = Field(
    #     default=None,
    #     title="Created By",
    #     description="User ID of the creator",
    # )
    # created_at: (
    #     FilterCapabilities[datetime, FilterOperatorsDateEnum, datetime | None, FilterOperatorsDateEnum | None] | None
    # ) = Field(
    #     default=None,
    #     title="Date of creation",
    #     description="Date of creation of the task",
    # )
    # updated_at: (
    #     FilterCapabilities[datetime, FilterOperatorsDateEnum, datetime | None, FilterOperatorsDateEnum | None] | None
    # ) = Field(
    #     default=None,
    #     title="Date of last update",
    #     description="Date of last update of the task",
    # )

    def to_filter_fields(self) -> list[ValueDescriptionToFilter]:
        """to_filter_fields _summary_

        _extended_summary_

        :return: _description_
        :rtype: list[ValueDescriptionToFilter]
        """
        return list(self.model_dump(exclude_none=True).values())

    # def build_task_query(self) -> dict:
    #     """build_task_query _summary_

    #     _extended_summary_

    #     :return: _description_
    #     :rtype: dict
    #     """
    #     task_query = {}
    #     for field, filter_capability in self:
    #         if filter_capability:
    #             task_query[field] = filter_capability.build_filter()
    #     return task_query
