from uuid import UUID
from sqlalchemy.sql import select, insert, delete, update

from ._base import BaseDao
from backend.models import (
    SubCategory as SubCategoryModel, 
    Category as CategoryModel
)
from backend.schemas import SubCategoryRecord, SubCategoryPost, SubCategoryIntegratedPost, SubCategoryPatch
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
        result = None
        statement = select(self.model).where(
            self.model.category_id == select(CategoryModel.id).where(
                CategoryModel.uuid == category_uuid
            ).scalar_subquery()
        )
        try:
            result = (await db.execute(statement)).all()
        except Exception as e:
            print(e)

        for category in result:
            yield self.schemaRecord.model_validate(category[0])
    
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
        valueslist = [{
            "title": item.title,
            "color": item.color,
            "category_id": select(CategoryModel.id).where(CategoryModel.uuid == category_uuid).scalar_subquery()
        } for item in data]
        statement = insert(self.model).values(valueslist).returning(self.model)
        
        try:
            result = (await db.execute(statement)).all()
            for sub_category in result:
                yield self.schemaRecord.model_validate(sub_category[0])
        except Exception as e:
            print(f"error: {e}")

    async def patch(self, db:AsyncSession, data: SubCategoryPatch):
        statement = update(
            self.model
        ).where(
            self.model.uuid == data.uuid
        ).values(
            data
        ).returning(self.model)
        result = (await db.execute(statement)).all()

        return self.schemaRecord.model_validate(result[0]) if result else None

    async def delete(self, db:AsyncSession, uuid:UUID):
        statement = delete(self.model).where(self.model.uuid == uuid)
        result = (await db.execute(statement)).all()

        return result
        


sub_category = SubCategory(
    SubCategoryModel, SubCategoryRecord
)