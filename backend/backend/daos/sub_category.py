from uuid import UUID
from sqlalchemy.sql import select, insert, delete

from ._base import BaseDao
from backend.db.models import SubCategory as SubCategoryModel, Category as CategoryModel
from backend.schemas import SubCategoryRecord, SubCategoryPost, SubCategoryIntegratedPost
from backend.api.session import AsyncSession

class SubCategory(BaseDao[SubCategoryModel, SubCategoryRecord]):
    async def get(
        self,
        db: AsyncSession,
        uuid: UUID
    ):
        result = None
        statement = select(self.model).where(
            self.model.uuid == uuid
        )
        try:
            result = (await db.execute(statement)).first()
        except Exception as e:
            print(e)
        
        return self.schemaRecord.model_validate(result[0]) if result else None
    
    async def get_all(
        self,
        db: AsyncSession,
        category_uuid: UUID
    ):
        try:
            result = None
            statement = select(self.model).where(
                self.model.category_id == select(CategoryModel.id).where(
                    CategoryModel.uuid == category_uuid
                ).scalar_subquery()
            )
            result = (await db.execute(statement)).all()
            for category in result:
                yield self.schemaRecord.model_validate(category[0])
        except Exception as e:
            print(e)
    
    async def post(
        self,
        db: AsyncSession,
        data: SubCategoryPost
    ):
        result = None
        
        statement = insert(self.model).values(
            self.model.category_id == select(CategoryModel.id).where(
                CategoryModel.uuid == data.category_uuid
            ).scalar_subquery(),
            title = data.title,
            color = data.color
        )
        try:
            result = (await db.execute(statement)).first()
        except Exception as e:
            print(e)
        
        return self.schemaRecord.model_validate(result[0]) if result else None
    
    async def post_list(
        self,
        db:AsyncSession,
        data:list[SubCategoryIntegratedPost],
        category_uuid:UUID
    ):
        category_id_result = await db.execute(
            select(CategoryModel.id).where(CategoryModel.uuid == category_uuid)
        )
        category_id = category_id_result.scalar_one_or_none()
        if category_id is None:
            raise ValueError(f"No category found with UUID: {category_uuid}")

        valueslist = [{
            "title": item.title,
            "color": item.color,
            "category_id": category_id,
        } for item in data]
        statement = insert(self.model).values(valueslist).returning(self.model)

        try:
            result = (await db.execute(statement)).all()
            for sub_category in result:
                yield self.schemaRecord.model_validate(sub_category[0])
        except Exception as e:
            print(f"error: {e}")


sub_category = SubCategory(
    SubCategoryModel, SubCategoryRecord
)