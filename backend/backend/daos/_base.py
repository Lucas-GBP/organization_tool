from typing import Generic, Type, TypeVar
from uuid import UUID

from backend.db.tables._base import Base as BaseModel
from backend.schemas._base import BaseRecord

ModelType = TypeVar("ModelType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseRecord)


class BaseDao(Generic[ModelType, SchemaType]):
    def __init__(self, model: Type[ModelType], schemaRecord: Type[SchemaType]):
        """
        Dao object with default methods to Create, Read, Update, Delete (Dao).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schemaRecord`: A Pydantic model (schema) class
        """
        self.model = model
        self.schemaRecord = schemaRecord