from uuid import UUID
from typing import Any
from fastapi import APIRouter, Depends, Body, status
from app import daos, schemas
from app.api.session import get_session, AsyncSession


router = APIRouter()

@router.get("/{uuid}/",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not fouded"
        }
    }
)
async def get(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session)
) -> Any:
    async with Session as db, db.begin():
        result = await daos.time_range_event.get(db,
            uuid=uuid
        )
        
        return result.to_base_model()

@router.get("/range/",
    responses={
        status.HTTP_200_OK: {
            "model": list[schemas.TimeRangeEventNotDeleted]
        }
    }
)
async def get_by_range(
    body:Any = Body(...),
    Session: AsyncSession = Depends(get_session)
) -> Any:
    async with Session as db, db.begin():
        #TODO
        pass

@router.get("/running/{user_uuid}",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not fouded"
        }
    }
)
async def get_running(
    user_uuid: UUID,
    Session: AsyncSession = Depends(get_session)
) -> Any:
    async with Session as db, db.begin():
        #TODO
        pass

@router.post("/",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_201_CREATED: {
            "description": "Timer created",
            "model": schemas.TimeRangeEventNotDeleted
        },
    }
)
async def post(
    body:Any = Body(...),
    Session: AsyncSession = Depends(get_session)
) -> Any:
    async with Session as db, db.begin():
        #TODO
        pass

@router.patch("/",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not fouded"
        }
    }
)
async def patch(
    body:Any = Body(...),
    Session: AsyncSession = Depends(get_session)
) -> Any:
    async with Session as db, db.begin():
        #TODO
        pass

@router.delete("/{uuid}/",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.TimeRangeEventNotDeleted
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Item not fouded"
        }
    }
)
async def delete(
    uuid: UUID,
    Session: AsyncSession = Depends(get_session)
) -> Any:
    async with Session as db, db.begin():
        #TODO
        pass