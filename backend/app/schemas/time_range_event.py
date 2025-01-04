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
    category_uuid:Optional[UUID] = None
    sub_category_uuid:Optional[UUID] = None
    title:Optional[str] = None
    description:Optional[str] = None
    end_time:Optional[datetime] = None
class TimeRangeEventPatch(BaseModel):
    uuid:UUID
    start_time:datetime
    # Optional arguments
    category_uuid:Optional[UUID] = None
    sub_category_uuid:Optional[UUID] = None
    title:Optional[str] = None
    description:Optional[str] = None
    end_time:Optional[datetime]
class TimeRangeEventGetByRange(BaseModel):
    user_uuid:UUID
    start: datetime
    end: Optional[datetime]

"""
    Database Operations
"""
class TimeRangeEvent(BaseModel):
    uuid:UUID

    category_uuid:UUID|None
    sub_category_uuid:UUID|None
    title:str|None
    description:str|None
    start_time:datetime
    end_time:datetime|None

    deleted_at:datetime|None
class TimeRangeEventNotDeleted(BaseModel):
    uuid:UUID

    category_uuid:UUID|None
    sub_category_uuid:UUID|None
    title:str|None
    description:str|None
    start_time:datetime
    end_time:datetime|None
class TimeRangeEventCreate(BaseModel):
    user_uuid: UUID
    start_time:datetime
    # Optional arguments
    category_uuid:Optional[UUID]
    sub_category_uuid:Optional[UUID]
    title:Optional[str]
    description:Optional[str]
    end_time:Optional[datetime]
class TimeRangeEventUpdate(BaseModel):
    uuid: UUID
    start_time:datetime
    # Optional arguments
    category_uuid:UUID|None
    sub_category_uuid:UUID|None
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
    
    def to_base_model(
        self, 
        category_uuid:UUID|None = None, 
        sub_category_uuid:UUID|None = None
    ) -> TimeRangeEvent:
        return TimeRangeEvent(
            uuid=self.uuid,
            category_uuid=category_uuid,
            sub_category_uuid=sub_category_uuid,
            title=self.title,
            description=self.description,
            start_time=self.start_time,
            end_time=self.end_time,
            deleted_at=self.deleted_at
        )
class TimeRangeEventNotDeletedView(BaseRecord):
    id:int
    uuid:UUID

    category_id:int|None
    sub_category_id:int|None
    title:str|None
    description:str|None
    start_time:datetime
    end_time:datetime|None

    def to_base_model(
        self, 
        category_uuid:UUID|None = None, 
        sub_category_uuid:UUID|None = None
    ) -> TimeRangeEventNotDeleted:
        return TimeRangeEventNotDeleted(
            uuid=self.uuid,
            category_uuid=category_uuid,
            sub_category_uuid=sub_category_uuid,
            title=self.title,
            description=self.description,
            start_time=self.start_time,
            end_time=self.end_time
        )