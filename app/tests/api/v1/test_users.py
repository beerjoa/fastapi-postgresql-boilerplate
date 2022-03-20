from typing import Dict

from fastapi.testclient import TestClient

from app.core import settings


def test_create_user(client: TestClient, random_user: Dict[str, str]) -> None:
    response = client.post(f"{settings.API_V1_STR}/users", json=random_user)
    user = response.json()
    assert response.status_code == 200
    assert user.get("name") == random_user.get("name")
    assert user.get("password") == random_user.get("password")
    assert user.get("email") == random_user.get("email")


def test_read_users(client: TestClient) -> None:
    response = client.get(f"{settings.API_V1_STR}/users")
    users = response.json()
    assert response.status_code == 200
    assert len(users) > 0
