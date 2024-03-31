from .base import Base
from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str]