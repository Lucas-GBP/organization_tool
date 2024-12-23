from datetime import datetime
from uuid import UUID
from typing import AsyncGenerator
from sqlalchemy.sql import select, insert, update

from .utils.base import BaseDao
from app.db import models
from app import schemas
from app.api.session import AsyncSession
from app.daos.utils import exeptions

class TimeRangeEventDao(BaseDao[models.TimeRangeEvent, schemas.TimeRangeEventTable]):
    async def get_not_deleted(
        self,
        db: AsyncSession,
        uuid: UUID,
        user_uuid: UUID
    ) -> schemas.TimeRangeEventNotDeletedView:
        try:
            statement = select(models.TimeRangeEventNotDeleted).where(
                self.model.uuid == uuid,
                self.model.user_id == select(models.User.id).where(
                    models.User.uuid == user_uuid
                ).scalar_subquery()
            )
            result = (await db.execute(statement)).all()

            return schemas.TimeRangeEventNotDeletedView.model_validate(result[0])
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
    ) -> AsyncGenerator[schemas.TimeRangeEventNotDeletedView, None]:
        try:
            if end is not None:
                statement = select(models.TimeRangeEventNotDeleted).where(
                    models.TimeRangeEventNotDeleted.user_id == select(models.User.id).where(
                        models.User.uuid == user_uuid,
                    ).scalar_subquery(),
                    models.TimeRangeEventNotDeleted.start_time >= start,
                    models.TimeRangeEventNotDeleted.end_time <= end
                ).limit(limit)
            else:
                statement = select(models.TimeRangeEventNotDeleted).where(
                    models.TimeRangeEventNotDeleted.user_id == select(models.User.id).where(
                        models.User.uuid == user_uuid,
                    ).scalar_subquery(),
                    models.TimeRangeEventNotDeleted.start_time >= start,
                ).limit(limit)
            result = (await db.execute(statement)).all()

            for event in result:
                yield schemas.TimeRangeEventNotDeletedView.model_validate(event[0])
        except Exception as e:
            print(f'Failed to get all {self.model.__tablename__}: {e}')
            raise e
    async def get_running_timer(
        self,
        db: AsyncSession,
        user_uuid: UUID
    ) -> schemas.TimeRangeEventNotDeletedView|None:
        try:
            statement = select(models.TimeRangeEventNotDeleted).where(
                models.TimeRangeEventNotDeleted.user_id == select(models.User.id).where(
                    models.User.uuid == user_uuid,
                ).scalar_subquery(),
                models.TimeRangeEventNotDeleted.end_time == None
            )
            result = (await db.execute(statement)).first()

            if result is None or len(result) <= 0:
                return None
            return schemas.TimeRangeEventNotDeletedView.model_validate(result[0])
        except Exception as e:
            print(f'Failed to get {self.model.__tablename__}: {e}')
            raise e
    async def post(
        self,
        db: AsyncSession,
        data: schemas.TimeRangeEventPost
    ) -> schemas.TimeRangeEventTable:
        try:
            statement = insert(models.TimeRangeEvent).values(
                user_id = select(models.User.id).where(
                    models.User.uuid == data.user_uuid
                ).scalar_subquery(),
                category_id = data.category_id,
                sub_category_id = data.sub_category_id,
                title = data.title,
                description = data.description,
                start_time = data.start_time,
                end_time = data.end_time
            ).returning(models.TimeRangeEvent)

            result = (await db.execute(statement)).one()

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            running_timer = await self.get_running_timer(db=db, user_uuid=data.user_uuid)
            if running_timer is None:
                raise exeptions.TimerAlreadyRunning()
            print(f'Failed to create {self.model.__tablename__}: {e}')
            raise e
    async def patch(
        self,
        db: AsyncSession,
        data: schemas.TimeRangeEventPatch
    ) -> schemas.TimeRangeEventTable:
        try:
            statement = update(
                self.model
            ).where(
                self.model.uuid == data.uuid
            ).values(
                data.model_dump(exclude_unset=True)
            ).returning(self.model)

            result = (await db.execute(statement)).one()
            if result is None or len(result) <= 0:
                raise exeptions.FailureToPatch(self.model)

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            raise e

time_range_event = TimeRangeEventDao(
    model=models.TimeRangeEvent,
    schemaRecord=schemas.TimeRangeEventTable
)