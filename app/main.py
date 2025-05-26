from typing import Annotated
from contextlib import suppress, asynccontextmanager
from collections.abc import AsyncGenerator

import uvicorn
from mangum import Mangum
from fastapi import Depends, FastAPI, Request
from scalar_fastapi import get_scalar_api_reference
from fastapi.responses import HTMLResponse, RedirectResponse
from slowapi.middleware import SlowAPIMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from scalar_fastapi.scalar_fastapi import Layout

from app.core import settings, get_settings
from app.core.logger import f, logger
from app.core.path_conf import STATIC_DIR
from app.api.routers.routes import router
from app.core.docs_metadata import tags_metadata
from app.core.docs_settings import load_theme_css
from app.core.rate_limiting import limiter
from app.infrastructure.datasource import init_db


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[any, any, any]:
    try:
        message = "Starting " + get_settings().PROJECT_NAME + " version: " + get_settings().get_formatted_version
        logger.info(f.renderText(message))
        if get_settings().DEBUG:
            logger.info(get_settings().check_env_variables)

        logger.info("Initializing database connection")
        await init_db()

        yield

        logger.info(f.renderText("Shutting down " + get_settings().PROJECT_NAME))
        if not get_settings().DEBUG:
            logger.info(
                "Submitting logs to the cloud",
            )  # TODO(<CosmicTiger>): Pending implementation to send logs to AWS Cloud  # noqa: TD003, FIX002

        logger.info("Closing database connection")
        get_settings().get_db_client.close()
    except Exception as e:  # noqa: BLE001
        logger.error("Error during lifespan: " + str(e))
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
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None,
)
app.state.limiter = limiter

app.add_middleware(SlowAPIMiddleware)
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


@app.get("/healthcheck", tags=["System"], response_class=HTMLResponse)
async def healthcheck(settings: Annotated[settings.Settings, Depends(get_settings)]) -> HTMLResponse:
    try:
        status = settings.get_health_status
        status["database_connection"] = await settings.get_ping_pong_db
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
                <p><a href="/docs">Swagger Docs</a></p>
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
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        scalar_favicon_url="/static/images/QuickTD-Icon-2.png",
        dark_mode=True,
        scalar_theme=load_theme_css(),
        show_sidebar=True,
        layout=Layout.MODERN,
    )


@app.get("/new-test-api")
async def return_hello_world():
    return {"message": "Hello World!"}


app.include_router(router, prefix=get_settings().get_api_prefix)


def start() -> None:
    """Start the app through uvicorn

    With the first param being the app itself, the app should go as an import\
    in order to be run by poetry as script
    """
    with suppress(KeyboardInterrupt):
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
        )


if __name__ == "__main__":
    start()

handler = Mangum(app)
