import pymongo
from pymongo.errors import OperationFailure, DuplicateKeyError

from app.core.logger import logger
from app.domain.entities.user import User
from app.schemas.pydantic.task_schemas import TaskRead, TaskCreate
from app.domain.datasource.task_datasource import ITaskDatasource
from app.infrastructure.mappers.task_mapper import to_beanie_task_from_schema_task_create
from app.infrastructure.models.odm.beanie_task_model import BeanieTask
from app.infrastructure.datasource.build_filters_datasource import LOGICAL_OPERATOR_MAPPING


class BeanieTaskDatasource(ITaskDatasource):
    """BeanieTaskDatasource _summary_

    _extended_summary_

    :param ITaskDatasource: _description_
    :type ITaskDatasource: _type_
    """

    async def create_task(self, current_user: User, task_data: TaskCreate) -> TaskRead:
        """create_task _summary_

        _extended_summary_

        :param task_data: _description_
        :type task_data: TaskRead
        :raises OperationFailure: _description_
        :return: _description_
        :rtype: Task
        """
        try:
            task = await to_beanie_task_from_schema_task_create(task_data, current_user)
            await task.insert()
            task.sub_tasks = await task.retrieve_sub_tasks()
            return task
        except DuplicateKeyError:
            raise ValueError("Task already exists") from DuplicateKeyError
        except Exception as e:
            msg = f"Failed to create task: {e}"
            logger.error(msg)
            raise OperationFailure(msg) from e

    async def get_task_by_id(self, task_id) -> TaskRead:
        try:
            task = await BeanieTask.get(task_id, fetch_links=True)
            if not task:
                raise ValueError("Task not found")  # noqa: TRY301

            task.sub_tasks = await task.retrieve_sub_tasks()
            return task
        except ValueError as e:
            msg = f"Failed to get task by ID: {e}"
            logger.error(msg)
            raise
        except Exception as e:
            msg = f"Failed to get task by ID: {e}"
            logger.error(msg)
            raise OperationFailure(msg) from e

    async def find_task_by_name(self, name: str) -> TaskRead:
        task = await BeanieTask.find_one(BeanieTask.name == name)

        if not task:
            raise ValueError("Task not found")

        return task

    async def list_tasks(
        self,
        task_filters: dict | None,
        task_sorts: list[str] | None,
        page: int,
        offset: int,
    ) -> list[TaskRead]:
        """list_tasks _summary_

        _extended_summary_

        :param task_filters: _description_
        :type task_filters: dict
        :param task_sorts: _description_
        :type task_sorts: dict
        :param page: _description_
        :type page: int
        :param offset: _description_
        :type offset: int
        :raises OperationFailure: _description_
        :raises OperationFailure: _description_
        :return: _description_
        :rtype: list[TaskRead]
        """
        try:
            # Apply sorting
            sorting_to_apply = (
                [
                    (BeanieTask.created_at, pymongo.DESCENDING),
                ]
                if not task_sorts or len(task_sorts) == 0
                else task_sorts
            )

            # Filters to apply
            task_filters_to_apply = (
                LOGICAL_OPERATOR_MAPPING[task_filters["logical_operator"]](
                    *task_filters["expression"],
                )
                if task_filters
                else None
            )

            tasks = (
                await BeanieTask.find_all(sort=sorting_to_apply, skip=page, limit=offset, fetch_links=True).to_list()
                if task_filters is None
                else await BeanieTask.find(
                    task_filters_to_apply,
                    sort=sorting_to_apply,
                    skip=page,
                    limit=offset,
                    fetch_links=True,
                ).to_list()
            )
            return tasks
        except OperationFailure as e:
            msg = f"Failed to list tasks: {e}"
            logger.error(msg)
            raise OperationFailure(msg) from e
        except Exception as e:
            msg = f"Failed to list tasks: {e}"
            logger.error(msg)
            raise OperationFailure(msg) from e

    async def update_task(self, task_id: str, task_data: dict) -> TaskRead:
        """update_task _summary_

        _extended_summary_

        :param task_id: _description_
        :type task_id: str
        :param task_data: _description_
        :type task_data: dict
        :raises OperationFailure: _description_
        :return: _description_
        :rtype: _type_
        """
        task = await self.get_task_by_id(task_id)
        if not task:
            raise OperationFailure("Task not found")

        task_data_to_update = {}

        if task_data.get("is_archived_process"):
            task_data_to_update["is_archived"] = task.is_archived

        task_data_to_update = {
            **task_data_to_update,
            **task_data,
        }

        task.update(**task_data_to_update)
        await task.save()
        return task

    async def delete_task(self, task_id: str) -> TaskRead:
        """delete_task _summary_

        _extended_summary_

        :param task_id: _description_
        :type task_id: str
        :raises OperationFailure: _description_
        :return: _description_
        :rtype: _type_
        """
        task = await self.get_task_by_id(task_id)
        if not task:
            raise OperationFailure("Task not found")

        await task.delete()
        return task
