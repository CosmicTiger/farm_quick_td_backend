from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from app.core import get_settings


async def init_mongo_db_instance() -> None:
    """Initialize MongoDB connection."""
    db_client = AsyncIOMotorClient(get_settings().DATABASE_URL)
    await init_beanie(database=db_client, document_models=[])


async def init_db() -> None:
    """Initialize the database connection."""
    if get_settings().DB_TYPE == "mongodb":
        await init_mongo_db_instance()

    elif get_settings().DB_TYPE == "sqlite":
        # SQLite initialization logic can be added here if needed | TODO: <CosmicTiger>: Pending implementation
        pass
    else:
        raise ValueError("Unsupported database type.")
