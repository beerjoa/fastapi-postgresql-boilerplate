from fastapi import APIRouter, Depends
from starlette.status import HTTP_200_OK

from app.api.dependencies.auth import get_current_user_auth
from app.api.dependencies.database import get_repository
from app.api.dependencies.service import get_service
from app.api.dependencies.users import get_users_filters
from app.database.repositories.users import UsersRepository
from app.models.user import User
from app.schemas.user import UserInUpdate, UserResponse, UsersFilters
from app.services.users import UsersService
from app.utils import ERROR_RESPONSES, handle_result

router = APIRouter()


@router.get(
    "",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="users:all",
)
async def read_users(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    users_filters: UsersFilters = Depends(get_users_filters),
):
    result = await users_service.get_users(
        users_repo=users_repo,
        users_filters=users_filters,
    )

    return await handle_result(result)


@router.get(
    "/{user_id}",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="user:info-by-id",
)
async def read_user_by_id(
    *,
    user: User = Depends(get_current_user_auth()),
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_id: int,
) -> UserResponse:
    result = await users_service.get_user_by_id(users_repo=users_repo, user_id=user_id)

    return await handle_result(result)


@router.patch(
    "",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="user:patch-by-id",
)
async def update_user(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    user_in: UserInUpdate,
    token_user: User = Depends(get_current_user_auth()),
) -> UserResponse:
    result = await users_service.update_user(users_repo=users_repo, token_user=token_user, user_in=user_in)
    return await handle_result(result)


@router.delete(
    "",
    status_code=HTTP_200_OK,
    response_model=UserResponse,
    responses=ERROR_RESPONSES,
    name="user:delete-by-id",
)
async def delete_user(
    *,
    users_service: UsersService = Depends(get_service(UsersService)),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    token_user: User = Depends(get_current_user_auth()),
) -> UserResponse:
    result = await users_service.delete_user(users_repo=users_repo, token_user=token_user)
    return await handle_result(result)
