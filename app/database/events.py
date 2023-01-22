import logging

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.settings.app import AppSettings

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to database...")

    engine = create_async_engine(url=str(settings.db_url), pool_size=50, max_overflow=0, echo=True, future=True)
    async_session_factory = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=True)
    app.state.pool = async_session_factory

    logger.info("Connected to database.")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing database connection...")

    # app.state.pool.close_all()

    logger.info("Database connection closed.")
