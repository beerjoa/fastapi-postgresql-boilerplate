from typing import Generator

from app.database.session import CustomSession


def get_postgres() -> Generator:
    try:
        db_session = CustomSession(db_name="postgres").get_session()
        db = db_session()
        yield db
    finally:
        db.close()


def get_docker_db() -> Generator:
    try:
        db_session = CustomSession(db_name="docker_db").get_session()
        db = db_session()
        yield db
    finally:
        db.close()


db_sessions = {
    "postgres": get_postgres,
    "docker_db": get_docker_db,
}
