from app.core.logger import logger
from app.core.security import get_password, verify_password
from app.domain.entities.user import User
from app.schemas.pydantic.user_schemas import UserRead, UserCreate, UserUpdate, UserUpdatePassword
from app.infrastructure.mappers.user_mapper import to_entity_user_from_beanie_user
from app.infrastructure.datasource.beanie_user_datasource import BeanieUserDatasource
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl


class UserService:
    """_summary_

    _extended_summary_

    :raises ValueError: _description_
    :raises ValueError: _description_
    :return: _description_
    :rtype: _type_
    """

    user_repository: UserRepositoryImpl

    def __init__(self) -> None:
        """__init__ _summary_

        _extended_summary_
        """
        self.user_repository = UserRepositoryImpl(BeanieUserDatasource())

    # async def validate_user_data(self, user_data: UserCreate) -> None:
    #     if not user_data.email or not user_data.password:
    #         raise ValueError("Email and password are required.")

    # async def check_user_exists(self, email: str) -> None:
    #     existing_user = await self.user_repository.get_user_by_email(email)
    #     if existing_user:
    #         raise ValueError("User already exists.")

    async def create_user(self, user_data: UserCreate) -> UserRead:
        """create_user _summary_

        _extended_summary_

        :param user_data: _description_
        :type user_data: UserCreate
        :return: _description_
        :rtype: UserRead
        """
        # await self.validate_user_data(user_data)
        # await self.check_user_exists(user_data.email)
        try:
            new_user = await self.user_repository.create_user(user_data)
            return new_user
        except Exception as e:
            msg = f"[UserService] - User creation failed, error: {e}"
            logger.error(msg)
            raise

    async def get_user_by_id(self, user_id: str) -> User:
        """get_user_by_id _summary_

        _extended_summary_

        :param user_id: _description_
        :type user_id: str
        :raises ValueError: _description_
        :return: _description_
        :rtype: User
        """
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")  # noqa: TRY301
            return to_entity_user_from_beanie_user(user)
        except Exception as e:
            msg = f"[UserService] - User retrieval failed, error: {e}"
            logger.error(msg)
            raise

    async def authenticate_user(self, email: str, password: str) -> User:
        """authenticate_user _summary_

        _extended_summary_

        :param email: _description_
        :type email: str
        :param password: _description_
        :type password: str
        :return: _description_
        :rtype: UserRead
        """
        try:
            user = await self.user_repository.find_user_by_email(email)

            if not user or not verify_password(password, user.hashed_password):
                logger.warning(f"[UserService] - Failed authentication attempt for: {email}")
                raise ValueError("Invalid credentials")  # noqa: TRY301

            return to_entity_user_from_beanie_user(user)
        except Exception as e:
            msg = f"[UserService] - User authentication failed, error: {e}"
            logger.error(msg)
            raise

    async def find_user_by_email(self, email: str) -> User:
        """find_user_by_email _summary_

        _extended_summary_

        :param email: _description_
        :type email: str
        :raises ValueError: _description_
        :return: _description_
        :rtype: User
        """
        try:
            user = await self.user_repository.find_user_by_email(email)

            if not user:
                logger.warning(f"[UserService] - User not found with: {email}")
                raise ValueError("User not found")  # noqa: TRY301

            return to_entity_user_from_beanie_user(user)
        except Exception as e:
            msg = f"[UserService] - User search by email failed, error: {e}"
            logger.error(msg)
            raise

    async def update_user_password(self, user_id: str, new_password_payload: UserUpdatePassword) -> bool:
        """update_user_password _summary_

        _extended_summary_

        :param new_password_payload: _description_
        :type new_password_payload: UserUpdate
        :return: _description_
        :rtype: bool
        """
        try:
            user = await self.user_repository.get_user_by_id(user_id)
            if not user:
                raise ValueError("User not found")  # noqa: TRY301

            if not verify_password(new_password_payload.current_password, user.hashed_password):
                logger.warning(f"[UserService] - Failed password update attempt for: {user.email}")
                raise ValueError("Invalid old password")  # noqa: TRY301
            if new_password_payload.new_password != new_password_payload.new_password_confirm:
                logger.warning(f"[UserService] - Passwords do not match for: {user.email}")
                raise ValueError("Passwords do not match")  # noqa: TRY301

            user.hashed_password = get_password(new_password_payload.new_password)

            return await self.user_repository.update_user(user_id, to_entity_user_from_beanie_user(user))
        except Exception as e:
            msg = f"[UserService] - User password update failed, error: {e}"
            logger.error(msg)
            raise

    async def update_user(self, user_id: str, user_data: UserUpdate) -> UserRead:
        try:
            updated_user = await self.user_repository.update_user(user_id, user_data)
            return updated_user
        except Exception as e:
            msg = f"[UserService] - User update failed, error: {e}"
            logger.error(msg)
            raise

    async def delete_user(self, user_id: str) -> bool:
        """delete_user _summary_

        _extended_summary_

        :param user_id: _description_
        :type user_id: str
        :return: _description_
        :rtype: bool
        """
        try:
            return await self.user_repository.delete_user(user_id)
        except Exception as e:
            msg = f"[UserService] - User deletion/restore failed, error: {e}"
            logger.error(msg)
            raise
