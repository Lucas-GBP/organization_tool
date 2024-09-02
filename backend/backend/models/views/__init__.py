from alembic_utils.pg_view import PGView

from ..time_range_event import (
    time_range_event_not_deleted
)

view_entities:list[PGView] = [
    time_range_event_not_deleted
]