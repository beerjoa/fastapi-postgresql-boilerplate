from collections.abc import AsyncGenerator
from os import environ
from typing import Any

import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

environ["APP_ENV"] = "test"


@pytest_asyncio.fixture
def app() -> FastAPI:
    from app.main import create_app  # local import for testing purpose

    return create_app()


@pytest_asyncio.fixture
async def initialized_app(app: FastAPI) -> AsyncGenerator[FastAPI]:
    from app.core import settings

    async with LifespanManager(app):
        engine = create_async_engine(
            url=str(settings.db_url),
            pool_size=10,
            max_overflow=0,
            echo=False,
            future=True,
        )
        async_session_factory = sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=True,
        )
        app.state.pool = async_session_factory
        yield app


@pytest_asyncio.fixture
async def client(initialized_app: FastAPI) -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(initialized_app),
        base_url="http://test",
        headers={"Content-Type": "application/json"},
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="module")
def random_user() -> dict[str, str]:
    return dict(
        username="tester",
        password="123",
        email="tester@test.com",
    )


@pytest_asyncio.fixture(scope="module")
def filter_params() -> dict[str, Any]:
    return dict(skip=0, limit=100)


@pytest_asyncio.fixture(scope="module")
def created_random_user() -> dict[str, str]:
    return dict(
        id=None,
        username="tester",
        password="123",
        email="tester@test.com",
    )


@pytest_asyncio.fixture(scope="module")
def update_target_user() -> dict[str, str]:
    return dict(
        id=None,
        username="new_tester",
        password="123",
        email="new_tester@test.com",
    )


@pytest_asyncio.fixture(scope="module")
def invalid_user() -> dict[str, str]:
    return dict(
        id=-1,
        username="",
        password="",
        email="",
    )
