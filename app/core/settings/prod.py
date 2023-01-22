import logging

from pydantic import PostgresDsn, SecretStr

from app.core.settings.app import AppSettings


class ProdAppSettings(AppSettings):
    # fastapi_kwargs
    debug: bool = False
    title: str = "Production FastAPI example application"

    # back-end app settings
    secret_key: SecretStr = SecretStr("secret-prod")
    db_url: PostgresDsn = "postgresql+asyncpg://postgres:postgres@postgresql:5432/postgres"
    logging_level: int = logging.INFO
