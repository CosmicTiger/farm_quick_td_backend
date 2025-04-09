from pymongo.errors import OperationFailure, DuplicateKeyError

from app.core.logger import logger
from app.domain.entities.user import User
from app.schemas.pydantic.user_schemas import UserCreate
from app.domain.datasource.user_datasource import IUserDatasource
from app.infrastructure.mappers.user_mapper import (
    to_beanie_user_from_entity_user,
    to_entity_user_from_schema_create_user,
)
from app.infrastructure.models.odm.beanie_user_model import BeanieUser


class BeanieUserDatasource(IUserDatasource):
    """BeanieUserDatasource _summary_

    _extended_summary_

    :param IUserDatasource: _description_
    :type IUserDatasource: _type_
    """

    async def create_user(self, data: UserCreate) -> User:
        """create_user _summary_

        _extended_summary_

        :param data: _description_
        :type data: UserCreate
        :raises OperationFailure: _description_
        :return: _description_
        :rtype: User
        """
        try:
            data_to_user = to_entity_user_from_schema_create_user(data)
            user = to_beanie_user_from_entity_user(data_to_user)
            await user.save()
            return user
        except DuplicateKeyError:
            raise ValueError("Username already exists") from DuplicateKeyError
        except Exception as e:
            msg = f"Failed to create user: {e}"
            logger.error(msg)
            raise OperationFailure(msg) from e

    async def get_user_by_id(self, user_id: str) -> User | None:
        return await BeanieUser.get(user_id)

    async def find_user_by_email(self, email: str) -> User | None:
        user = await BeanieUser.find_one(BeanieUser.email == email)

        if not user:
            raise ValueError("User not found")

        return user

    async def find_all(self) -> list[User]:
        return await BeanieUser.find_all().to_list()

    async def update_user(self, user_id: str, user_data: dict) -> User | None:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise OperationFailure("User not found")

        clean_user_data_to_update = user_data.model_dump(exclude_unset=True, exclude_none=True)
        await user.update({"$set": clean_user_data_to_update})
        return user

    async def delete_user(self, user_id: str) -> bool:
        user = await self.get_user_by_id(user_id)
        if not user:
            raise OperationFailure("User not found")

        await user.update({"$set": {"is_active": not user.is_active}})
        return user.is_active
