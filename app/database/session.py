from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import settings


class CustomSession:
    def __init__(self, db_name: str):
        self.db_url = settings.DB_URL_CONF.dict()
        self.engine = create_engine(
            url=self.db_url[db_name],
            pool_pre_ping=True,
        )

    def get_session(self):
        return sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
