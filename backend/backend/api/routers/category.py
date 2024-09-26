from uuid import UUID
from fastapi import APIRouter, Depends, Body
from backend import daos
from backend.schemas import (
    Category,
    CategoryWithSubCategory,
    CategoryPost,
    CategoryWithSubCategoryPost,
    CategoryPatch,
    SubCategoryPost,
    SubCategoryPatch,
)
from backend.api.session import get_session, AsyncSession

router = APIRouter()

@router.get("/{uuid}")
async def get_category(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session)
):
    async with Session as db, db.begin():
        result = await daos.category.get(db,
            uuid=uuid
        )

    return result.to_base_model() if result else None

@router.post("/")
async def post_content(
    Session: AsyncSession = Depends(get_session),
    data:CategoryPost = Body(...)
):
    async with Session as db, db.begin():
        new_category = await daos.category.post(db, data)

    return new_category.to_base_model() if new_category else None

@router.patch("/")
async def path_content(
    Session: AsyncSession = Depends(get_session),
    data:CategoryPatch = Body(...)
):
    async with Session as db, db.begin():
        patched = await daos.category.patch(db, data)
    return patched.to_base_model() if patched else None

@router.delete("/{uuid}")
async def delete_content(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session),
):
    async with Session as db, db.begin():
        deleted = await daos.category.delete(db, uuid)
    
    return deleted

@router.get("/all/{user_uuid}")
async def get_all_content(
    user_uuid:UUID,
    Session: AsyncSession = Depends(get_session)
):
    content_list:list[Category] = []
    async with Session as db, db.begin():
        generator = daos.category.get_all(db,
            user_uuid
        )
        async for item in generator:
            content_list.append(item.to_base_model())
        return content_list

@router.get("/subcategory/{uuid}")
async def get_sub_category(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session)
):
    async with Session as db, db.begin():
        result = await daos.sub_category.get(db,
            uuid=uuid
        )

    return result.to_base_model() if result else None

@router.post("/subcategory")
async def post_sub_category(
    Session: AsyncSession = Depends(get_session),
    data:SubCategoryPost = Body(...)
):
    async with Session as db, db.begin():
        posted = await daos.sub_category.post(db, data)

    return posted.to_base_model() if posted else None

@router.patch("/subcategory")
async def patch_sub_category(
    Session: AsyncSession = Depends(get_session),
    data: SubCategoryPatch = Body(...)
):
    async with Session as db, db.begin():
        patched = await daos.sub_category.patch(db, data)
    return patched

@router.delete("/subcategory/{uuid}")
async def delete_sub_category(
    uuid: UUID,
    Session: AsyncSession = Depends(get_session)
):
    async with Session as db, db.begin():
        deleted = await daos.sub_category.delete(db, uuid)

        return deleted
    
@router.get("/complety/{uuid}")
async def get_complety(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session),
):
    async with Session as db, db.begin():
        completed_category = await daos.category.get_with_subcategory(db, uuid)
    return completed_category

@router.post("/complety")
async def post_complety(
    Session: AsyncSession = Depends(get_session),
    data:CategoryWithSubCategoryPost = Body(...)
):
    async with Session as db, db.begin():
        return None

@router.get("/complety/all/{uuid}")
async def get_complety_all(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session),
):
    async with Session as db, db.begin():
        categories:list[CategoryWithSubCategory] = []
        category_generator = daos.category.get_all_with_subcategory(db, uuid)
        async for category in category_generator:
            categories.append(category.to_base_model())
        return categories