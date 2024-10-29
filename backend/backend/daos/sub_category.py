from uuid import UUID
from sqlalchemy.sql import select, insert, delete, update

from ._base import BaseDao
from backend.db.models import (
    SubCategory as SubCategoryModel, 
    Category as CategoryModel
)
from backend.schemas import SubCategoryTable, SubCategoryPost, SubCategoryIntegratedPost, SubCategoryPatch
from backend.api.session import AsyncSession

class SubCategory(BaseDao[SubCategoryModel, SubCategoryTable]):    
    async def get_all(
        self,
        db: AsyncSession,
        category_uuid: UUID
    ):
        """
        get all subcategory itens from a category
        """
        try:
            statement = select(self.model).where(
                self.model.category_id == select(CategoryModel.id).where(
                    CategoryModel.uuid == category_uuid
                ).scalar_subquery()
            )
            result = (await db.execute(statement)).all()

            for category in result:
                yield self.schemaRecord.model_validate(category[0])
        except Exception as e:
            print(f"Exception: {e}")
            raise e
    
    async def post(
        self,
        db: AsyncSession,
        data: SubCategoryPost
    ):
        """
        Post a single subgategory
        """
        try:
            statement = insert(self.model).values(
                self.model.category_id == select(CategoryModel.id).where(
                    CategoryModel.uuid == data.category_uuid
                ).scalar_subquery(),
                title = data.title,
                color = data.color
            )
            result = (await db.execute(statement)).first()
            return self.schemaRecord.model_validate(result[0]) if result else None
        except Exception as e:
            print(f"Exception: {e}")
            raise e
    
    async def post_list(
        self,
        db:AsyncSession,
        data:list[SubCategoryIntegratedPost],
        category_uuid:UUID
    ):
        """
        post a list of sub_category in a single category
        """
        try:
            valueslist = [{
                "title": item.title,
                "color": item.color,
                "category_id": select(CategoryModel.id).where(CategoryModel.uuid == category_uuid).scalar_subquery()
            } for item in data]
            statement = insert(self.model).values(valueslist).returning(self.model)

            result = (await db.execute(statement)).all()
            for sub_category in result:
                yield self.schemaRecord.model_validate(sub_category[0])
        except Exception as e:
            print(f"Exception: {e}")
            raise e

    async def patch(
        self, 
        db:AsyncSession, 
        data: SubCategoryPatch
    ):
        try:
            statement = update(
                self.model
            ).where(
                self.model.uuid == data.uuid
            ).values(
                data
            ).returning(self.model)
            result = (await db.execute(statement)).all()

            return self.schemaRecord.model_validate(result[0]) if result else None
        except Exception as e:
            print(f"Exception: {e}")
            raise e


sub_category = SubCategory(
    SubCategoryModel, SubCategoryTable
)