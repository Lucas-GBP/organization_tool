from ._base import Base
from backend.db.utils import uuid_column, hex_color_column, CheckColorHex
from uuid import UUID as pyUUID
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .category import Category

class SubCategory(Base):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid:Mapped[pyUUID] = uuid_column()
    category_id:Mapped[int] = mapped_column(ForeignKey(Category.id, ondelete="CASCADE"))

    title:Mapped[str]
    color:Mapped[str|None] = hex_color_column()

    __table_args__ = (
        CheckColorHex("color"),
    )