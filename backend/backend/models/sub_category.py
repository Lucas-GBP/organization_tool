from ._base import Base
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .category import Category

class SubCategory(Base):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    category_id:Mapped[int] = mapped_column(ForeignKey(f"{Category.__tablename__}.id"))

    data:Mapped[float]