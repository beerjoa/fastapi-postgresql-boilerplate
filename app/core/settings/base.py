from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppEnvTypes(Enum):
    prod: str = "prod"
    dev: str = "dev"
    test: str = "test"


class BaseAppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_env: AppEnvTypes = AppEnvTypes.dev
