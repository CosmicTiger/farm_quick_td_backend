import pytest_asyncio
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from app.infrastructure.models.odm.beanie_task_model import BeanieTask
from app.infrastructure.models.odm.beanie_user_model import BeanieUser


@pytest_asyncio.fixture(autouse=True)
async def initialize_fixture_beanie() -> None:
    client = AsyncMongoMockClient()
    await init_beanie(document_models=[BeanieUser, BeanieTask], database=client.get_database(name="db"))
