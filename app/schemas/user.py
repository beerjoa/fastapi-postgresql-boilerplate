from typing import Optional, Dict, Any, Union, List
from datetime import datetime
from pydantic import BaseModel
from app.schemas.message import ApiResponse


class UserBase(BaseModel):
    id: Optional[int]
    name: str
    password: str
    email: str
    created_at: Optional[datetime] = datetime.today()
    last_login: Optional[datetime] = datetime.today()


class UserCreate(BaseModel):
    name: str
    password: str
    email: str


class UserUpdate(UserCreate):
    pass


class UsersFilterParams(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 100


class UserResponse(ApiResponse):
    message: str = "User API Response"
    data: Optional[Union[UserBase, List[UserBase]]]
    detail: Optional[Dict[str, Any]] = {"key": "val"}

    class Config:
        orm_mode = True
