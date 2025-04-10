from uuid import UUID, uuid4
from datetime import UTC, datetime

from beanie import Link, Insert, Indexed, Replace, Document, before_event
from pydantic import Field, BaseModel

from app.core.logger import logger
from app.domain.entities.task import SubTask
from app.domain.entities.task_enum import Priority, TaskStatus, SubTaskRelationType
from app.infrastructure.models.odm.beanie_user_model import BeanieUser


class BeanieSubTask(BaseModel):
    """BeanieSubTask _summary_

    _extended_summary_

    :param BaseModel: _description_
    :type BaseModel: _type_
    """

    id: UUID = Field(default_factory=uuid4)
    relation_type: SubTaskRelationType = Field(default=SubTaskRelationType.RELATES_TO)


class BeanieTask(Document):
    """BeanieTask _summary_

    _extended_summary_

    :param Document: _description_
    :type Document: _type_
    :return: _description_
    :rtype: _type_
    """

    id: UUID = Field(default_factory=uuid4, unique=True)
    title: Indexed(str)  # type: ignore  # noqa: PGH003
    description: str = Field(max_length=500)
    status: TaskStatus = TaskStatus.DRAFT
    priority: Priority = Priority.NO_PRIORITY
    is_archived: bool = False
    assigned_to: Link[BeanieUser] | None = None
    sub_tasks: list[BeanieSubTask] = Field(default=[])
    due_date: datetime | None = Field(default_factory=lambda: datetime.now(tz=UTC))
    created_by: Link[BeanieUser]
    updated_by: Link[BeanieUser] | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(tz=UTC))

    @before_event([Replace, Insert])
    def update_updated_at(self) -> None:
        """update_updated_at _summary_

        _extended_summary_
        """
        self.updated_at = datetime.now(tz=UTC)

    @classmethod
    async def validate_sub_tasks(cls, sub_tasks: list[SubTask]) -> list[BeanieSubTask]:
        """validate_sub_tasks _summary_

        _extended_summary_

        :param sub_tasks: _description_
        :type sub_tasks: list[SubTask]
        :return: _description_
        :rtype: list[SubTask]
        """
        try:
            validated_sub_tasks = []
            for sub_task in sub_tasks:
                sub_task_id = sub_task.get("id", None)
                sub_task_validation = await cls.get(sub_task_id) if sub_task_id else None
                if not sub_task_validation:
                    msg = f"Subtask with ID {sub_task_id} not found"
                    logger.warning(msg)
                validated_sub_tasks.append(
                    {
                        "id": sub_task_validation.id,
                        "relation_type": sub_task.get("relation_type", SubTaskRelationType.RELATES_TO),
                    },
                )
            return validated_sub_tasks
        except Exception as error:
            msg = f"[BeanieTask] - Subtask validation failed, error: {error}"
            logger.error(msg)
            raise

    async def retrieve_sub_tasks(self) -> list[BeanieSubTask]:
        """validate_sub_tasks _summary_

        _extended_summary_

        :param sub_tasks: _description_
        :type sub_tasks: list[SubTask]
        :return: _description_
        :rtype: list[SubTask]
        """
        try:
            retrieved_sub_tasks = []
            for sub_task in self.sub_tasks:
                sub_task_id = sub_task.id
                sub_task_found = await self.get(sub_task_id) if sub_task_id else None
                if not sub_task_found:
                    msg = f"Subtask with ID {sub_task_id} not found"
                    logger.warning(msg)
                retrieved_sub_tasks.append(
                    {
                        "id": sub_task_found.id,
                        "title": sub_task_found.title,
                        "description": sub_task_found.description,
                        "due_date": sub_task_found.due_date,
                        "relation_type": sub_task.relation_type,
                    },
                )
            return retrieved_sub_tasks
        except Exception as error:
            msg = f"[BeanieTask] - Subtask validation failed, error: {error}"
            logger.error(msg)
            raise

    class Settings:
        """_summary_

        _extended_summary_
        """

        name = "tasks"

    def __repr__(self) -> str:
        return f"<BeanieTask(title={self.title}, status={self.status})>"
