from ._base import BaseDao
from backend.models import Category as CategoryModel
from backend.schemas import CategoryRecord

from sqlalchemy.sql import select, insert, delete
from backend.api.session import AsyncSession

class Category(BaseDao[CategoryModel, CategoryRecord]):
    async def get(
        self,
        db: AsyncSession,
        id:int
    ):
        try:
            statement = select(self.model).where(
                self.model.id == id
            )
            result = (await db.execute(statement)).first()
        except Exception as e:
            print(e)
        
        return self.schemaRecord.model_validate(result)
    
    async def get_all(
        self,
        db: AsyncSession,
        user_id:int
    ):
        statement = select(self.model).where(
            self.model.user_id == user_id
        )
        result = (await db.execute(statement)).all()
        
        for category in result:
            yield self.schemaRecord.model_validate(category[0])

    async def create(
        self,
        db: AsyncSession,
        user_id: int
    ):
        try:
            statement = insert(self.model).values(
                user_id = user_id
            ).returning(self.model)
            result = (await db.execute(statement)).first()
        except Exception as e:
            print(f'Failed to create {self.model.__tablename__}: {e}')

        if result:
            return self.schemaRecord.model_validate(result[0])
        else:
            return None
        
    async def delete(
        self,
        db: AsyncSession,
        id: int
    ):
        result = None
        try:
            statement = delete(self.model).where(
                self.model.id == id
            )
            result = (await db.execute(statement)).all()
        except Exception as e:
            print(e)
        
        return result
    
category = Category(
    model=CategoryModel,
    schemaRecord=CategoryRecord
)