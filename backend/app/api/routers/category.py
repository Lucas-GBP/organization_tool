from uuid import UUID
from fastapi import APIRouter, Depends, Body
from app import daos
from app.schemas import (
    Category,
    CategoryWithSubCategory,
    CategoryPost,
    CategoryWithSubCategoryPost,
    CategoryPatch,
    SubCategory,
    SubCategoryPost,
    SubCategoryPatch,
    CategoryWithSubCategoryComposed
)
from app.api.session import get_session, AsyncSession

router = APIRouter()

@router.get("/{uuid}")
async def get_category(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session)
) -> Category:
    async with Session as db, db.begin():
        result = await daos.category.get(db,
            uuid=uuid
        )
        
        return result.to_base_model()

@router.post("/")
async def post_content(
    Session: AsyncSession = Depends(get_session),
    data:CategoryPost = Body(...)
) -> Category:
    async with Session as db, db.begin():
        new_category = await daos.category.post(db, data)

    return new_category.to_base_model()

@router.patch("/")
async def path_content(
    Session: AsyncSession = Depends(get_session),
    data:CategoryPatch = Body(...)
) -> Category:
    async with Session as db, db.begin():
        patched = await daos.category.patch(db, data)
    return patched.to_base_model()

@router.delete("/{uuid}")
async def delete_content(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session),
) -> None:
    async with Session as db, db.begin():
        await daos.category.delete(db, uuid)

        return

@router.get("/all/{user_uuid}")
async def get_all_content(
    user_uuid:UUID,
    Session: AsyncSession = Depends(get_session)
) -> list[Category]:
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
) -> SubCategory:
    async with Session as db, db.begin():
        result = await daos.sub_category.get(db,
            uuid=uuid
        )

    return result.to_base_model()

@router.post("/subcategory")
async def post_sub_category(
    Session: AsyncSession = Depends(get_session),
    data:SubCategoryPost = Body(...)
) -> SubCategory:
    async with Session as db, db.begin():
        posted = await daos.sub_category.post(db, data)

    return posted.to_base_model()

@router.patch("/subcategory")
async def patch_sub_category(
    Session: AsyncSession = Depends(get_session),
    data: SubCategoryPatch = Body(...)
) -> SubCategory:
    async with Session as db, db.begin():
        patched = await daos.sub_category.patch(db, data)
    return patched.to_base_model()

@router.delete("/subcategory/{uuid}")
async def delete_sub_category(
    uuid: UUID,
    Session: AsyncSession = Depends(get_session)
) -> None:
    async with Session as db, db.begin():
        await daos.sub_category.delete(db, uuid)

    return
    
@router.get("/complety/{uuid}")
async def get_complety(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session),
) -> CategoryWithSubCategoryComposed:
    async with Session as db, db.begin():
        completed_category = await daos.category.get_with_subcategory(db, uuid)
    return completed_category

@router.post("/complety")
async def post_complety(
    Session: AsyncSession = Depends(get_session),
    data:CategoryWithSubCategoryPost = Body(...)
) -> CategoryWithSubCategory:
    async with Session as db, db.begin():
        sub_categories:list[SubCategory]|None = None
        new_category = await daos.category.post(db, data)
        if data.sub_categories is not None:
            sub_categories = []
            for sub in data.sub_categories:
                new_sub_category = await daos.sub_category.post(db, SubCategoryPost(
                    category_uuid=new_category.uuid,
                    color=sub.color,
                    title=sub.title
                ))
                sub_categories.append(new_sub_category.to_base_model())

        return CategoryWithSubCategory(
            title=new_category.title,
            uuid=new_category.uuid,
            description=new_category.description,
            color=new_category.color,
            sub_categories=sub_categories
        )

@router.get("/complety/all/{uuid}")
async def get_complety_all(
    uuid:UUID,
    Session: AsyncSession = Depends(get_session),
) -> list[CategoryWithSubCategory]:
    async with Session as db, db.begin():
        categories:list[CategoryWithSubCategory] = []
        category_generator = daos.category.get_all_with_subcategory(db, uuid)
        async for category in category_generator:
            categories.append(category.to_base_model())
        return categories