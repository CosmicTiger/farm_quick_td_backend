from uuid import UUID, uuid4

from beanie import Indexed, Document
from pydantic import Field, EmailStr


class BeanieUser(Document):
    """User _summary_

    _extended_summary_

    :param Document: _description_
    :type Document: _type_
    :return: _description_
    :rtype: _type_
    """

    id: UUID = Field(default_factory=lambda: uuid4())
    username: Indexed(str, unique=True)  # type: ignore  # noqa: PGH003
    email: Indexed(EmailStr, unique=True)  # type: ignore  # noqa: PGH003
    hashed_password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=2, max_length=20)
    last_name: str = Field(..., min_length=2, max_length=20)
    is_active: bool = Field(default=True)

    class Settings:
        """_summary_

        _extended_summary_
        """

        name = "users"
