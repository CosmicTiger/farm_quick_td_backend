from app.services.user_service import BeanieUserDatasource
from app.domain.repositories.user_repository_interface import IUserRepository


class UserRepositoryImpl(IUserRepository):
    """UserRepositoryImpl _summary_

    _extended_summary_

    :param IUserRepository: _description_
    :type IUserRepository: _type_
    :return: _description_
    :rtype: _type_
    """

    datasource: BeanieUserDatasource

    def __init__(self, datasource: BeanieUserDatasource):
        self.datasource = datasource

    async def create_user(self, user_data):
        return await self.datasource.create_user(user_data)

    async def get_user_by_id(self, user_id: str):
        return await self.datasource.get_user_by_id(user_id)

    async def find_user_by_email(self, email: str):
        return await self.datasource.find_user_by_email(email)

    async def update_user(self, user_id: str, user_data: dict):
        return await self.datasource.update_user(user_id, user_data)

    async def delete_user(self, user_id: str):
        return await self.datasource.delete_user(user_id)
