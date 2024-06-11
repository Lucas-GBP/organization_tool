import re
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

ts_vector_dict = 'portuguesedict'


class Base(DeclarativeBase):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)  # type: ignore
        name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name).lower()
        return name