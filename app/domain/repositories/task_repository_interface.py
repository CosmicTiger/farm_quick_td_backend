from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entities.task import Task
from app.domain.entities.user import User
from app.schemas.pydantic.task_schemas import TaskCreate


class ITaskRepository(ABC):
    """ITaskRepository _summary_

    _extended_summary_

    :param ABC: _description_
    :type ABC: _type_
    """

    @abstractmethod
    def create_task(self, current_user: User, task_data: TaskCreate) -> Task:
        """create_task _summary_

        _extended_summary_

        :param task_data: _description_
        :type task_data: TaskCreate
        :raises NotImplementedError: _description_
        :return: _description_
        :rtype: Task
        """
        raise NotImplementedError

    @abstractmethod
    def get_task_by_id(self, task_id: UUID) -> Task:
        """get_task_by_id _summary_

        _extended_summary_

        :param task_id: _description_
        :type task_id: UUID
        :raises NotImplementedError: _description_
        :return: _description_
        :rtype: Task
        """
        raise NotImplementedError

    @abstractmethod
    def find_task_by_name(self, name: str) -> Task:
        """find_task_by_name _summary_

        _extended_summary_

        :param name: _description_
        :type name: str
        :raises NotImplementedError: _description_
        :return: _description_
        :rtype: Task
        """
        raise NotImplementedError

    @abstractmethod
    def list_tasks(self, task_filters: dict, task_sorts: dict, page: int, offset: int) -> list[Task]:
        """list_tasks _summary_

        _extended_summary_

        :raises NotImplementedError: _description_
        :return: _description_
        :rtype: list[Task]
        """
        raise NotImplementedError

    @abstractmethod
    def update_task(self, current_user: User, task_id: UUID, task_data_to_update: dict) -> Task:
        """update_task _summary_

        _extended_summary_

        :param current_user: _description_
        :type current_user: str
        :param task_id: _description_
        :type task_id: UUID
        :param task_data_to_update: _description_
        :type task_data_to_update: dict
        :raises NotImplementedError: _description_
        :return: _description_
        :rtype: Task
        """
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, user_id: UUID, task_id: UUID) -> Task:
        """delete_task _summary_

        _extended_summary_

        :param user_id: _description_
        :type user_id: UUID
        :param task_id: _description_
        :type task_id: UUID
        :raises NotImplementedError: _description_
        :return: _description_
        :rtype: Task
        """
        raise NotImplementedError
