from pathlib import Path
from fastapi import FastAPI

from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import HTTPException
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.staticfiles import StaticFiles
from asgi_correlation_id import CorrelationIdMiddleware

from app.api.v1 import api_router
from app.core import settings
from app.utils import (
    AppExceptionCase,
    app_exception_handler,
    CustomizeLogger,
    http_exception_handler,
    request_validation_exception_handler,
)

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
    _app.add_middleware(CorrelationIdMiddleware)
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

    @_app.exception_handler(HTTPException)
    async def custom_http_exception_handler(request, e):
        return await http_exception_handler(request, e)

    @_app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        return await request_validation_exception_handler(request, e)

    @_app.exception_handler(AppExceptionCase)
    async def custom_app_exception_handler(request, e):
        return await app_exception_handler(request, e)

    return _app


app = create_app()
