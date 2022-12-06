from typing import Any, Dict

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    app_exception: str = "FailToSendAlert"
    context: Dict[str, Any] | None = {"reason": "Not Connected with notification channel"}

    class Config:
        orm_mode = True


class ApiResponse(BaseModel):
    message: str = "default response message"
    data: BaseModel
    detail: Dict[str, Any] | None = {"key": "val"}

    class Config:
        orm_mode = True
