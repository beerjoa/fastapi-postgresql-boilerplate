from sqlalchemy import Column, Integer, String, DateTime
from app.database.base_class import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(Integer, nullable=False)
    created_at: Column(DateTime(timezone=True), nullable=True)
    last_login: Column(DateTime(timezone=True), nullable=True)
