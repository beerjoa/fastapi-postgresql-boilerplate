from typing import Callable

from fastapi import FastAPI

from app.core.settings.app import AppSettings
from app.database.events import connect_to_db, close_db_connection


def create_start_app_handler(app: FastAPI, settings: AppSettings) -> Callable:
    async def start_app() -> None:
        await connect_to_db(app, settings)

    return start_app


def create_stop_app_handler(app):
    async def stop_app():
        await close_db_connection(app)

    return stop_app