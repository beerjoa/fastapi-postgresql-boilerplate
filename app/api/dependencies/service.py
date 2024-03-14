from collections.abc import Callable

from app.services.base import BaseService


def get_service(service_type: type[BaseService]) -> Callable[[], BaseService]:
    def _get_service() -> BaseService:
        return service_type()

    return _get_service
