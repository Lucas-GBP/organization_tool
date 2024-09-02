from typing import Generic, Type, TypeVar
from uuid import UUID
from sqlalchemy.sql import select, insert, delete, update

from backend.models.utils.base import Base as BaseModel
from backend.schemas._base import BaseRecord
from backend.api.session import AsyncSession

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

    async def delete(self, db:AsyncSession, uuid:UUID):
        try:
            statement = delete(self.model).where(
                self.model.uuid == uuid
            )
            await db.execute(statement)
            await db.commit()
        except Exception as e:
            print(f"Failed to delete {self.model.__tablename__}: {e}")
            raise e
        
    async def get(self, db: AsyncSession, uuid: UUID):
        try:
            statement = select(self.model).where(
                self.model.uuid == uuid
            )
            result = (await db.execute(statement)).first()

            return self.schemaRecord.model_validate(result[0]) if result else None
        except Exception as e:
            print(f"Failed to get {self.model.__tablename__}: {e}")
            raise e