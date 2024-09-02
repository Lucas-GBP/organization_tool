from uuid import UUID
from datetime import datetime

from ._base import BaseRecord, BaseModel


class TimeRangeEventRecord(BaseRecord):
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

class TimeRangeEventNotDeletedRecord(BaseRecord):
    id:int
    uuid:UUID

    user_id:int
    category_id:int|None
    sub_category_id:int|None
    title:str|None
    description:str|None
    start_time:datetime
    end_time:datetime|None

