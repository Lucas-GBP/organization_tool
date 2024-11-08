from enum import Enum

from .views import (
    view_entities
)
from .functions import  (
    function_entities
)
from .triggers import (
    trigger_entities
)

# All the entities for the alembic_utils
entities = function_entities + view_entities + trigger_entities

class Schemas(Enum):
    public = 0
    users = 1