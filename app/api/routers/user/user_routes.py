from fastapi import Request, APIRouter, HTTPException, status
from pydantic import ValidationError

from app.main import logger
from app.core.rate_limiting import limiter
from app.services.user_service import UserService
from app.api.routers.auth.auth_routes import CommonResponse
from app.schemas.pydantic.user_schemas import UserRead, UserCreate, UserUpdate, UserUpdatePassword

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
async def create_user(request: Request, user_data: UserCreate) -> UserRead:
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
        return await UserService().create_user(user_data)
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
async def get_me() -> UserRead:
    """Get user information.

    Returns:
        dict: User information.
    """
    return {"user": "user information"}


@user_router.patch(
    "/update_password/{user_id}",
    summary="Update user password",
    response_description="User password updated successfully",
)
@limiter.limit("2/hour")
async def update_user_password(request: Request, user_id: str, new_password_payload: UserUpdatePassword) -> dict:
    """Update user password.

    Args:
        user_data (UserCreate): User data.

    Returns:
        dict: User password updated successfully.
    """
    try:
        result = await UserService().update_user_password(user_id, new_password_payload)
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
async def update_user_info(request: Request, user_id: str, user_data: UserUpdate) -> CommonResponse[UserRead]:
    try:
        updated_user = await UserService().update_user(user_id, user_data)
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
async def delete_user(user_id: str) -> dict:
    try:
        result = await UserService().delete_user(user_id)
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
