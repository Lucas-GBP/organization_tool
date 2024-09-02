from re import sub
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr

ts_vector_dict = 'portuguesedict'

class Base(DeclarativeBase):
    """
    Base class for sqlalchemy tables/models
    """
    @declared_attr #type: ignore
    def __tablename__(cls) -> str:
        name = sub(r"(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)
        name = sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()
        return name

class BaseView(DeclarativeBase):
    """
    Base class for sqlalchemy tables/models
    """
    @declared_attr #type: ignore
    def __tablename__(cls) -> str:
        name = sub(r"(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)
        name = sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()
        return name