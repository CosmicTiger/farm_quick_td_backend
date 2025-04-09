from app.core.logger import logger
from app.domain.entities.user import User
from app.schemas.pydantic.task_schemas import TaskRead, TaskCreate, TaskUpdate
from app.schemas.pydantic.common_schemas import FilterCapabilities
from app.infrastructure.datasource.beanie_task_datasource import BeanieTaskDatasource
from app.infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from app.infrastructure.datasource.build_filters_datasource import build_beanie_filter


class TaskService:
    """_summary_

    _extended_summary_
    """

    task_repository = TaskRepositoryImpl

    def __init__(self) -> None:
        """__init__ _summary_

        _extended_summary_
        """
        self.task_repository = TaskRepositoryImpl(BeanieTaskDatasource())

    async def create_task(self, current_user: User, task_data: TaskCreate) -> TaskRead:
        """create_task _summary_

        _extended_summary_

        :param task_data: _description_
        :type task_data: dict
        :return: _description_
        :rtype: dict
        """
        try:
            new_task = await self.task_repository.create_task(current_user, task_data)
            return new_task
        except Exception as e:
            msg = f"[TaskService] - Task creation failed, error: {e}"
            logger.error(msg)
            raise

    async def list_my_assigned_tasks(self, current_user: User) -> list[TaskRead]:
        """list_my_assigned_tasks _summary_

        _extended_summary_

        :param current_user: _description_
        :type current_user: User
        :return: _description_
        :rtype: list[TaskRead]
        """

    async def list_tasks(
        self,
        task_filters: FilterCapabilities | None,
        task_sorts: list[str] | None,
        page: int,
        offset: int,
    ) -> list[TaskRead]:
        """list_tasks _summary_

        _extended_summary_

        :return: _description_
        :rtype: list[TaskRead]
        """
        try:
            tasks = await self.task_repository.list_tasks(
                build_beanie_filter(task_filters) if task_filters else None,
                task_sorts,
                page,
                offset,
            )
            return tasks
        except Exception as e:
            msg = f"[TaskService] - Task listing failed, error: {e}"
            logger.error(msg)
            raise

    async def get_task_by_id(self, task_id: str) -> TaskRead:
        """get_task_by_id _summary_

        _extended_summary_

        :param task_id: _description_
        :type task_id: str
        :raises ValueError: _description_
        :return: _description_
        :rtype: TaskRead
        """
        try:
            task = await self.task_repository.get_task_by_id(task_id)
            return task
        except Exception as e:
            msg = f"[TaskService] - Task retrieval failed, error: {e}"
            logger.error(msg)
            raise

    async def find_task_by_name(self, name: str) -> TaskRead:
        """find_task_by_name _summary_

        _extended_summary_

        :param name: _description_
        :type name: str
        :raises ValueError: _description_
        :return: _description_
        :rtype: TaskRead
        """
        try:
            task = await self.task_repository.find_task_by_name(name)
            return task
        except Exception as e:
            msg = f"[TaskService] - Task retrieval by name failed, error: {e}"
            logger.error(msg)
            raise

    async def update_task(self, task_id: str, current_user: User, task_data: TaskUpdate) -> TaskRead:
        """update_task _summary_

        _extended_summary_

        :param task_id: _description_
        :type task_id: str
        :param task_data: _description_
        :type task_data: TaskUpdate
        :return: _description_
        :rtype: TaskRead
        """
        try:
            task = await self.task_repository.update_task(current_user, task_id, task_data)
            return task
        except Exception as e:
            msg = f"[TaskService] - Task update failed, error: {e}"
            logger.error(msg)
            raise

    async def archive_task(self, task_id: str, current_user: User) -> TaskRead:
        """archive_task _summary_

        _extended_summary_

        :param task_id: _description_
        :type task_id: str
        :return: _description_
        :rtype: TaskRead
        """
        try:
            task = await self.task_repository.update_task(current_user, task_id)
            return task
        except Exception as e:
            msg = f"[TaskService] - Task archiving failed, error: {e}"
            logger.error(msg)
            raise

    async def delete_task(self, task_id: str) -> TaskRead:
        """delete_task _summary_

        _extended_summary_

        :param task_id: _description_
        :type task_id: str
        :return: _description_
        :rtype: TaskRead
        """
        try:
            task = await self.task_repository.delete_task(task_id)
            return task
        except Exception as e:
            msg = f"[TaskService] - Task deletion failed, error: {e}"
            logger.error(msg)
            raise
