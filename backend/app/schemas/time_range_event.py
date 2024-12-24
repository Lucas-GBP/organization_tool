from uuid import UUID
from datetime import datetime
from typing import Optional

from .utils.base import BaseRecord, BaseModel


"""
    HTTP Operations
"""
class TimeRangeEventPost(BaseModel):
    user_uuid:UUID
    start_time:datetime
    # Optional arguments
    category_id:Optional[int]
    sub_category_id:Optional[int]
    title:Optional[str]
    description:Optional[str]
    end_time:Optional[datetime]
class TimeRangeEventPatch(BaseModel):
    uuid:UUID
    start_time:datetime
    # Optional arguments
    category_id:Optional[int]
    sub_category_id:Optional[int]
    title:Optional[str]
    description:Optional[str]
    end_time:Optional[datetime]
class TimeRangeEventGetByRange(BaseModel):
    user_uuid:UUID
    start: datetime
    end: Optional[datetime]

"""
    Database Operations
"""
class TimeRangeEventNotDeleted(BaseModel):
    uuid:UUID

    user_id:int
    category_id:int|None
    sub_category_id:int|None
    title:str|None
    description:str|None
    start_time:datetime
    end_time:datetime|None
class TimeRangeEventCreate(BaseModel):
    user_uuid: UUID
    start_time:datetime
    # Optional arguments
    category_id:Optional[int]
    sub_category_id:Optional[int]
    title:Optional[str]
    description:Optional[str]
    end_time:Optional[datetime]
class TimeRangeEventUpdate(BaseModel):
    uuid: UUID
    start_time:datetime
    # Optional arguments
    category_id:int|None
    sub_category_id:int|None
    title:str|None
    description:str|None
    end_time:datetime|None

"""
    Database Objects
"""
class TimeRangeEventTable(BaseRecord):
    id:int
    uuid:UUID

    user_id:int
    category_id:int|None
    sub_category_id:int|None
    title:str|None
    description:str|None
    start_time:datetime
    end_time:datetime|None

    deleted_at:datetime|None
    
    def to_base_model(self) -> TimeRangeEventNotDeleted:
        return TimeRangeEventNotDeleted(
            uuid=self.uuid,
            user_id=self.user_id,
            category_id=self.category_id,
            sub_category_id=self.sub_category_id,
            title=self.title,
            description=self.description,
            start_time=self.start_time,
            end_time=self.end_time
        )


class TimeRangeEventNotDeletedView(BaseRecord):
    id:int
    uuid:UUID

    user_id:int
    category_id:int|None
    sub_category_id:int|None
    title:str|None
    description:str|None
    start_time:datetime
    end_time:datetime|None

    def to_base_model(self) -> TimeRangeEventNotDeleted:
        return TimeRangeEventNotDeleted(
            uuid=self.uuid,
            user_id=self.user_id,
            category_id=self.category_id,
            sub_category_id=self.sub_category_id,
            title=self.title,
            description=self.description,
            start_time=self.start_time,
            end_time=self.end_time
        )