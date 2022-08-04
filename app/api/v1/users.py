from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app import schemas, services
from app.utils import handle_result, ServiceResult, ERROR_RESPONSES
from app.api.deps import db_sessions

router = APIRouter()


@router.get("", response_model=schemas.UserResponse, responses=ERROR_RESPONSES)
async def read_users(
    *, db: AsyncSession = Depends(db_sessions["docker_db"]), filters: schemas.UsersFilterParams = Depends()
):

    services.user.db = db
    result = await services.user.get_users(filters=filters.dict())

    return await handle_result(result)


@router.get("/{user_id}", response_model=schemas.UserResponse, responses=ERROR_RESPONSES)
async def read_user_by_id(*, db: AsyncSession = Depends(db_sessions["docker_db"]), user_id: int) -> ServiceResult:

    services.user.db = db
    result = services.user.get_user_by_id(user_id=user_id)

    return handle_result(result)


@router.put("/{user_id}", response_model=schemas.UserResponse, responses=ERROR_RESPONSES)
async def update_user(
    *, db: AsyncSession = Depends(db_sessions["docker_db"]), user_id: int, user_in: schemas.UserUpdate
) -> ServiceResult:

    services.user.db = db
    result = services.user.update_user(user_id=user_id, user_in=user_in)

    return handle_result(result)


@router.delete("/{user_id}", response_model=schemas.UserResponse, responses=ERROR_RESPONSES)
async def delete_user(*, db: AsyncSession = Depends(db_sessions["docker_db"]), user_id: int) -> ServiceResult:

    services.user.db = db
    result = services.user.delete_user(user_id=user_id)

    return handle_result(result)


@router.post("", response_model=schemas.UserResponse, responses=ERROR_RESPONSES)
async def create_user(
    *, db: AsyncSession = Depends(db_sessions["docker_db"]), user_in: schemas.UserCreate
) -> ServiceResult:
    """
    Create new users.
    """
    services.user.db = db
    result = await services.user.create_user(obj_in=user_in)

    return await handle_result(result)
