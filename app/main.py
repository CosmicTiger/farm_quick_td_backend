from typing import Annotated
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import uvicorn
from fastapi import Depends, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings, get_settings
from app.core.logger import f, logger
from app.api.routers.routes import router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[any, any, any]:
    try:
        message = "Starting " + get_settings().PROJECT_NAME + " version: " + get_settings().API_VERSION
        logger.info(f.renderText(message))
        if get_settings().DEBUG:
            logger.info(get_settings().check_env_variables)
        yield
        logger.info(f.renderText("Shutting down " + get_settings().PROJECT_NAME))
        if not get_settings().DEBUG:
            logger.info(
                "Submitting logs to the cloud",
            )  # TODO(<CosmicTiger>): Pending implementation to send logs to AWS Cloud  # noqa: TD003, FIX002

    finally:
        pass


app = FastAPI(
    title=get_settings().PROJECT_NAME,
    lifespan=lifespan,
    contact={
        "name": get_settings().PROJECT_NAME + " Maintainers",
        "email": get_settings().emails_maintainers_list[0],
    },
    description=get_settings().PROJECT_DESCRIPTION,
    version=get_settings().API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOWED_CORS_ORIGIN,
    allow_methods=get_settings().ALLOWED_METHODS,
    allow_headers=get_settings().ALLOWED_HEADERS,
)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/healthcheck", response_class=HTMLResponse)
async def healthcheck(settings: Annotated[settings.Settings, Depends(get_settings)]) -> HTMLResponse:
    try:
        status = settings.get_health_status
        status_text = ""

        for key, value in status.items():
            status_text += f"<h2>{key}</h2>"
            if isinstance(value, dict):
                for k, v in value.items():
                    status_text += f"<p>{k}: {v}</p>"
            else:
                status_text += f"<p>{value}</p>"
        status["status"] = "healthy"
        return HTMLResponse(
            content=f"""
        <html>
            <head><title>Health Check</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center;">
                <h1 style="color: green;">System Status: Healthy</h1>
                {status_text}
            </body>
        </html>
        """,
            status_code=200,
        )
    except Exception as e:  # noqa: BLE001
        return HTMLResponse(
            content=f"""
            <html>
                <head>
                    <title>Health Check</title>
                </head>
                <body style="font-family: Arial, sans-serif; text-align: center;">
                <h1 style="color: red;">System Status: Error</h1>
                <p>{e!s}</p>
            </body>
            </html>
        """,
        )


app.include_router(router)


def start() -> None:
    """Start the app through uvicorn

    With the first param being the app itself, the app should go as an import\
    in order to be run by poetry as script
    """
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    start()
