from uuid import UUID
from typing import Any
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
            result = await daos.time_range_event.get(db,
                uuid=uuid
            )
            
            return result.to_base_model()
        except exeptions.ItemNotFound:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time event not founded."
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@router.get("/range/",
    responses={
        status.HTTP_200_OK: {
            "model": list[schemas.TimeRangeEventNotDeleted]
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
        }
    }
)
async def get_by_range(
    body:schemas.TimeRangeEventGetByRange = Body(...),
    Session: AsyncSession = Depends(get_session)
) -> list[schemas.TimeRangeEventNotDeleted]:
    async with Session as db, db.begin():
        try:
            range_list:list[schemas.TimeRangeEventNotDeleted] = []
            generator = daos.time_range_event.get_by_time_range(db,
                user_uuid=body.user_uuid,
                start=body.start,
                end=body.end
            )

            async for item in generator:
                range_list.append(item.to_base_model())
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
) -> schemas.TimeRangeEventNotDeleted:
    async with Session as db, db.begin():
        running_timer = await daos.time_range_event.get_running_timer(db, user_uuid=user_uuid)
        
        if running_timer is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No timers are running now"
            )
        return running_timer.to_base_model()

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
    async with Session as db, db.begin():
        try:
            posted = await daos.time_range_event.post(db,
                data=schemas.TimeRangeEventCreate(
                    category_id=body.category_id,
                    description=body.description,
                    end_time=body.end_time,
                    start_time=body.start_time,
                    sub_category_id=body.sub_category_id,
                    title=body.title,
                    user_uuid=body.user_uuid
                ),
            )

            response.status_code = status.HTTP_201_CREATED
            return posted.to_base_model()
        except Exception:
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
    body:schemas.TimeRangeEventPatch = Body(...),
    Session: AsyncSession = Depends(get_session)
) -> schemas.TimeRangeEventNotDeleted:
    async with Session as db, db.begin():
        try:
            patched = await daos.time_range_event.patch(db=db,
                data=schemas.TimeRangeEventUpdate(
                    uuid=body.uuid,
                    category_id=body.category_id,
                    description=body.description,
                    end_time=body.end_time,
                    start_time=body.start_time,
                    sub_category_id=body.sub_category_id,
                    title=body.title
                )
            )

            return patched.to_base_model()
        except Exception:
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
) -> schemas.TimeRangeEventNotDeleted:
    async with Session as db, db.begin():
        try:
            deleted = await daos.time_range_event.delete(db, uuid)
            return deleted.to_base_model()
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )