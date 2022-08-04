from typing import Optional

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.crud.base import CRUDBase, ModelType, CreateSchemaType
from app.models.user import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # Declare model specific CRUD operation met

    async def get_duplicate_user(self, db: AsyncSession, obj_in: CreateSchemaType) -> Optional[ModelType]:
        query = select(self.model).where(or_(User.name == obj_in.name, User.email == obj_in.email))
        raw_result = await db.execute(query)
        user = raw_result.scalars().first()
        return user


crud_user = CRUDUser(User)
