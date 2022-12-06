from typing import Callable, Type

from app.services.base import BaseService


def get_service(service_type: Type[BaseService]) -> Callable[[], BaseService]:
    def _get_service() -> BaseService:
        return service_type()

    return _get_service
