from typing import Type, TypeVar
from app.db.utils.base import Base as BaseModel, BaseView as BaseMovelView

ModelType = TypeVar("ModelType", bound=BaseModel|BaseMovelView)

"""
    Generic DAO's Exeptions
"""
class GenerticDaoError(Exception):
    def __init__(self, table:Type[ModelType]|None) -> None:
        if not table:
            super().__init__("Some error :p")
        else:
            super().__init__(f"Some error doing stuff in {table.__tablename__}")
        return
class ItemNotFound(Exception):
    def __init__(self) -> None:
        super().__init__("Item not found in the database")
        return
class MissingUUID(Exception):
    def __init__(self, table:Type[ModelType]) -> None:
        super().__init__(f"{table.__tablename__} does not have a 'uuid' field.")
        return
class FailuredToPost(Exception):
    def __init__(self) -> None:
        super().__init__(f"Failed to Post data.")
        return
class FailureToPatch(Exception):
    def __init__(self, table:Type[ModelType]) -> None:
        super().__init__(f"Failed to Patch data into {table.__tablename__}.")
        return

"""
    Timer Exeptions
"""
class TimerAlreadyRunning(Exception):
    def __init__(self) -> None:
        super().__init__(f"A timer is already ruinning")
        return