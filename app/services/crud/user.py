from typing import Optional

from sqlalchemy.orm import Session

from app.services.crud.base import CRUDBase, ModelType, CreateSchemaType
from app.models.user import User
from app.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # Declare model specific CRUD operation met

    def get_duplicate_user(self, db: Session, obj_in: CreateSchemaType) -> Optional[ModelType]:
        user = db.query(User).filter((User.name == obj_in.name) | (User.email == obj_in.email)).first()
        return user


crud_user = CRUDUser(User)
