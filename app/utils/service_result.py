import inspect
from loguru import logger
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.utils import AppExceptionCase


class ServiceResult(object):
    def __init__(self, arg):
        if isinstance(arg, AppExceptionCase):
            self.success = False
            self.exception_case = arg.expception_case
            self.status_code = arg.status_code
            self.result = arg
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
            self.result = JSONResponse(**arg)

    def __str__(self) -> str:
        if self.success:
            return "[Success]"
        return f'[Exception] "{self.exception_case}"'

    def __repr__(self) -> str:
        if self.success:
            return "<ServiceResult Success>"
        return f"<ServiceResult AppException {self.exception_case}>"

    def __enter__(self):
        return self.result

    def __exit__(self, *kwargs):
        pass


def caller_info() -> str:
    info = inspect.getframeinfo(inspect.stack()[2][0])
    return f"{info.filename}:{info.function}:{info.lineno}"


def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            raise exception
    with result as result:
        return result
