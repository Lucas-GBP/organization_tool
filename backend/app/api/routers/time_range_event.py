from uuid import UUID
from datetime import datetime
from typing import Optional, Any
from fastapi import APIRouter, Depends, Body, status, HTTPException, Response
from app import daos, schemas
from app.daos.utils import exeptions
from app.api.session import get_session, AsyncSession


router = APIRouter()

@router.get("/{uuid}/",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Time event not founded."
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
        }
    }
)
async def get(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session)
) -> schemas.TimeRangeEventNotDeleted:
    async with Session as db, db.begin():
        try: 
            print(f"\n\n\nuuid:\t{uuid}")
            result = await daos.time_range_event.get_not_deleted(db,
                uuid=uuid
            )
            
            return result
        except exeptions.ItemNotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time event not founded."
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@router.get("/range",
    responses={
        status.HTTP_200_OK: {
            "model": list[schemas.TimeRangeEventNotDeleted]
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
        }
    }
)
async def get_by_range(
    user_uuid:UUID,
    start: datetime,
    end: Optional[datetime] = None,
    Session: AsyncSession = Depends(get_session)
) -> list[schemas.TimeRangeEventNotDeleted]:
    async with Session as db, db.begin():
        try:
            range_list:list[schemas.TimeRangeEventNotDeleted] = []
            generator = daos.time_range_event.get_by_time_range(db,
                user_uuid=user_uuid,
                start=start,
                end=end
            )

            async for item in generator:
                range_list.append(item)
            return range_list
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@router.get("/running/{user_uuid}",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No timers are running now"
        }
    }
)
async def get_running(
    user_uuid: UUID,
    Session: AsyncSession = Depends(get_session)
) -> schemas.TimeRangeEventNotDeleted|None:
    async with Session as db, db.begin():
        running_timer = await daos.time_range_event.get_running_timer(db, user_uuid=user_uuid)
        
        return running_timer

@router.post("/",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Timer created",
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
        }
    }
)
async def post(
    response: Response,
    body:schemas.TimeRangeEventPost = Body(...),
    Session: AsyncSession = Depends(get_session)
) -> schemas.TimeRangeEventNotDeleted:
    print(f"\n\n\nbody post: \n{body}")
    async with Session as db, db.begin():
        try:
            posted = await daos.time_range_event.post(db,
                data=schemas.TimeRangeEventCreate(
                    description=body.description,
                    end_time=body.end_time,
                    start_time=body.start_time,
                    category_uuid=body.category_uuid,
                    sub_category_uuid=body.sub_category_uuid,
                    title=body.title,
                    user_uuid=body.user_uuid
                ),
            )

            response.status_code = status.HTTP_201_CREATED
            return await daos.time_range_event.get_not_deleted(db, posted.uuid)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@router.patch("/",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not fouded"
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
        }
    }
)
async def patch(
    body: schemas.TimeRangeEventPatch = Body(...),
    Session: AsyncSession = Depends(get_session)
) -> schemas.TimeRangeEventNotDeleted:
    async with Session as db, db.begin():
        try:
            patched = await daos.time_range_event.patch(db=db,
                data=schemas.TimeRangeEventUpdate(
                    uuid=body.uuid,
                    category_uuid=body.category_uuid,
                    sub_category_uuid=body.sub_category_uuid,
                    description=body.description,
                    end_time=body.end_time,
                    start_time=body.start_time,
                    title=body.title
                )
            )

            return await daos.time_range_event.get_not_deleted(db, patched.uuid)
        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@router.delete("/{uuid}/",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        }
    }
)
async def delete(
    uuid: UUID,
    Session: AsyncSession = Depends(get_session)
) -> UUID:
    async with Session as db, db.begin():
        try:
            deleted = await daos.time_range_event.delete_timer(db, uuid)
            return deleted
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )