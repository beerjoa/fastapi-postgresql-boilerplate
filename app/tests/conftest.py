from typing import Dict, Generator

import pytest

from fastapi.testclient import TestClient

from app.database.session import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def random_user() -> Dict[str, str]:
    return {
        "name": "tester",
        "password": "123",
        "email": "tester@test.com",
    }
