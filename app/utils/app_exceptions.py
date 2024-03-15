from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.schemas.message import ErrorResponse

ERROR_RESPONSES = {
    status.HTTP_400_BAD_REQUEST: {
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "app_exception": "Response4XX",
                    "context": {"reason": "clinet error"},
                }
            }
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {
                    "app_exception": "Response5XX",
                    "context": {"error": "server error"},
                }
            }
        },
    },
}


class AppExceptionCase(Exception):
    def __init__(self, status_code: int, context: dict):
        self.exception_case = self.__class__.__name__
        self.status_code = status_code
        self.context = context

    def __str__(self):
        return f"<AppException {self.exception_case}> - " + f"status_code={self.status_code} - context={self.context}>"


async def app_exception_handler(request: Request, exc: AppExceptionCase):
    return JSONResponse(
        status_code=exc.status_code,
        content={"app_exception": exc.exception_case, "context": exc.context},
    )


class AppException:
    class Response4XX(AppExceptionCase):
        """
        Response4XX
        """

        def __init__(
            self,
            status_code: status = status.HTTP_400_BAD_REQUEST,
            context: dict = None,
        ):
            # status_code = status_code
            AppExceptionCase.__init__(self, status_code, context)

    class Response5XX(AppExceptionCase):
        """
        Response5XX
        """

        def __init__(self, context: dict = None):
            status_code = 500
            AppExceptionCase.__init__(self, status_code, context)


response_4xx = AppException.Response4XX
response_5xx = AppException.Response5XX
