from fastapi import APIRouter

router = APIRouter()

routers = []


for route in routers:
    router.include_router(route)
