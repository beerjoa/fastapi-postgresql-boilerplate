from typing import Any, Dict, List, Optional, Union

from app.schemas.user import UserInCreate, UserInUpdate, UserResponse, UsersFilters


def get_users_filters(skip: int | None = 0, limit: int | None = 100) -> UsersFilters:
    return UsersFilters(
        skip=skip,
        limit=limit,
    )
