from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core import settings


class Session:
    def __init__(self, db_name: str):
        self.db_url = settings.db_url_conf.dict()
        self.engine = create_async_engine(url=self.db_url[db_name], echo=True, future=True)

    async def get_session(self):
        return sessionmaker(
            bind=self.engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
        )
