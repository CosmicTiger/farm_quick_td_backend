from typing import Annotated

from jose import jwt
from fastapi import Depends, Request, APIRouter, HTTPException, status
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token, create_refresh_token, verify_refresh_token
from app.domain.entities.user import User
from app.services.user_service import UserService
from app.schemas.pydantic.auth_schemas import TokenSchema, TokenPayload
from app.api.routers.dependencies.user_deps import get_current_user

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
    dependencies=[],
)


@auth_router.post("/login", summary="Sign in user")
async def login(
    service: Annotated[UserService, Depends()],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    """Sign in user.

    Args:
        user (dict): User data.

    Returns:
        dict: Sign-in response.
    """
    try:
        user = await service.authenticate_user(form_data.username, form_data.password)
        if not user:
            return None
        return  {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }
    except Exception as error:
        print(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error


@auth_router.post("/test-token", summary="Test if the access token is valid")
async def test_token(user: Annotated[User, Depends(get_current_user)]):
    return user


@auth_router.post("/refresh", summary="Refresh token")
# @limiter.limit("5/minute")
async def refresh_token(
    request: Request,
    refresh_token: str,
    service: Annotated[UserService, Depends()],
) -> TokenSchema:
    """Refresh token.

    Args:
        token (str): Token to refresh.

    Returns:
        dict: Refreshed token.
    """
    try:
        payload = verify_refresh_token(refresh_token)

        token_data = TokenPayload(**payload)
        user = await service.get_user_by_id(token_data.sub)

        if not user:
            raise Exception("Invalid token for user")  # noqa: TRY301, TRY002

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }
    except (jwt.JWTError, ValidationError) as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user",
            headers={"WWW-Authenticate": "Bearer"},
        ) from error
