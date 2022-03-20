from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api.deps import db_sessions

router = APIRouter()


@router.get("", response_model=List[schemas.UserResponse])
def read_user(
    db: Session = Depends(db_sessions["docker_db"]),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("", response_model=schemas.UserResponse)
def create_user(*, db: Session = Depends(db_sessions["docker_db"]), user_in: schemas.UserCreate) -> Any:
    """
    Create new users.
    """
    print(user_in)
    user = crud.user.create(db, obj_in=user_in)
    return user
