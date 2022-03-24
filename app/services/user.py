from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.utils import ServiceResult, response_4xx
from app.services.base import BaseService
from app.services.crud import crud_user, CreateSchemaType, UpdateSchemaType


class UserService(BaseService):
    def get_user_by_id(self, user_id: int) -> ServiceResult:
        user = crud_user.get(self.db, model_id=user_id)
        if not user:
            return ServiceResult(
                response_4xx(
                    status_code=HTTP_404_NOT_FOUND,
                    context={"reason": f"User with ID:{user_id} does not exist."},
                )
            )

        return ServiceResult(
            dict(
                status_code=HTTP_200_OK,
                content={"message": f"id: {user_id} user", "data": jsonable_encoder(user)},
            )
        )

    def get_users(self, filters: dict) -> ServiceResult:
        users = crud_user.get_multi(self.db, **filters)
        if not users:
            return ServiceResult(response_4xx(status_code=HTTP_404_NOT_FOUND, context={"reason": "there are no users"}))

        return ServiceResult(
            dict(
                status_code=HTTP_200_OK,
                content={"message": "filtered users", "data": jsonable_encoder(users)},
            )
        )

    def create_user(self, obj_in: CreateSchemaType) -> ServiceResult:
        duplicate_user = crud_user.get_duplicate_user(self.db, obj_in=obj_in)

        if duplicate_user:
            return ServiceResult(
                response_4xx(status_code=HTTP_400_BAD_REQUEST, context={"reason": "already created user"})
            )

        created_user = crud_user.create(self.db, obj_in=obj_in)
        return ServiceResult(
            dict(
                status_code=HTTP_201_CREATED,
                content={"message": "created user", "data": jsonable_encoder(created_user)},
            )
        )

    def update_user(self, user_id: int, user_in: UpdateSchemaType) -> ServiceResult:
        user = crud_user.get(self.db, model_id=user_id)

        if not user:
            return ServiceResult(
                response_4xx(
                    status_code=HTTP_404_NOT_FOUND,
                    context={"reason": f"User with ID:{user_id} does not exist."},
                )
            )

        updated_user = crud_user.update(self.db, db_obj=user, obj_in=user_in)
        return ServiceResult(
            dict(
                status_code=HTTP_201_CREATED,
                content={"message": "updated user", "data": jsonable_encoder(updated_user)},
            )
        )

    def delete_user(self, user_id: int) -> ServiceResult:
        user = crud_user.get(self.db, model_id=user_id)

        if not user:
            return ServiceResult(
                response_4xx(
                    status_code=HTTP_404_NOT_FOUND,
                    context={"reason": f"User with ID:{user_id} does not exist."},
                )
            )

        deleted_user = crud_user.delete(self.db, model_id=user_id)
        return ServiceResult(
            dict(
                status_code=HTTP_200_OK,
                content={"message": "deleted user", "data": jsonable_encoder(deleted_user)},
            )
        )


service_user = UserService()
