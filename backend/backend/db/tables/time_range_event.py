from datetime import datetime as Pydatetime
from uuid import UUID
from sqlalchemy import ForeignKey, DateTime, select
from sqlalchemy.orm import mapped_column, MappedColumn as Mapped

from backend.db.utils import (
    Base, BaseView,
    uuid_column, primary_id_column,
    view_entity
)
from .category import Category
from .sub_category import SubCategory
from .user import User

class TimeRangeEvent(Base):
    id:Mapped[int] = primary_id_column()
    uuid:Mapped[UUID] = uuid_column()

    user_id:Mapped[int] = mapped_column(ForeignKey(User.id))
    category_id:Mapped[int|None] = mapped_column(ForeignKey(Category.id), nullable=True)
    sub_category_id:Mapped[int|None] = mapped_column(
        ForeignKey(SubCategory.id), nullable=True
    )
    title:Mapped[str|None]
    description:Mapped[str|None]
    start_time:Mapped[Pydatetime] = mapped_column(DateTime)
    end_time:Mapped[Pydatetime|None] = mapped_column(DateTime, nullable=True)

    deleted_at:Mapped[Pydatetime|None] = mapped_column(DateTime, nullable=True)

class TimeRangeEventNotDeleted(BaseView):
    id:Mapped[int] = primary_id_column()
    uuid:Mapped[UUID]

    user_id:Mapped[int]
    category_id:Mapped[int|None]
    sub_category_id:Mapped[int|None]
    title:Mapped[str|None]
    description:Mapped[str|None]
    start_time:Mapped[Pydatetime]
    end_time:Mapped[Pydatetime|None]

time_range_event_not_deleted = view_entity(
    TimeRangeEventNotDeleted,
    select(TimeRangeEventNotDeleted).where(TimeRangeEvent.deleted_at.is_not(None))
)