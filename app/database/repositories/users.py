from datetime import datetime
from typing import List

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncConnection

from app.database.repositories.base import BaseRepository
from app.models.user import User
from app.schemas.user import UserInCreate, UserInDB, UserInSignIn, UserInUpdate


class UsersRepository(BaseRepository):
    def __init__(self, conn: AsyncConnection) -> None:
        super().__init__(conn)

    #
    async def get_user_password_validation(self, *, user: User, password: str) -> bool:
        user_password_checked = user.check_password(password=password)
        return user_password_checked

    #
    async def get_user_by_id(self, *, user_id: int) -> User:
        query = select(User).where(User.id == user_id).limit(1)

        raw_result = await self.connection.execute(query)
        result = raw_result.fetchone()
        return result.User if result is not None else result

    async def get_user_by_email(self, *, email: str) -> User:
        query = select(User).where(and_(User.email == email, User.deleted_at.is_(None)))
        raw_result = await self.connection.execute(query)
        result = raw_result.fetchone()
        return result.User if result is not None else result

    async def get_duplicated_user(self, *, user_in: UserInCreate) -> User:
        query = select(User).where(
            and_(or_(User.username == user_in.username, User.email == user_in.email), User.deleted_at.is_(None))
        )
        raw_result = await self.connection.execute(query)
        result = raw_result.fetchone()
        return result.User if result is not None else result

    async def get_filttered_users(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[User]:
        query = select(User).offset(skip).limit(limit)

        raw_results = await self.connection.execute(query)
        results = raw_results.scalars().all()
        return results

    #
    async def signup_user(self, *, user_in: UserInCreate) -> User:
        user_in_db_obj = UserInDB(
            username=user_in.username,
            email=user_in.email,
        )
        user_in_db_obj.change_password(user_in.password)

        created_user = User(**user_in_db_obj.dict(exclude_none=True))
        self.connection.add(created_user)
        await self.connection.commit()
        await self.connection.refresh(created_user)
        return created_user

    async def update_user(self, *, user: User, user_in: UserInUpdate) -> User:
        user_in_obj = user_in.dict(exclude_unset=True)
        if user_in.password:
            user.change_password(user_in.password)

        for (key, val) in user_in_obj.items():
            setattr(user, key, val)

        self.connection.add(user)
        await self.connection.commit()
        await self.connection.refresh(user)
        return user

    async def delete_user(self, *, user: User) -> User:
        user.deleted_at = datetime.utcnow()
        self.connection.add(user)
        await self.connection.commit()
        await self.connection.refresh(user)
        return user
