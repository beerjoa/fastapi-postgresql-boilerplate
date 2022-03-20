from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    id: Optional[int]
    name: str
    password: str
    email: str
    created_at: Optional[datetime] = datetime.today()
    last_login: Optional[datetime] = datetime.today()


class UserCreate(UserBase):
    name: str
    password: str
    email: str


class UserUpdate(UserBase):
    id: int
    pass


class UserResponse(UserBase):
    class Config:
        orm_mode = True
