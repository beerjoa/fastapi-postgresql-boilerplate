from typing import Dict

from fastapi.testclient import TestClient
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from app.core import settings
from app.models import User


def test_create_user(client: TestClient, random_user: Dict[str, str], created_random_user: Dict[str, str]) -> None:
    response = client.post(f"{settings.API_V1_STR}/users", json=random_user)
    result = response.json()
    created_user = result.get("data")
    assert response.status_code == HTTP_201_CREATED
    assert created_user.get("name") == random_user.get("name")
    assert created_user.get("password") == random_user.get("password")
    assert created_user.get("email") == random_user.get("email")

    created_random_user["id"] = created_user.get("id")


def test_create_user_duplicate_user(client: TestClient, random_user: Dict[str, str]) -> None:
    response = client.post(f"{settings.API_V1_STR}/users", json=random_user)
    result = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert result.get("app_exception") == "Response4XX"
    assert result["context"].get("reason") == "already created user"


def test_get_users(client: TestClient, filter_params: Dict[str, int]) -> None:
    response = client.get(f"{settings.API_V1_STR}/users", params=filter_params)
    result = response.json()
    filterd_users = result.get("data")
    assert response.status_code == HTTP_200_OK
    assert len(filterd_users) > 0


def test_get_user_by_id(client: TestClient, created_random_user: Dict[str, str]) -> None:
    response = client.get(f"{settings.API_V1_STR}/users/{created_random_user.get('id')}")
    result = response.json()

    result_user = result.get("data")
    assert response.status_code == HTTP_200_OK
    assert result_user.get("id") == created_random_user.get("id")
    assert result_user.get("name") == created_random_user.get("name")
    assert result_user.get("password") == created_random_user.get("password")
    assert result_user.get("email") == created_random_user.get("email")


def test_get_user_by_id_exception(
    client: TestClient, invalid_user: Dict[str, str], created_random_user: Dict[str, str]
) -> None:
    ## 1. not found
    response = client.get(f"{settings.API_V1_STR}/users/{invalid_user.get('id')}")

    result = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert result.get("app_exception") == "Response4XX"
    assert result["context"].get("reason") == f"User with ID:{invalid_user.get('id')} does not exist."


def test_delete_user(client: TestClient, created_random_user: Dict[str, str]) -> None:
    response = client.delete(f"{settings.API_V1_STR}/users/{created_random_user.get('id')}")
    result = response.json()

    deleted_user = result["data"]
    assert response.status_code == HTTP_200_OK
    assert deleted_user.get("id") == created_random_user.get("id")
    assert deleted_user.get("name") == created_random_user.get("name")
    assert deleted_user.get("password") == created_random_user.get("password")
    assert deleted_user.get("email") == created_random_user.get("email")


def test_delete_user_exception(
    client: TestClient, invalid_user: Dict[str, str], created_random_user: Dict[str, str]
) -> None:
    ## 1. not found
    response = client.delete(f"{settings.API_V1_STR}/users/{invalid_user.get('id')}")

    result = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert result.get("app_exception") == "Response4XX"
    assert result["context"].get("reason") == f"User with ID:{invalid_user.get('id')} does not exist."
