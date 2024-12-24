from typing import Generic, Type, TypeVar, Any
from uuid import UUID
from sqlalchemy.sql import select, insert, delete, update

from app.db.utils.base import Base as BaseModel, BaseView as BaseMovelView
from app.schemas.utils.base import BaseRecord as BaseRecord
from app.api.session import AsyncSession as AsyncSession
from app.daos.utils import exeptions

from .exeptions import (
    ItemNotFound, MissingUUID
)

ModelType = TypeVar("ModelType", bound=BaseModel|BaseMovelView)
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

    async def delete(self, db:AsyncSession, uuid:UUID) -> SchemaType:
        try:
            if not hasattr(self.model, 'uuid'):
                raise MissingUUID(self.model)

            statement = delete(self.model).where(
                self.model.uuid == uuid # type: ignore[attr-defined, unused-ignore]
            ).returning(self.model)
            result = await db.execute(statement)
            await db.commit()
            deleted_instance = result.fetchone()

            if not deleted_instance:
                raise exeptions.ItemNotFound()
            return self.schemaRecord.model_validate(deleted_instance[0]) # type: ignore[no-any-return]
        except Exception as e:
            print(f"Failed to delete {self.model.__tablename__}: {e}")
            raise e
        
    async def get(self, db: AsyncSession, uuid: UUID) -> SchemaType:
        try:
            if not hasattr(self.model, 'uuid'):
                raise MissingUUID(self.model)

            statement = select(self.model).where(
                self.model.uuid == uuid # type: ignore[attr-defined, unused-ignore]
            )
            result = (await db.execute(statement)).first()

            if result is None or len(result) <= 0:
                raise ItemNotFound()

            return self.schemaRecord.model_validate(result[0]) # type: ignore[no-any-return]
        except Exception as e:
            print(f"Failed to get {self.model.__tablename__}: {e}")
            raise e