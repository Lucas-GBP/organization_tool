from alembic_utils.pg_view import PGView

from backend.db.tables.time_range_event import (
    TimeRangeEventNotDeleted,
    time_range_event_not_deleted,
)

view_entities:list[PGView] = [
    time_range_event_not_deleted
]