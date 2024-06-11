from ._base import Base
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .user import User

class Category(Base):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id:Mapped[int] = mapped_column(ForeignKey(f"{User.__tablename__}.id"))