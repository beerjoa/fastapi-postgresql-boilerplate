from sqlalchemy.orm import declarative_base, declared_attr


class RWModel:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __name__: str


RWModel = declarative_base(cls=RWModel)
