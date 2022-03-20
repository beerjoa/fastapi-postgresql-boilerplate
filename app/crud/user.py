from typing import Optional, List, TypeVar

from sqlalchemy.orm import Session

from fastapi.encoders import jsonable_encoder
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas import UserCreate, UserUpdate

from pydantic import BaseModel

from app.database.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    # Declare model specific CRUD operation methods.

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        user = db.query(self.model).filter(User.name == obj_in_data["name"]).first()

        if user:
            return user
        else:
            obj_in_data = obj_in.dict(exclude_unset=True)
            db_obj = self.model(**obj_in_data)

            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj


user = CRUDUser(User)
