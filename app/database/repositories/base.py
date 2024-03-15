from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils import AppExceptionCase


class BaseRepository:
    """Base Repository for all repositories."""

    def __init__(self, conn: AsyncSession) -> None:
        self._conn = conn

    @property
    def connection(self) -> AsyncSession:
        return self._conn


def db_error_handler(func) -> callable:
    """Database error handler decorator

    Args:
        func (callable): [description]

    Returns:
        callable: [description]

    Raises:
        AppExceptionCase: [description]
    """

    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DatabaseError as e:
            db_error_context = e.orig.__context__.__str__()
            raise AppExceptionCase(
                context={"reason": db_error_context, "code": e.code},
                status_code=500,
            )

    return wrapper
