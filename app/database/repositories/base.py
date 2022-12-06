from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, conn: AsyncSession) -> None:
        self._conn = conn

    @property
    def connection(self) -> AsyncSession:
        return self._conn
