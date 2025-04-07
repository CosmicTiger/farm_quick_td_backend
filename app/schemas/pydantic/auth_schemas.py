from pydantic import Field, EmailStr, BaseModel


class UserAuthPayload(BaseModel):
    """UserAuthPayload schema."""

    email: EmailStr = Field(..., min_length=5, max_length=50, description="User email")
    username: str = Field(..., min_length=5, max_length=50, description="user username")
    password: str = Field(..., min_length=5, max_length=24, description="user password")


class TokenSchema(BaseModel):
    """TokenSchema schema."""

    access_token: str = Field(..., min_length=5, description="Access token")
    refresh_token: str = Field(..., min_length=5, description="Refresh token")


class TokenData(BaseModel):
    """TokenData schema."""

    uuid: str = Field(..., min_length=5, max_length=50, description="User UUID")

    def get_uuid(self) -> str:
        """Get UUID from TokenData."""
        if self.uuid:
            return self.uuid
        return None


class TokenPayload(BaseModel):
    """TokenPayload schema."""

    sub: str = Field(..., min_length=5, max_length=50, description="Subject")
    exp: int = Field(..., description="Expiration time")
