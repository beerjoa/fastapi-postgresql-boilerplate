from typing import Dict, Generator, Any

import pytest

from fastapi.testclient import TestClient

from app.database.session import CustomSession

from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    db_session = CustomSession(db_name="docker_db").get_session()
    db = db_session()
    yield db


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def random_user() -> Dict[str, str]:
    return dict(
        name="tester",
        password="123",
        email="tester@test.com",
    )


@pytest.fixture(scope="module")
def filter_params() -> Dict[str, Any]:
    return dict(skip=0, limit=100)


@pytest.fixture(scope="module")
def created_random_user() -> Dict[str, str]:
    return dict(
        id=None,
        name="tester",
        password="123",
        email="tester@test.com",
    )


@pytest.fixture(scope="module")
def invalid_user() -> Dict[str, str]:
    return dict(
        id=-1,
        name="",
        password="",
        email="",
    )
