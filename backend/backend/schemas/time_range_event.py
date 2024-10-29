from uuid import UUID
from datetime import datetime

from ._base import BaseRecord, BaseModel


"""
    HTTP Operations
"""

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

    def to_base_model(self):
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