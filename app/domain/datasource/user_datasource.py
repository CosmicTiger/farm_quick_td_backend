from abc import ABC, abstractmethod

from app.domain.entities.user import User
from app.schemas.pydantic.user_schemas import UserCreate


class IUserDatasource(ABC):
    """IUserDatasource _summary_

    _extended_summary_

    :param ABC: _description_
    :type ABC: _type_
    """

    @abstractmethod
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user with the provided data."""
        raise NotImplementedError

    @abstractmethod
    def get_user_by_id(self, user_id: str) -> User:
        """Fetch a user by their ID."""
        raise NotImplementedError

    @abstractmethod
    def find_user_by_email(self, email: str) -> User:
        """Fetch a user by their email address."""
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user_id: str, user_data: dict) -> User:
        """Update an existing user's information."""
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id: str) -> User:
        """Delete a user by their ID."""
        raise NotImplementedError
