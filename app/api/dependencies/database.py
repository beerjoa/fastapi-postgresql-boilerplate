from collections.abc import AsyncGenerator, Callable

from fastapi import Depends
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.repositories.base import BaseRepository


def _get_db_session(request: Request) -> AsyncSession:
    return request.app.state.pool


async def _get_connection_from_session(
    pool: AsyncSession = Depends(_get_db_session),
) -> AsyncGenerator[AsyncSession, None]:
    async with pool() as session:
        yield session


def get_repository(
    repo_type: type[BaseRepository],
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(
        session: AsyncSession = Depends(_get_connection_from_session),
    ) -> BaseRepository:
        return repo_type(session)

    return _get_repo
