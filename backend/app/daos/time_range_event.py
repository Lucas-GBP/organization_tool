from datetime import datetime
from uuid import UUID
from typing import AsyncGenerator, overload
from sqlalchemy.sql import select, insert, update, delete

from .utils.base import BaseDao
from app.db import models
from app import schemas
from app.api.session import AsyncSession
from app.daos.utils import exeptions

class TimeRangeEventDao(BaseDao[models.TimeRangeEvent, schemas.TimeRangeEventTable]):
    async def get_not_deleted(
        self,
        db: AsyncSession, 
        uuid: UUID
    ) -> schemas.TimeRangeEventNotDeleted:
        try:
            statement = select(
                models.TimeRangeEventNotDeleted.uuid,
                models.TimeRangeEventNotDeleted.title,
                models.TimeRangeEventNotDeleted.description,
                models.TimeRangeEventNotDeleted.start_time,
                models.TimeRangeEventNotDeleted.end_time,
                models.Category.uuid.label("category_uuid"),
                models.SubCategory.uuid.label("sub_category_uuid")
            ).join(
                models.Category,  # Tabela com a qual será feito o join
                models.Category.id == models.TimeRangeEventNotDeleted.category_id,
                isouter=True  # LEFT JOIN
            ).join(
                models.SubCategory,  # Outra tabela para join
                models.SubCategory.id == models.TimeRangeEventNotDeleted.sub_category_id,
                isouter=True  # LEFT JOIN
            ).where(
                models.TimeRangeEventNotDeleted.uuid == uuid
            )
            result = (await db.execute(statement)).one()

            return schemas.TimeRangeEventNotDeleted.model_validate(result._mapping)
        except Exception as e:
            print(f'Failed to get all {self.model.__tablename__}: {e}')
            raise e
    async def get_by_time_range(
        self,
        db: AsyncSession,
        start: datetime,
        end: datetime|None,
        user_uuid: UUID,
        limit: int = 50
    ) -> AsyncGenerator[schemas.TimeRangeEventNotDeleted, None]:
        try:
            statement = select(
                models.TimeRangeEventNotDeleted.uuid,
                models.TimeRangeEventNotDeleted.title,
                models.TimeRangeEventNotDeleted.description,
                models.TimeRangeEventNotDeleted.start_time,
                models.TimeRangeEventNotDeleted.end_time,
                models.Category.uuid.label("category_uuid"),
                models.SubCategory.uuid.label("sub_category_uuid")
            ).join(
                models.Category,  # Tabela com a qual será feito o join
                models.Category.id == models.TimeRangeEventNotDeleted.category_id,
                isouter=True  # LEFT JOIN
            ).join(
                models.SubCategory,  # Outra tabela para join
                models.SubCategory.id == models.TimeRangeEventNotDeleted.sub_category_id,
                isouter=True  # LEFT JOIN
            ).limit(limit)
            if end:
                statement = statement.where(
                    models.TimeRangeEventNotDeleted.user_id == select(models.User.id).where(
                        models.User.uuid == user_uuid
                    ).scalar_subquery(),
                    models.TimeRangeEventNotDeleted.start_time >= start,
                    models.TimeRangeEventNotDeleted.end_time <= end
                )
            else:
                statement = statement.where(
                    models.TimeRangeEventNotDeleted.user_id == select(models.User.id).where(
                        models.User.uuid == user_uuid
                    ).scalar_subquery(),
                    models.TimeRangeEventNotDeleted.start_time >= start
                )

            result = (await db.execute(statement)).all()
            for event in result:
                yield schemas.TimeRangeEventNotDeleted.model_validate(event._mapping)
        except Exception as e:
            print(f'Failed to get all {self.model.__tablename__}: {e}')
            raise e
    async def get_running_timer(
        self,
        db: AsyncSession,
        user_uuid: UUID
    ) -> schemas.TimeRangeEventNotDeleted|None:
        try:
            statement = select(
                models.TimeRangeEventNotDeleted.uuid,
                models.TimeRangeEventNotDeleted.title,
                models.TimeRangeEventNotDeleted.description,
                models.TimeRangeEventNotDeleted.start_time,
                models.TimeRangeEventNotDeleted.end_time,
                models.Category.uuid.label("category_uuid"),
                models.SubCategory.uuid.label("sub_category_uuid")
            ).join(
                models.Category,  # Tabela com a qual será feito o join
                models.Category.id == models.TimeRangeEventNotDeleted.category_id,
                isouter=True  # LEFT JOIN
            ).join(
                models.SubCategory,  # Outra tabela para join
                models.SubCategory.id == models.TimeRangeEventNotDeleted.sub_category_id,
                isouter=True  # LEFT JOIN
            ).where(
                models.TimeRangeEventNotDeleted.user_id == select(models.User.id).where(
                    models.User.uuid == user_uuid,
                ).scalar_subquery(),
                models.TimeRangeEventNotDeleted.end_time == None
            )
            result = (await db.execute(statement)).first()

            if result is None or len(result) <= 0:
                return None
            return schemas.TimeRangeEventNotDeleted.model_validate(result._mapping)
        except Exception as e:
            print(f'Failed to get {self.model.__tablename__}: {e}')
            raise e
    async def post(
        self,
        db: AsyncSession,
        data: schemas.TimeRangeEventCreate
    ) -> schemas.TimeRangeEventTable:
        try:
            statement = insert(models.TimeRangeEvent).values(
                user_id = select(models.User.id).where(
                    models.User.uuid == data.user_uuid
                ).scalar_subquery(),
                category_id = select(models.Category.id).where(
                    models.Category.uuid == data.category_uuid
                ).scalar_subquery(),
                sub_category_id = select(models.SubCategory.id).where(
                    models.SubCategory.uuid == data.sub_category_uuid
                ).scalar_subquery(),
                title = data.title,
                description = data.description,
                start_time = data.start_time,
                end_time = data.end_time
            ).returning(models.TimeRangeEvent)

            result = (await db.execute(statement)).one()

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            running_timer = await self.get_running_timer(db=db, user_uuid=data.user_uuid)
            if running_timer:
                raise exeptions.TimerAlreadyRunning()
            print(f'Failed to create {self.model.__tablename__}: {e}')
            raise e
    async def patch(
        self,
        db: AsyncSession,
        data: schemas.TimeRangeEventUpdate
    ) -> schemas.TimeRangeEventTable:
        try:
            values = data.model_dump(exclude_unset=True)
            if "category_uuid" in values:
                values["category_id"] = select(models.Category.id).where(
                    models.Category.uuid == values["category_uuid"]
                ).scalar_subquery()
                values.pop("category_uuid", None)
            if "sub_category_uuid" in values:
                values["sub_category_id"] = select(models.SubCategory.id).where(
                    models.SubCategory.uuid == values["sub_category_uuid"]
                ).scalar_subquery()
                values.pop("sub_category_uuid", None)
            print(f"\n\n\nvalues: {values}\n\n\n")

            statement = update(
                self.model
            ).where(
                self.model.uuid == data.uuid
            ).values(
                values
            ).returning(self.model)

            result = (await db.execute(statement)).one()
            if result is None or len(result) <= 0:
                raise exeptions.FailureToPatch(self.model)

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            raise e
    async def delete_timer(
        self,
        db: AsyncSession,
        uuid: UUID
    ) -> UUID:
        try:
            print(f"\n\n\nuuid to delete: {uuid}\n\n\n")
            statement = update(
                self.model
            ).where(
                self.model.uuid == uuid
            ).values(
                deleted_at = datetime.now()
            ).returning(self.model.uuid)
            result = (await db.execute(statement)).first()
            if not result:
                raise exeptions.FailureToDelete(self.model)

            return UUID(result[0])
        except Exception as e:
            print(f"Failed to delete {self.model.__tablename__}: {e}")
            raise e
        

time_range_event = TimeRangeEventDao(
    model=models.TimeRangeEvent,
    schemaRecord=schemas.TimeRangeEventTable
)