from .utils.base import BaseDao
from app.db.models import (
    TimeRangeEvent,
    TimeRangeEventNotDeleted
)
from app.schemas import (
    TimeRangeEventTable
)

class TimeRangeEventDao(BaseDao[TimeRangeEvent, TimeRangeEventTable]):
    ...

time_range_event = TimeRangeEventDao(
    model=TimeRangeEvent,
    schemaRecord=TimeRangeEventTable
)