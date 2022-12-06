from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.api.dependencies.auth import get_current_user_auth
from app.api.dependencies.database import get_repository
from app.api.dependencies.service import get_service
from app.core.config import get_app_settings
from app.core.settings.app import AppSettings
from app.database.repositories.users import UsersRepository
from app.models.user import User
from app.schemas.user import UserInCreate, UserInSignIn, UserResponse
from app.services.users import UsersService
from app.utils import ERROR_RESPONSES, ServiceResult, handle_result

router = APIRouter()


@router.get(
    path="/info",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:info",
)
async def get_user_by_token(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    token_user: User = Depends(get_current_user_auth()),
) -> ServiceResult:
    """
    Create new users.
    """
    result = await users_service.get_user_by_token(
        token_user=token_user,
    )

    return await handle_result(result)


@router.post(
    path="/signup",
    status_code=HTTP_201_CREATED,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:signup",
)
async def signup_user(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_in: UserInCreate,
    settings: AppSettings = Depends(get_app_settings),
) -> ServiceResult:
    """
    Signup new users.
    """
    secret_key = str(settings.secret_key.get_secret_value())
    result = await users_service.signup_user(users_repo=users_repo, user_in=user_in, secret_key=secret_key)

    return await handle_result(result)


@router.post(
    path="/signin",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="auth:signin",
)
async def signin_user(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_in: UserInSignIn,
    settings: AppSettings = Depends(get_app_settings),
) -> ServiceResult:
    """
    Create new users.
    """
    secret_key = str(settings.secret_key.get_secret_value())
    result = await users_service.signin_user(users_repo=users_repo, user_in=user_in, secret_key=secret_key)

    return await handle_result(result)
