from typing import Annotated

from fastapi import Depends, Request, APIRouter, HTTPException, status
from pydantic import ValidationError

from app.main import logger
from app.core.rate_limiting import limiter
from app.domain.entities.user import User
from app.services.user_service import UserService
from app.schemas.pydantic.user_schemas import UserRead, UserCreate, UserUpdate, UserUpdatePassword
from app.schemas.pydantic.common_schemas import CommonResponse
from app.api.routers.dependencies.user_deps import get_current_user

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
    dependencies=[],
)


@user_router.post(
    "/create",
    summary="Create user",
    response_description="User information",
)
@limiter.limit("5/hour")
async def create_user(request: Request, user_data: UserCreate, service: Annotated[UserService, Depends()]) -> UserRead:
    """create_user _summary_

    _extended_summary_

    :param request: _description_
    :type request: Request used for rate limiting, already processed passively
    :param user_data: Payload of the user to be created
    :type user_data: UserCreate
    :raises HTTPException: _description_
    :raises HTTPException: _description_
    :return: _description_
    :rtype: UserRead
    """
    try:
        return await service.create_user(user_data)
    except ValidationError as validation_error:
        msg = f"User creation failed, validation error: {validation_error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_error.errors(),
            headers={"X-Error": "User creation failed"},
        ) from validation_error
    except Exception as error:
        msg = f"User creation failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User creation failed",
            headers={"X-Error": "User creation failed"},
        ) from error


@user_router.get(
    "/me",
    summary="Get user information",
    response_description="User information",
    response_model=dict,
)
async def get_me(current_user: Annotated[User, Depends(get_current_user)]) -> UserRead:
    """Get user information.

    Returns:
        dict: User information.
    """
    return current_user.model_dump(exclude={"password", "hashed_password"})


@user_router.patch(
    "/update_password/{user_id}",
    summary="Update user password",
    response_description="User password updated successfully",
)
@limiter.limit("2/hour")
async def update_user_password(
    request: Request,
    user_id: str,
    new_password_payload: UserUpdatePassword,
    service: Annotated[UserService, Depends()],
) -> dict:
    """Update user password.

    Args:
        user_data (UserCreate): User data.

    Returns:
        dict: User password updated successfully.
    """
    try:
        result = await service.update_user_password(user_id, new_password_payload)
        return {"message": "User password updated successfully" if result else "User password update failed"}
    except ValidationError as validation_error:
        msg = f"User password update failed, validation error: {validation_error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_error.errors(),
            headers={"X-Error": "User password update failed"},
        ) from validation_error
    except Exception as error:
        msg = f"User password update failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User password update failed",
            headers={"X-Error": "User password update failed"},
        ) from error


@user_router.put(
    "/update/{user_id}",
    summary="Update user information",
    response_description="User information updated successfully",
)
@limiter.limit("1/hour")
async def update_user_info(
    request: Request,
    user_id: str,
    user_data: UserUpdate,
    service: Annotated[UserService, Depends()],
) -> CommonResponse[UserRead]:
    try:
        updated_user = await service.update_user(user_id, user_data)
        return {"message": "User information updated successfully", "result": updated_user}
    except ValidationError as validation_error:
        msg = f"User update failed, validation error: {validation_error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_error.errors(),
            headers={"X-Error": "User update failed"},
        ) from validation_error
    except Exception as error:
        msg = f"User update failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User update failed",
            headers={"X-Error": "User update failed"},
        ) from error


@user_router.patch(
    "/delete/{user_id}",
    summary="Change user logical status",
    response_description="User information restored/deleted successfully",
)
async def delete_user(user_id: str, service: Annotated[UserService, Depends()]) -> dict:
    try:
        result = await service.delete_user(user_id)
        return {
            "message": "User deleted successfully" if result is False else "User restored successfully",
        }
    except ValidationError as validation_error:
        msg = f"User change status failed, validation error: {validation_error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_error.errors(),
            headers={"X-Error": "User change status failed"},
        ) from validation_error
    except Exception as error:
        msg = f"User change status failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User change status failed",
            headers={"X-Error": "User change status failed"},
        ) from error
