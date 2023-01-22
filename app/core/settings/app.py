from typing import Any, Dict, List

from pydantic import SecretStr

from app.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    # fastapi_kwargs
    debug: bool = False
    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    title: str = "FastAPI example application"
    version: str = "0.2.0"

    # back-end app settings
    api_v1_prefix: str = "/api/v1"
    secret_key: SecretStr
    jwt_token_prefix: str = "bearer"
    auth_header_key: str = "Authorization"
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
