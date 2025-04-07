from datetime import UTC, datetime

from jose import jwt
from fastapi import Depends, HTTPException, status
from pydantic import ValidationError

from app.core import get_settings
from app.core.security import oauth2_bearer
from app.domain.entities.user import User
from app.services.user_service import UserService
from app.schemas.pydantic.auth_schemas import TokenPayload


async def get_current_user(token: str = Depends(oauth2_bearer)) -> User:
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

    user = await UserService().get_user_by_id(token_data.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return user
