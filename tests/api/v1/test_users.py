from os import environ

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

# from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from app.core import settings
from app.core.constant import (
    FAIL_VALIDATION_MATCHED_USER_EMAIL,
    FAIL_VALIDATION_MATCHED_USER_ID,
    FAIL_VALIDATION_USER_DUPLICATED,
    FAIL_VALIDATION_USER_WRONG_PASSWORD,
    SUCCESS_DELETE_USER,
    SUCCESS_GET_USERS,
    SUCCESS_MATCHED_USER_ID,
    SUCCESS_MATCHED_USER_TOKEN,
    SUCCESS_SIGN_IN,
    SUCCESS_SIGN_UP,
    SUCCESS_UPDATE_USER,
)

environ["APP_ENV"] = "test"

pytestmark = pytest.mark.asyncio


async def test_signup(
    app: FastAPI,
    client: AsyncClient,
    random_user: dict[str, str],
    created_random_user: dict[str, str],
) -> None:
    response = await client.post(app.url_path_for("auth:signup"), json=random_user)
    result = response.json()
    created_user = result.get("data")
    assert response.status_code == HTTP_201_CREATED
    assert result.get("message") == SUCCESS_SIGN_UP
    assert created_user.get("username") == random_user.get("username")
    assert created_user.get("email") == random_user.get("email")

    created_random_user["id"] = created_user.get("id")


async def test_signup_duplicate_user(app: FastAPI, client: AsyncClient, random_user: dict[str, str]) -> None:
    response = await client.post(app.url_path_for("auth:signup"), json=random_user)
    result = response.json()
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert result.get("app_exception") == "Response4XX"
    assert result["context"].get("reason") == FAIL_VALIDATION_USER_DUPLICATED


async def test_signin_error(
    app: FastAPI,
    client: AsyncClient,
    created_random_user: dict[str, str],
    invalid_user: dict[str, str],
) -> None:
    # FAIL_VALIDATION_MATCHED_USER_EMAIL
    response = await client.post(app.url_path_for("auth:signin"), json=invalid_user)
    result = response.json()

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert result.get("app_exception") == "Response4XX"
    assert result["context"].get("reason") == FAIL_VALIDATION_MATCHED_USER_EMAIL

    # FAIL_VALIDATION_USER_WRONG_PASSWORD
    invalid_user["email"] = created_random_user["email"]
    response = await client.post(app.url_path_for("auth:signin"), json=invalid_user)
    result = response.json()

    assert response.status_code == HTTP_400_BAD_REQUEST
    assert result.get("app_exception") == "Response4XX"
    assert result["context"].get("reason") == FAIL_VALIDATION_USER_WRONG_PASSWORD


async def test_signin(app: FastAPI, client: AsyncClient, created_random_user: dict[str, str]) -> None:
    response = await client.post(app.url_path_for("auth:signin"), json=created_random_user)
    result = response.json()
    token = result.get("data").get("token")

    assert response.status_code == HTTP_200_OK
    assert result.get("message") == SUCCESS_SIGN_IN
    assert token.get("access_token")
    assert token.get("token_type") == settings.jwt_token_prefix

    created_random_user["token"] = token


async def test_auth_info(app: FastAPI, client: AsyncClient, created_random_user: dict[str, str]) -> None:
    headers = {
        "Authorization": f"{settings.jwt_token_prefix} {created_random_user.get('token').get('access_token')}",
        **client.headers,
    }
    response = await client.get(app.url_path_for("auth:info"), headers=headers)
    result = response.json()

    result_user = result.get("data")

    assert response.status_code == HTTP_200_OK
    assert result.get("message") == SUCCESS_MATCHED_USER_TOKEN
    assert result_user.get("id") == created_random_user.get("id")
    assert result_user.get("username") == created_random_user.get("username")
    assert result_user.get("email") == created_random_user.get("email")


async def test_all_user(app: FastAPI, client: AsyncClient) -> None:
    response = await client.get(app.url_path_for("users:all"))

    result = response.json()
    assert response.status_code == HTTP_200_OK
    assert result.get("message") == SUCCESS_GET_USERS
    assert isinstance(result.get("data"), list)


async def test_user_by_id(app: FastAPI, client: AsyncClient, created_random_user: dict[str, str]) -> None:
    headers = {
        "Authorization": f"{settings.jwt_token_prefix} {created_random_user.get('token').get('access_token')}",
        **client.headers,
    }
    response = await client.get(
        app.url_path_for("user:info-by-id", user_id=created_random_user.get("id")),
        headers=headers,
    )

    result = response.json()
    assert response.status_code == HTTP_200_OK
    assert result.get("message") == SUCCESS_MATCHED_USER_ID
    assert result.get("data").get("id") == created_random_user.get("id")
    assert result.get("data").get("username") == created_random_user.get("username")
    assert result.get("data").get("email") == created_random_user.get("email")


async def test_user_by_id_error(app: FastAPI, client: AsyncClient, created_random_user: dict[str, str]) -> None:
    headers = {
        "Authorization": f"{settings.jwt_token_prefix} {created_random_user.get('token').get('access_token')}",
        **client.headers,
    }
    response = await client.get(
        app.url_path_for("user:info-by-id", user_id=-1),
        headers=headers,
    )

    result = response.json()
    assert response.status_code == HTTP_404_NOT_FOUND
    assert result.get("app_exception") == "Response4XX"
    assert result["context"].get("reason") == FAIL_VALIDATION_MATCHED_USER_ID


async def test_update_user(app: FastAPI, client: AsyncClient, created_random_user: dict[str, str]) -> None:
    headers = {
        "Authorization": f"{settings.jwt_token_prefix} {created_random_user.get('token').get('access_token')}",
        **client.headers,
    }

    update_user = {
        "username": "new_username",
        **created_random_user,
    }
    response = await client.patch(
        app.url_path_for("user:patch-by-id"),
        json=update_user,
        headers=headers,
    )

    result = response.json()
    assert response.status_code == HTTP_200_OK
    assert result.get("message") == SUCCESS_UPDATE_USER
    assert result.get("data").get("id") == update_user.get("id")
    assert result.get("data").get("username") == update_user.get("username")
    assert result.get("data").get("email") == update_user.get("email")


async def test_delete_user(app: FastAPI, client: AsyncClient, created_random_user: dict[str, str]) -> None:
    headers = {
        "Authorization": f"{settings.jwt_token_prefix} {created_random_user.get('token').get('access_token')}",
        **client.headers,
    }
    response = await client.delete(app.url_path_for("user:delete-by-id"), headers=headers)

    result = response.json()
    assert response.status_code == HTTP_200_OK
    assert result.get("message") == SUCCESS_DELETE_USER
