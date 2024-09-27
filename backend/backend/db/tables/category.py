from uuid import UUID as pyUUID
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ._base import Base
from backend.db.utils import uuid_column, hex_color_column, CheckColorHex
from .user import User

class Category(Base):
    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    uuid:Mapped[pyUUID] = uuid_column()
    user_id:Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))

    title:Mapped[str]
    color:Mapped[str|None] = hex_color_column()
    description:Mapped[str|None]

    __table_args__ = (
        CheckColorHex("color"),
    )