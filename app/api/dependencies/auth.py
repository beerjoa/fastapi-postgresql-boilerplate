from collections.abc import Callable

from fastapi import Depends, Request, Security
from fastapi.exceptions import HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from app.api.dependencies.database import get_repository
from app.core import constant, settings
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.core.token import get_user_from_token
from app.database.repositories.users import UsersRepository
from app.models.user import User

AUTH_HEADER_KEY = settings.auth_header_key


class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: Request) -> str | None:
        try:
            return await super().__call__(request)
        except HTTPException as auth_exc:
            raise HTTPException(
                status_code=auth_exc.status_code,
                detail=constant.FAIL_AUTH_CHECK,
            )


def _get_auth_header_retriever(
    *,
    required: bool = True,
) -> Callable:
    return _get_auth_from_header if required else _get_auth_from_header_optional


def _get_auth_from_header(
    api_key: str = Security(RWAPIKeyHeader(name=AUTH_HEADER_KEY)),
    settings: AppSettings = Depends(get_app_settings),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=constant.FAIL_AUTH_INVALID_TOKEN_PREFIX,
        )

    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=constant.FAIL_AUTH_INVALID_TOKEN_PREFIX,
        )

    return token


def _get_auth_from_header_optional(
    auth: str | None = Security(RWAPIKeyHeader(name=AUTH_HEADER_KEY, auto_error=False)),
    settings: AppSettings = Depends(get_app_settings),
) -> str:
    if auth:
        return _get_auth_from_header(api_key=auth, settings=settings)

    return ""


async def _get_current_user(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_auth_header_retriever()),
    settings: AppSettings = Depends(get_app_settings),
) -> User:
    try:
        secret_key = str(settings.secret_key.get_secret_value())
        token_user = get_user_from_token(token=token, secret_key=secret_key)

    except ValueError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail=constant.FAIL_AUTH_VALIDATION_CREDENTIAL,
        )

    try:
        user = await users_repo.get_user_by_email(email=token_user.email)

        if user is None:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=constant.FAIL_VALIDATION_MATCHED_USER_EMAIL,
            )
        else:
            return user

    except ValueError:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=constant.FAIL_VALIDATION_MATCHED_USER_EMAIL,
        )


async def _get_current_user_optional(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token: str = Depends(_get_auth_header_retriever()),
    settings: AppSettings = Depends(get_app_settings),
) -> User | None:
    if token:
        return await _get_current_user(users_repo=users_repo, token=token, settings=settings)

    return None


def get_current_user_auth(
    *,
    required: bool = True,
) -> Callable:
    return _get_current_user if required else _get_current_user_optional
