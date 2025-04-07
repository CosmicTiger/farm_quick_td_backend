from pydantic import Field, EmailStr, BaseModel


class UserCreate(BaseModel):
    """UserCreate schema."""

    username: str = Field(..., min_length=2, max_length=20, description="User username")
    email: EmailStr = Field(..., min_length=5, max_length=50, description="User email")
    first_name: str = Field(..., min_length=2, max_length=20, description="First name of the person of this user")
    last_name: str = Field(..., min_length=2, max_length=20, description="Last name of the person of this user")


class UserUpdatePassword(BaseModel):
    """UserUpdatePassword schema."""

    current_password: str = Field(..., min_length=8, max_length=24, description="Current password")
    new_password: str = Field(..., min_length=8, max_length=24, description="New password")
    new_password_confirm: str = Field(..., min_length=8, max_length=24, description="New password confirmation")


class UserUpdate(BaseModel):
    """UserUpdate schema."""

    username: str | None = Field(None, min_length=2, max_length=20, description="User username")
    email: EmailStr | None = Field(None, min_length=5, max_length=50, description="User email")
    first_name: str | None = Field(
        None,
        min_length=2,
        max_length=20,
        description="First name of the person of this user",
    )
    last_name: str | None = Field(None, min_length=2, max_length=20, description="Last name of the person of this user")


class UserRead(BaseModel):
    """UserRead schema."""

    username: str
    email: str
    first_name: str
    last_name: str
