from app.db.utils import Base, primary_id_column
from app.db.tables import User
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class UserInfo(Base):
    id:Mapped[int] = primary_id_column()
    user_id:Mapped[int] = mapped_column(ForeignKey(User.id, ondelete="CASCADE"))
    first_name:Mapped[str] = mapped_column(String)
    last_name:Mapped[str] = mapped_column(String)
    email:Mapped[str] = mapped_column(String)