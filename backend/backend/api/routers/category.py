from fastapi import APIRouter, Depends, Body
from uuid import UUID
from backend.api.session import get_session, AsyncSession

from backend.daos import category, sub_category
from backend.schemas import (
    Category, 
    CategoryPost, 
    CategoryPatch, 
    SubCategory,
    SubCategoryPost,
    SubCategoryPatch
)

router = APIRouter()

@router.get("/{uuid}")
async def get_category(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session)
):
    async with Session as db, db.begin():
        result = await category.get(db,
            uuid=uuid
        )

    return result.to_base_model() if result else None

@router.post("/")
async def post_content(
    Session: AsyncSession = Depends(get_session),
    data:CategoryPost = Body(...)
):
    async with Session as db, db.begin():
        posted = await category.post(db, data)
        new_category = posted.to_base_model()

        if posted and data.sub_categories:
            sub_categories:list[SubCategory] = []
            
            generator = sub_category.post_list(db, data.sub_categories, posted.uuid)
            async for item in generator:
                sub_categories.append(item)

            new_category.sub_categories = sub_categories

    return new_category if new_category else None

@router.patch("/")
async def path_content(
    Session: AsyncSession = Depends(get_session),
    data:CategoryPatch = Body(...)
):
    async with Session as db, db.begin():
        patched = await category.patch(db, data)
    return patched

@router.delete("/{uuid}")
async def delete_content(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session),
):
    async with Session as db, db.begin():
        deleted = await category.delete(db, uuid)
    
    return deleted

@router.get("/all/{user_uuid}")
async def get_all_content(
    user_uuid:UUID,
    Session: AsyncSession = Depends(get_session)
):
    content_list:list[Category] = []
    async with Session as db, db.begin():
        generator = category.get_all_with_subcategory(db,
            user_uuid
        )
        async for item in generator:
            content_list.append(item)
        return content_list

@router.get("/subcategory/{uuid}")
async def get_sub_category(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session)
):
    async with Session as db, db.begin():
        result = await sub_category.get(db,
            uuid=uuid
        )

    return result.to_base_model() if result else None

@router.post("/subcategory")
async def post_sub_category(
    Session: AsyncSession = Depends(get_session),
    data:SubCategoryPost = Body(...)
):
    async with Session as db, db.begin():
        posted = await sub_category.post(db, data)

    return posted.to_base_model() if posted else None

@router.patch("/subcategory")
async def patch_sub_category(
    Session: AsyncSession = Depends(get_session),
    data: SubCategoryPatch = Body(...)
):
    async with Session as db, db.begin():
        patched = await sub_category.patch(db, data)
    return patched

@router.delete("/subcategory/{uuid}")
async def delete_sub_category(
    uuid: UUID,
    Session: AsyncSession = Depends(get_session)
):
    async with Session as db, db.begin():
        deleted = await sub_category.delete(db, uuid)

        return deleted