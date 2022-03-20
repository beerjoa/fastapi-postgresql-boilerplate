import os
import secrets
from pydantic import BaseSettings, Field, PostgresDsn


class DBUrlSettings(BaseSettings):
    postgres: PostgresDsn = "postgresql://postgres:postgres@0.0.0.0:5432/postgres"
    docker_db: PostgresDsn = "postgresql://postgres:postgres@0.0.0.0:5432/docker_db"


class Settings(BaseSettings):
    APP_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "fastapi-postgresql-boilerplate"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    PYTHONPATH = Field("./", env="PYTHONPATH")
    ROOT_PATH: str = ""
    DB_URL_CONF = DBUrlSettings()

    POSTGRES_USER = Field("postgres", env="POSTGRES_USER")
    POSTGRES_PASSWORD = Field("postgres", env="POSTGRES_PASSWORD")
    POSTGRES_DB = Field("postgres", env="POSTGRES_DB")
    POSTGRES_PORT = Field(5432, env="POSTGRES_PORT")
    POSTGRES_HOST = Field("0.0.0.0", env="POSTGRES_HOST")
    DEFAULT_DATABASE = Field("docker_db", env="DEFAULT_DATABASE")

    class Config:
        env_file = os.path.expanduser("./.env")


settings = Settings()
