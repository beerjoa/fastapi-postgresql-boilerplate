import logging
import uvicorn

from pathlib import Path
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.core import settings
from app.utils import CustomizeLogger


logger = logging.getLogger(__name__)

config_path = Path(__file__).with_name("logging_conf.json")


def create_app() -> FastAPI:
    _app = FastAPI(
        root_path=settings.ROOT_PATH,
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        debug=False,
        docs_url=None,
        redoc_url=None,
    )
    _app.logger = CustomizeLogger.make_logger(config_path)
    _app.include_router(api_router, prefix=settings.API_V1_STR)
    _app.mount("/static", StaticFiles(directory="app/static"))
    _app.openapi_url = "./openapi.json" if settings.ROOT_PATH else "/openapi.json"

    @_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=_app.openapi_url,
            title=_app.title + " - Swagger UI custom",
            oauth2_redirect_url=_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"{settings.ROOT_PATH}/static/swagger-ui-bundle.js",
            swagger_css_url=f"{settings.ROOT_PATH}/static/swagger-ui.css",
        )

    @_app.get(_app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @_app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=_app.openapi_url,
            title=_app.title + " - ReDoc",
            redoc_js_url=f"{settings.ROOT_PATH}/static/redoc.standalone.js",
        )

    return _app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", root_path=settings.ROOT_PATH, host="0.0.0.0", port=8000)
