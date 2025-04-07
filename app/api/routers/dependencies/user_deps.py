from typing import Annotated
from datetime import UTC, datetime

from jose import jwt
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer

from app.core import get_settings
from app.domain.entities.user import User
from app.services.user_service import UserService
from app.schemas.pydantic.auth_schemas import TokenPayload

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl=f"{get_settings().get_api_prefix}/auth/login",
    scheme_name="JWT",
    description="JWT Bearer Token",
)

print(f"{get_settings().get_api_prefix}/auth/login")


async def get_current_user(
    service: Annotated[UserService, Depends()],
    token: Annotated[str, Depends(oauth2_bearer)],
) -> User:
    try:
        payload = jwt.decode(
            token,
            get_settings().JWT_SECRET_KEY,
            algorithms=[get_settings().JWT_ALGORITHM],
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp, tz=UTC) < datetime.now(tz=UTC):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWTError, ValidationError) as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error

    user = await service.get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
