from beanie import init_beanie

from app.core import get_settings
from app.core.logger import logger
from app.infrastructure.models.odm.beanie_user_model import BeanieUser


async def init_mongo_db_instance() -> None:
    """Initialize MongoDB connection."""
    db_client = get_settings().get_db_client

    if not db_client:
        raise RuntimeError("MongoDB client not initialized.")

    try:
        await init_beanie(database=db_client.quick_td_db, document_models=[BeanieUser])
    except Exception as e:
        msg = f"Failed to initialize Beanie ODM: {e}"
        logger.error(msg)
        raise RuntimeError(msg) from e


async def init_db() -> None:
    """Initialize the database connection."""
    if get_settings().DB_TYPE == "mongodb":
        await init_mongo_db_instance()

    elif get_settings().DB_TYPE == "sqlite":
        # SQLite initialization logic can be added here if needed | TODO: <CosmicTiger>: Pending implementation
        pass
    else:
        raise ValueError("Unsupported database type.")
