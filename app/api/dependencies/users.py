from app.schemas.user import UsersFilters


def get_users_filters(skip: int | None = 0, limit: int | None = 100) -> UsersFilters:
    return UsersFilters(
        skip=skip,
        limit=limit,
    )
