from ._base import BaseDao
from backend.db import Category as CategoryModel, User as UserModel
from backend.schemas import (
    CategoryRecord, 
    CategoryPost, 
    CategoryPatch, 
    Category as CategorySchema
)
from uuid import UUID
from backend import daos
from typing import AsyncGenerator

from sqlalchemy.sql import select, insert, delete
from backend.api.session import AsyncSession

class Category(BaseDao[CategoryModel, CategoryRecord]):
    async def get(
        self,
        db: AsyncSession,
        uuid: UUID
    ):
        try:
            statement = select(self.model).where(
                self.model.uuid == uuid
            )
            result = (await db.execute(statement)).first()
        except Exception as e:
            print(e)
        
        return self.schemaRecord.model_validate(result[0]) if result else None
    
    async def get_all(
        self,
        db: AsyncSession,
        user_uuid:UUID
    ):
        statement = select(self.model).where(
            self.model.user_id == select(UserModel.id).where(
                UserModel.uuid == user_uuid
            ).scalar_subquery()
        )
        result = (await db.execute(statement)).all()

        for category in result:
            yield self.schemaRecord.model_validate(category[0])
    
    async def get_all_with_subcategory(
        self,
        db: AsyncSession,
        user_uuid:UUID
    ):
        category_generator = self.get_all(db, user_uuid)
        async for item in category_generator:
            category = item.to_base_model()
            category.sub_categories = []
            sub_category_generator = daos.sub_category.get_all(db, item.uuid)
            async for sub_category in sub_category_generator:
                category.sub_categories.append(sub_category.to_base_model())
            
            yield category

    async def post(
        self,
        db: AsyncSession,
        data: CategoryPost
    ):
        statement = insert(self.model).values(
            color = data.color,
            title = data.title,
            description = data.description,
            user_id = select(UserModel.id).where(
                UserModel.uuid == data.user_uuid
            ).scalar_subquery()
        ).returning(self.model)

        try:
            result = (await db.execute(statement)).first()
            return self.schemaRecord.model_validate(result[0]) if result else None
        except Exception as e:
            print(f'Failed to create {self.model.__tablename__}: {e}')
            return None
        
    async def pacth(
        self,
        db: AsyncSession,
        data: CategoryPatch
    ):
        return
        
    async def delete(
        self,
        db: AsyncSession,
        uuid: UUID
    ):
        try:
            statement = delete(self.model).where(
                self.model.uuid == uuid
            )
            result = (await db.execute(statement)).all()
            return None
        except Exception as e:
            print(e)
            return None
    
category = Category(
    model=CategoryModel,
    schemaRecord=CategoryRecord
)