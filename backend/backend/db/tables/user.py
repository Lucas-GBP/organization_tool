from ._base import Base
from backend.db.utils import uuid_column
from uuid import UUID as pyUUID
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid:Mapped[pyUUID] = uuid_column()
    name:Mapped[str]