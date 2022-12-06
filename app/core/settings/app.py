import os
import secrets
from typing import Any, Dict, List, Tuple

from pydantic import BaseSettings, PostgresDsn, SecretStr

from app.core.settings.base import BaseAppSettings


class DBUrlSettings(BaseSettings):
    postgres: PostgresDsn = "postgresql://postgres:postgres@0.0.0.0:5432/postgres"
    docker_db: PostgresDsn = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/docker_db"


class AppSettings(BaseAppSettings):
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI example application"
    version: str = "0.1.0"

    api_v1_prefix: str = "/api/v1"
    secret_key: SecretStr
    jwt_token_prefix: str = "bearer"

    db_url_conf = DBUrlSettings()

    allowed_hosts: List[str] = ["*"]

    class Config:
        validate_assignment = True

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url,
            "title": self.title,
            "version": self.version,
        }
