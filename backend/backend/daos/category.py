from ._base import BaseDao
from backend.db.models import Category as CategoryModel, User as UserModel
from backend.schemas import (
    CategoryTable,
    CategoryWithSubCategoryComposed,
    CategoryPost, 
    CategoryPatch, 
)
from uuid import UUID
import backend.daos as daos
from sqlalchemy.sql import select, insert, update
from backend.api.session import AsyncSession

class Category(BaseDao[CategoryModel, CategoryTable]): 
    async def get_all(
        self,
        db: AsyncSession,
        user_uuid:UUID
    ):
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
    ):
        try:
            category_generator = self.get_all(db, user_uuid)
            async for item in category_generator:
                item.sub_categories = []
                sub_category_generator = daos.sub_category.get_all(db, item.uuid)
                async for sub_category in sub_category_generator:
                    item.sub_categories.append(sub_category)
                
                yield CategoryWithSubCategoryComposed.model_validate(item)
        except Exception as e:
            print(f'Failed to get with subcategory and {self.model.__tablename__}: {e}')
            raise e

    async def get_with_subcategory(
        self,
        db: AsyncSession,
        user_uuid:UUID
    ):
        try:
            category = await self.get(db, user_uuid)
            if category is not None:
                category.sub_categories = []
                sub_category_generator = daos.sub_category.get_all(db, category.uuid)
                async for sub_category in sub_category_generator:
                    category.sub_categories.append(sub_category)
            
            return CategoryWithSubCategoryComposed.model_validate(category)
        except Exception as e:
            raise e

    async def post(
        self,
        db: AsyncSession,
        data: CategoryPost
    ):
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
            return self.schemaRecord.model_validate(result[0]) if result else None
        except Exception as e:
            print(f'Failed to create {self.model.__tablename__}: {e}')
            raise e
        
    async def patch(
        self,
        db: AsyncSession,
        data: CategoryPatch
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
            print(f'Failed to patch {self.model.__tablename__}: {e}')
            raise e

    
category = Category(
    model=CategoryModel,
    schemaRecord=CategoryTable
)