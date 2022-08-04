from typing import Generator, AsyncGenerator

from app.database.session import Session

from asyncpg.connection import Connection


def get_postgres() -> Generator:
    try:
        db_session = Session(db_name="postgres").get_session()
        db = db_session()
        yield db
    finally:
        db.close()


async def get_docker_db() -> AsyncGenerator[Connection, None]:
    try:
        session = Session(db_name="docker_db")
        db_session = await session.get_session()

        async with db_session() as db:
            yield db
    finally:
        await db.close()


db_sessions = {
    "postgres": get_postgres,
    "docker_db": get_docker_db,
}
