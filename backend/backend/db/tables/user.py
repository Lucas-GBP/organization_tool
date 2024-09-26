from backend.db.utils import Base, uuid_column, primary_id_column
from uuid import UUID
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    id:Mapped[int] = primary_id_column()
    uuid:Mapped[UUID] = uuid_column()
    name:Mapped[str] = mapped_column(String)