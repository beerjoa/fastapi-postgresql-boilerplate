import logging

from pydantic import SecretStr

from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    # fastapi_kwargs
    debug: bool = True
    title: str = "Dev FastAPI example application"

    # back-end app settings
    secret_key: SecretStr = SecretStr("secret-dev")
    logging_level: int = logging.DEBUG
