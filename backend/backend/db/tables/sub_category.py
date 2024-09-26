from backend.db.utils import (
    Base, 
    BaseView, 
    primary_id_column,
    uuid_column, 
    hex_color_column, 
    CheckColorHex
)
from uuid import UUID
from sqlalchemy import Integer, String, ForeignKey, select
from sqlalchemy.orm import MappedColumn, mapped_column

from .category import Category

class SubCategory(Base):
    id:MappedColumn[int] = primary_id_column()
    uuid:MappedColumn[UUID] = uuid_column()
    category_id:MappedColumn[int] = mapped_column(ForeignKey(Category.id, ondelete="CASCADE"))

    title:MappedColumn[str] = mapped_column(String)
    color:MappedColumn[str] = hex_color_column()

    __table_args__ = (
        CheckColorHex(color),
    )

class SubCategoryWithoutColor(BaseView):
    id:MappedColumn[int] = mapped_column(Integer, primary_key=True)
    uuid:MappedColumn[UUID] = uuid_column()
    category_id:MappedColumn[int] = mapped_column(ForeignKey(Category.id, ondelete="CASCADE"))
    title:MappedColumn[str]