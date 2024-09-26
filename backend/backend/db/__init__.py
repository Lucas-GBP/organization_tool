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