import logging

from pydantic import PostgresDsn, SecretStr

from app.core.settings.app import AppSettings


class DevAppSettings(AppSettings):
    # fastapi_kwargs
    debug: bool = True
    title: str = "Dev FastAPI example application"

    # back-end app settings
    secret_key: SecretStr = SecretStr("secret-dev")
    db_url: PostgresDsn = "postgresql+asyncpg://postgres:postgres@postgresql:5432/postgres"
    logging_level: int = logging.DEBUG
