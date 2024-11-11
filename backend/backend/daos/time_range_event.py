from .utils.base import BaseDao
from backend.db.models import (
    TimeRangeEvent,
    TimeRangeEventNotDeleted
)
from backend.schemas import (
    TimeRangeEventTable
)

class TimeRangeEventDao(BaseDao[TimeRangeEvent, TimeRangeEventTable]):
    ...

time_range_event = TimeRangeEventDao(
    model=TimeRangeEvent,
    schemaRecord=TimeRangeEventTable
)