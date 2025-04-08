from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from httpx import AsyncClient, ASGITransport

from app.main import app, init_db


@asynccontextmanager
async def lifespan_test_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        await init_db()
        yield client
