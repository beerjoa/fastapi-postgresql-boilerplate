from datetime import datetime
from typing import Any, Dict, List

from pydantic import BaseModel

from app.core import security
from app.schemas.message import ApiResponse


class UserBase(BaseModel):
    id: int | None
    username: str
    email: str
    created_at: datetime | None
    updated_at: datetime | None
    deleted_at: datetime | None

    class Config:
        orm_mode = True


class UserInDB(UserBase):
    salt: str | None
    hashed_password: str | None

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
    username: str | None
    password: str | None
    email: str | None


class UsersFilters(BaseModel):
    skip: int | None = 0
    limit: int | None = 100


class UserTokenData(BaseModel):
    access_token: str | None
    token_type: str | None


class UserAuthOutData(UserBase):
    token: UserTokenData | None

    class Config:
        fields = {
            "salt": {"exclude": True},
            "hashed_password": {"exclude": True},
        }


class UserOutData(UserBase):
    class Config:
        fields = {
            "salt": {"exclude": True},
            "hashed_password": {"exclude": True},
        }


class UserResponse(ApiResponse):
    message: str = "User API Response"
    data: UserOutData | List[UserOutData] | UserAuthOutData
    detail: Dict[str, Any] | None = {"key": "val"}
