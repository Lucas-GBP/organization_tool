from uuid import UUID
from typing import AsyncGenerator
from sqlalchemy.sql import select, insert, update

from .utils.base import BaseDao
from app.daos.utils.exeptions import (
    FailuredToPost,
    FailureToPatch
)
from app.db.models import (
    SubCategory as SubCategoryModel, 
    Category as CategoryModel
)
from app.schemas import SubCategoryTable, SubCategoryPost, SubCategoryIntegratedPost, SubCategoryPatch
from app.api.session import AsyncSession

class SubCategory(BaseDao[SubCategoryModel, SubCategoryTable]):    
    async def get_all(
        self,
        db: AsyncSession,
        category_uuid: UUID
    ) -> AsyncGenerator[SubCategoryTable, None]:
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
    ) -> SubCategoryTable:
        """
        Post a single subgategory
        """
        try:
            # Seleciona o `id` da categoria com o `uuid` correspondente
            category_id_subquery = select(CategoryModel.id).where(
                CategoryModel.uuid == data.category_uuid
            ).scalar_subquery()
            # Usa a subquery como o valor de `category_id`
            statement = insert(self.model).values(
                category_id=category_id_subquery,
                title=data.title,
                color=data.color
            ).returning(self.model)

            result = (await db.execute(statement)).first()
            if result is None or len(result) <= 0:
                raise FailuredToPost

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            print(f"Exception: {e}")
            raise e
    
    async def post_list(
        self,
        db:AsyncSession,
        data:list[SubCategoryIntegratedPost],
        category_uuid:UUID
    ) -> AsyncGenerator[SubCategoryTable, None]:
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
    ) -> SubCategoryTable:
        try:
            statement = update(
                self.model
            ).where(
                self.model.uuid == data.uuid
            ).values(
                data.model_dump(exclude_unset=True)
            ).returning(self.model)

            result = (await db.execute(statement)).one()
            if result is None or len(result) <= 0:
                raise FailureToPatch

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            print(f"Exception: {e}")
            raise e


sub_category = SubCategory(
    SubCategoryModel, SubCategoryTable
)