from ._base import BaseDao
from backend.models import (
    TimeRangeEvent,
    TimeRangeEventNotDeleted
)
from backend.schemas import (
    TimeRangeEventRecord
)

class TimeRangeEventDao(BaseDao[TimeRangeEvent, TimeRangeEventRecord]):
    ...

time_range_event = TimeRangeEventNotDeleted()