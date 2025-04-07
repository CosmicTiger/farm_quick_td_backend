from uuid import UUID, uuid4

from pydantic import Field, EmailStr, BaseModel


class User(BaseModel):
    """User entity."""

    id: UUID = Field(default_factory=lambda: uuid4())
    username: str = Field(..., min_length=2, max_length=20)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    hashed_password: str = Field(..., min_length=8)
    first_name: str = Field(..., min_length=2, max_length=20)
    last_name: str = Field(..., min_length=2, max_length=20)
    is_active: bool = Field(default=True)

    def __repr__(self) -> str:
        """__repr__ _summary_

        _extended_summary_

        :return: _description_
        :rtype: str
        """
        return f"<User(uuid={self.id}, username={self.username}, email={self.email})>"

    def __str__(self) -> str:
        """__str__ _summary_

        _extended_summary_

        :return: _description_
        :rtype: str
        """
        return self.email

    def __hash__(self) -> int:
        """__hash__ _summary_

        _extended_summary_

        :return: _description_
        :rtype: int
        """
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        """__eq__ _summary_

        _extended_summary_

        :param other: _description_
        :type other: object
        :return: _description_
        :rtype: bool
        """
        if isinstance(other, User):
            return self.email == other.email
        return False
