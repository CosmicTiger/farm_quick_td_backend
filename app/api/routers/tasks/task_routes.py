from typing import Annotated

from fastapi import Body, Query, Depends, APIRouter, HTTPException

from app.core.logger import logger
from app.domain.entities.user import User
from app.services.task_service import TaskService
from app.schemas.pydantic.task_schemas import TaskRead, TaskCreate, TaskUpdate, TaskFilters
from app.schemas.pydantic.common_schemas import (
    CommonResponse,
    PaginationOptions,
    CommonListResponse,
    FilterCapabilities,
)
from app.api.routers.dependencies.user_deps import get_current_user

task_router = APIRouter(
    prefix="/task",
    tags=["Task"],
    responses={404: {"description": "Not found"}},
    dependencies=[],
)


@task_router.post(
    "/create",
    summary="Create task",
    response_description="📝💾 Recently created Task information",
)
async def create_task(
    current_user: Annotated[User, Depends(get_current_user)],
    task_data: TaskCreate,
    service: Annotated[TaskService, Depends()],
) -> CommonResponse[TaskRead]:
    try:
        created_task = await service.create_task(current_user, task_data)
        return {
            "message": "Task created successfully.",
            "result": created_task,
        }
    except Exception as error:
        msg = f"Task creation failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=500,
            detail="Task creation failed",
            headers={"X-Error": "Task creation failed"},
        ) from error


@task_router.get(
    "/read/{task_id}",
    summary="Get task",
    response_description="📝🧩 Founded Task",
)
async def get_task(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends()],
    task_id: str,
) -> CommonResponse[TaskRead]:
    try:
        retrieved_task = await service.get_task_by_id(task_id)
        return {
            "message": "Task retrieved successfully.",
            "result": retrieved_task,
        }
    except Exception as error:
        msg = f"Task retrieval failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=500,
            detail="Task retrieval failed",
            headers={"X-Error": "Task retrieval failed"},
        ) from error


@task_router.post(
    "/list",
    summary="List tasks",
    response_description="📝🔎 List of tasks in dependence of filters and sorts applied",
)
async def list_tasks(
    # current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends()],
    pagination_options: Annotated[
        PaginationOptions[FilterCapabilities[TaskFilters]] | None,
        Body(description="Pagination options"),
    ] = None,
    page: Annotated[int, Query(description="Current page retrieved")] = 0,
    offset: Annotated[int, Query(description="Number of items per page")] = 10,
) -> CommonListResponse[TaskRead]:
    try:
        tasks = await service.list_tasks(
            pagination_options.filters if pagination_options else None,
            pagination_options.build_sorts_options() if pagination_options else None,
            page,
            offset,
        )
        return {
            "total": len(tasks),
            "data": tasks,
        }
    except Exception as error:
        msg = f"Task retrieval failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=500,
            detail="Task retrieval failed",
            headers={"X-Error": "Task retrieval failed"},
        ) from error


@task_router.put(
    "/{task_id}",
    summary="Update task",
    response_description="📝🔄 Updated task information",
)
async def update_task(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends()],
    task_id: str,
    task_data: TaskUpdate,
) -> CommonResponse[TaskRead]:
    try:
        updated_task = await service.update_task(task_id, current_user, task_data)
        return {
            "message": "Task updated successfully.",
            "result": updated_task,
        }
    except Exception as error:
        msg = f"Task update failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=500,
            detail="Task update failed",
            headers={"X-Error": "Task update failed"},
        ) from error


@task_router.patch(
    "/archive/{task_id}",
    summary="Archive task",
    response_description="📝📁 Toggle Archive task information",
)
async def archive_task(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends()],
    task_id: str,
) -> CommonResponse[TaskRead]:
    try:
        retrieved_task = await service.archive_task(task_id, current_user)
        return {
            "message": "Task has been archived successfully.",
            "result": retrieved_task,
        }
    except Exception as error:
        msg = f"Task retrieval failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=500,
            detail="Task retrieval failed",
            headers={"X-Error": "Task retrieval failed"},
        ) from error


@task_router.delete(
    "/{task_id}",
    summary="Delete task",
    response_description="📝💥 Task deletion confirmation",
)
async def delete_task(
    current_user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends()],
    task_id: str,
) -> CommonResponse[TaskRead]:
    try:
        retrieved_task = await service.delete_task(task_id)
        return {
            "message": "Task deleted successfully.",
            "result": retrieved_task,
        }
    except Exception as error:
        msg = f"Task deletion attempt failed, error: {error}"
        logger.error(msg)
        raise HTTPException(
            status_code=500,
            detail="Task deletion attempt failed",
            headers={"X-Error": "Task deletion attempt failed"},
        ) from error
