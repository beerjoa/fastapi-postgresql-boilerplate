from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.core import security
from app.schemas.message import ApiResponse


class UserBase(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int | None = None
    username: str
    email: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class UserInDB(UserBase):
    salt: str | None = None
    hashed_password: str | None = None

    def check_password(self, password: str) -> bool:
        return security.verify_password(self.salt + password, self.hashed_password)

    def change_password(self, password: str) -> None:
        self.salt = security.generate_salt()
        self.hashed_password = security.get_password_hash(self.salt + password)


class UserInSignIn(BaseModel):
    password: str
    email: str


class UserInCreate(BaseModel):
    username: str
    password: str
    email: str


class UserInUpdate(UserInCreate):
    username: str | None = None
    password: str | None = None
    email: str | None = None


class UsersFilters(BaseModel):
    skip: int | None = 0
    limit: int | None = 100


class UserTokenData(BaseModel):
    access_token: str | None = None
    token_type: str | None = None


class UserAuthOutData(UserBase):
    token: UserTokenData | None = None


class UserOutData(UserBase):
    pass


class UserResponse(ApiResponse):
    message: str = "User API Response"
    data: UserOutData | list[UserOutData] | UserAuthOutData
    detail: dict[str, Any] | None = {"key": "val"}
