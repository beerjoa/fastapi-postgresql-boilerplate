import inspect

from fastapi.responses import JSONResponse
from loguru import logger

from app.utils import AppExceptionCase


class ServiceResult:
    def __init__(self, args):
        if isinstance(args, AppExceptionCase):
            self.success = False
            self.exception_case = args.exception_case
            self.status_code = args.status_code
            self.result = args
        else:
            self.success = True
            self.exception_case = None
            self.status_code = None
            self.result = JSONResponse(**args)

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


async def handle_result(result: ServiceResult):
    if not result.success:
        with result as exception:
            logger.error(f"{exception} | caller={caller_info()}")
            raise exception
    with result as result:
        return result


def return_service(service_func) -> ServiceResult:
    async def wrapper(*args, **kwargs):
        sf = await service_func(*args, **kwargs)

        return ServiceResult(sf)

    return wrapper
