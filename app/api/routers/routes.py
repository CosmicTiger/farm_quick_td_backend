from fastapi import APIRouter

from app.api.routers.auth.auth_routes import auth_router
from app.api.routers.user.user_routes import user_router
from app.api.routers.tasks.task_routes import task_router

router = APIRouter()

routers = [auth_router, user_router, task_router]


for route in routers:
    router.include_router(route)
