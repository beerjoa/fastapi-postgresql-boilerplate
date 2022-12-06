from datetime import datetime

from pydantic import BaseModel


class TokenBase(BaseModel):
    exp: datetime
    sub: str


class TokenUser(BaseModel):
    id: int
    username: str
    email: str
