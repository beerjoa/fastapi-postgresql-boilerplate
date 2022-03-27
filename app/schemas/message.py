from typing import Optional, Dict, Any
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    app_exception: str = "FailToSendAlert"
    context: Optional[Dict[str, Any]] = {"reason": "Not Connected with notification channel"}

    class Config:
        orm_mode = True


class ApiResponse(BaseModel):
    message: str = "default response message"
    data: BaseModel
    detail: Optional[Dict[str, Any]] = {"key": "val"}

    class Config:
        orm_mode = True
