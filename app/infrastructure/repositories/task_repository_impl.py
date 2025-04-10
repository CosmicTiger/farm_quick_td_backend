from app.domain.repositories.task_repository_interface import ITaskRepository
from app.infrastructure.datasource.beanie_task_datasource import BeanieTaskDatasource


class TaskRepositoryImpl(ITaskRepository):
    """TaskRepositoryImpl _summary_

    _extended_summary_

    :param ITaskRepository: _description_
    :type ITaskRepository: _type_
    :return: _description_
    :rtype: _type_
    """

    datasource: BeanieTaskDatasource

    def __init__(self, datasource: BeanieTaskDatasource):
        self.datasource = datasource

    async def create_task(self, current_user, task_data):
        return await self.datasource.create_task(current_user, task_data)

    async def get_task_by_id(self, task_id: str):
        return await self.datasource.get_task_by_id(task_id)

    async def find_task_by_name(self, name: str):
        return await self.datasource.find_task_by_name(name)

    async def list_my_created_tasks(self, current_user):
        return await self.datasource.list_my_created_tasks(current_user)

    async def list_my_assigned_tasks(self, current_user):
        return await self.datasource.list_my_assigned_tasks(current_user)

    async def list_tasks(self, task_filters: dict | None, task_sorts: list[str] | None, page: int, offset: int):
        return await self.datasource.list_tasks(task_filters, task_sorts, page, offset)

    async def list_tasks_by_filter(self, task_filter):
        return await self.datasource.list_tasks_by_filter(task_filter)

    async def update_task(self, current_user, task_id: str, task_data: dict):
        return await self.datasource.update_task(current_user, task_id, task_data)

    async def delete_task(self, task_id: str):
        return await self.datasource.delete_task(task_id)
