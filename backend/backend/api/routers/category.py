from fastapi import APIRouter, Depends
from backend.api.session import get_session, AsyncSession

from backend.daos import category
from backend.schemas import CategoryRecord

router = APIRouter()

@router.get("/{user_id}")
async def get_content_list(
    user_id:int,
    Session: AsyncSession = Depends(get_session)
) -> list[CategoryRecord]:
    content_list:list[CategoryRecord] = []
    async with Session as db, db.begin():
        generator = category.get_all(db,
            user_id=user_id
        )
        async for row in generator:
            content_list.append(row)

    return content_list

@router.post("/{user_id}")
async def post_content( 
    user_id:int,
    Session: AsyncSession = Depends(get_session)
) -> CategoryRecord|None:
    async with Session as db, db.begin():
        created = await category.create(db,
            user_id=user_id
        )

    return created

