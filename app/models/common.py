from sqlalchemy import Column, DateTime, text
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class DateTimeModelMixin:
    created_at = Column(DateTime, server_default=text("now()"))
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
