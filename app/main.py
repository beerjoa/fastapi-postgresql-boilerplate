from pathlib import Path

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from starlette.staticfiles import StaticFiles

from app.api.v1 import api_router
from app.core import settings
from app.core.events import create_start_app_handler, create_stop_app_handler
from app.utils import (
    AppExceptionCase,
    CustomizeLogger,
    app_exception_handler,
    http_exception_handler,
    request_validation_exception_handler,
)

config_path = Path(__file__).with_name("logging_conf.json")


def create_app() -> FastAPI:
    _app = FastAPI(**settings.fastapi_kwargs)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.add_middleware(CorrelationIdMiddleware)
    _app.logger = CustomizeLogger.make_logger(config_path)
    _app.include_router(api_router, prefix=settings.api_v1_prefix)
    _app.mount("/static", StaticFiles(directory="app/static"))

    @_app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=_app.openapi_url,
            title=_app.title + " - Swagger UI custom",
            oauth2_redirect_url=_app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=f"{settings.openapi_prefix}/static/swagger-ui-bundle.js",
            swagger_css_url=f"{settings.openapi_prefix}/static/swagger-ui.css",
        )

    @_app.get(_app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @_app.get("/redoc", include_in_schema=False)
    async def redoc_html():
        return get_redoc_html(
            openapi_url=_app.openapi_url,
            title=_app.title + " - ReDoc",
            redoc_js_url=f"{settings.openapi_prefix}/static/redoc.standalone.js",
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

    _app.add_event_handler("startup", create_start_app_handler(_app, settings))
    _app.add_event_handler("shutdown", create_stop_app_handler(_app))

    return _app


app = create_app()
