from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.utils import ServiceResult, response_4xx, return_service
from app.services.base import BaseService
from app.services.crud import crud_user, CreateSchemaType, UpdateSchemaType


class UserService(BaseService):
    @return_service
    def get_user_by_id(self, user_id: int) -> ServiceResult:
        user = crud_user.get(self.db, model_id=user_id)
        if not user:
            return response_4xx(
                status_code=HTTP_404_NOT_FOUND,
                context={"reason": f"User with ID:{user_id} does not exist."},
            )

        return dict(
            status_code=HTTP_200_OK,
            content={"message": f"id: {user_id} user", "data": jsonable_encoder(user)},
        )

    @return_service
    async def get_users(self, filters: dict) -> ServiceResult:
        users = await crud_user.get_multi(self.db, **filters)

        if not users:
            return response_4xx(status_code=HTTP_404_NOT_FOUND, context={"reason": "there are no users"})

        return dict(
            status_code=HTTP_200_OK,
            content={"message": "filtered users", "data": jsonable_encoder(users)},
        )

    @return_service
    async def create_user(self, obj_in: CreateSchemaType) -> ServiceResult:
        duplicate_user = await crud_user.get_duplicate_user(self.db, obj_in=obj_in)

        if duplicate_user:
            return response_4xx(status_code=HTTP_400_BAD_REQUEST, context={"reason": "already created user"})

        created_user = await crud_user.create(self.db, obj_in=obj_in)
        return dict(
            status_code=HTTP_201_CREATED,
            content={"message": "created user", "data": jsonable_encoder(created_user)},
        )

    @return_service
    async def update_user(self, user_id: int, user_in: UpdateSchemaType) -> ServiceResult:
        user = await crud_user.get(self.db, model_id=user_id)

        if not user:
            return response_4xx(
                status_code=HTTP_404_NOT_FOUND,
                context={"reason": f"User with ID:{user_id} does not exist."},
            )

        updated_user = await crud_user.update(self.db, db_obj=user, obj_in=user_in)
        return dict(
            status_code=HTTP_200_OK,
            content={"message": "updated user", "data": jsonable_encoder(updated_user)},
        )

    @return_service
    async def delete_user(self, user_id: int) -> ServiceResult:
        user = await crud_user.get(self.db, model_id=user_id)

        if not user:
            return response_4xx(
                status_code=HTTP_404_NOT_FOUND,
                context={"reason": f"User with ID:{user_id} does not exist."},
            )

        deleted_user = await crud_user.delete(self.db, db_obj=user)
        return dict(
            status_code=HTTP_200_OK,
            content={"message": "deleted user", "data": jsonable_encoder(deleted_user)},
        )


service_user = UserService()
