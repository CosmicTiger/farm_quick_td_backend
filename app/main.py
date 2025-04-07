from typing import Annotated
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

import uvicorn
from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings, get_settings
from app.core.logger import f, logger
from app.core.path_conf import STATIC_DIR
from app.infrastructure import init_db
from app.api.routers.routes import router


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[any, any, any]:
    try:
        message = "Starting " + get_settings().PROJECT_NAME + " version: " + get_settings().get_formatted_version
        logger.info(f.renderText(message))
        if get_settings().DEBUG:
            logger.info(get_settings().check_env_variables)
        yield
        logger.info(f.renderText("Shutting down " + get_settings().PROJECT_NAME))
        if not get_settings().DEBUG:
            logger.info(
                "Submitting logs to the cloud",
            )  # TODO(<CosmicTiger>): Pending implementation to send logs to AWS Cloud  # noqa: TD003, FIX002

        logger.info(f.renderText("Initializing database connection"))
        await init_db()
    except Exception as e:  # noqa: BLE001
        logger.error(f.renderText("Error during lifespan: " + str(e)))
        if not get_settings().DEBUG:
            logger.error(
                "Submitting logs to the cloud",
            )
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
    version=get_settings().get_formatted_version,
    docs_url=None,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOWED_CORS_ORIGIN,
    allow_methods=get_settings().ALLOWED_METHODS,
    allow_headers=get_settings().ALLOWED_HEADERS,
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def root() -> HTMLResponse:
    return RedirectResponse(
        url="/docs",
        status_code=302,
        headers={
            "X-Redirect-By": "FastAPI",
            "Location": "/docs",
        },
    )


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
                <h2>Docs Access</h2>
                <p><a href="/docs">Swagger UI</a></p>
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


@app.get("/docs", include_in_schema=False)
def overridden_swagger(req: Request) -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=get_settings().PROJECT_NAME + " API Docs",
        swagger_favicon_url="/static/images/QuickTD-Icon-2.png",
        swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    )


app.include_router(router, prefix=get_settings().get_api_prefix)


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
