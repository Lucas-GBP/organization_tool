from uuid import UUID
from typing import AsyncGenerator, Any

from app.daos.utils.base import BaseDao
from app.daos.utils.exeptions import (
    FailuredToPost,
    FailureToPatch,
    ItemNotFound
)
from app.db.models import Category as CategoryModel, User as UserModel
from app.schemas import (
    CategoryTable,
    CategoryWithSubCategoryComposed,
    CategoryPost, 
    CategoryPatch,
    CategoryWithSubCategoryPost
)
import app.daos as daos
from sqlalchemy.sql import select, insert, update
from app.api.session import AsyncSession

class Category(BaseDao[CategoryModel, CategoryTable]): 
    async def get_all(
        self,
        db: AsyncSession,
        user_uuid:UUID
    ) -> AsyncGenerator[CategoryTable, None]:
        try:
            statement = select(self.model).where(
                self.model.user_id == select(UserModel.id).where(
                    UserModel.uuid == user_uuid
                ).scalar_subquery()
            )
            result = (await db.execute(statement)).all()

            for category in result:
                yield self.schemaRecord.model_validate(category[0])
        except Exception as e:
            print(f'Failed to get all {self.model.__tablename__}: {e}')
            raise e
    
    async def get_all_with_subcategory(
        self,
        db: AsyncSession,
        user_uuid:UUID
    ) -> AsyncGenerator[CategoryWithSubCategoryComposed, None]:
        try:
            category_generator = self.get_all(db, user_uuid)
            async for item in category_generator:
                completed_item = CategoryWithSubCategoryComposed.model_validate(item)
                completed_item.sub_categories = []
                sub_category_generator = daos.sub_category.get_all(db, completed_item.uuid)
                async for sub_category in sub_category_generator:
                    completed_item.sub_categories.append(sub_category)
                
                yield completed_item
        except Exception as e:
            print(f'Failed to get with subcategory and {self.model.__tablename__}: {e}')
            raise e

    async def get_with_subcategory(
        self,
        db: AsyncSession,
        user_uuid:UUID
    ) -> CategoryWithSubCategoryComposed:
        try:
            category = await self.get(db, user_uuid)
            completed_category = None
            if category is not None:
                completed_category = CategoryWithSubCategoryComposed.model_validate(category)
                completed_category.sub_categories = []
                sub_category_generator = daos.sub_category.get_all(db, completed_category.uuid)
                async for sub_category in sub_category_generator:
                    completed_category.sub_categories.append(sub_category)
            else:
                raise ItemNotFound()
            
            return completed_category
        except Exception as e:
            raise e

    async def post(
        self,
        db: AsyncSession,
        data: CategoryPost
    ) -> CategoryTable:
        try:
            statement = insert(self.model).values(
                color = data.color,
                title = data.title,
                description = data.description,
                user_id = select(UserModel.id).where(
                    UserModel.uuid == data.user_uuid
                ).scalar_subquery()
            ).returning(self.model)

            result = (await db.execute(statement)).first()
            if result is None or len(result) <= 0:
                raise FailuredToPost()

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            print(f'Failed to create {self.model.__tablename__}: {e}')
            raise e

    async def patch(
        self,
        db: AsyncSession,
        data: CategoryPatch
    ) -> CategoryTable:
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
                raise FailureToPatch()

            return self.schemaRecord.model_validate(result[0])
        except Exception as e:
            print(f'Failed to patch {self.model.__tablename__}: {e}')
            raise e

    
category = Category(
    model=CategoryModel,
    schemaRecord=CategoryTable
)