from sqlalchemy.sql import select, insert, delete, update

from backend import schemas
from backend.db import tables
from backend.schemas import UserTable as UserSchema
from backend.db.tables import User as UserModel
from backend.daos.utils import BaseDao
from backend.daos.utils.exeptions import (
    FailuredToPost,
    ItemNotFound
)
from backend.api.session import AsyncSession

class User(BaseDao[tables.User, schemas.UserTable]):
    async def create(
        self,
        db: AsyncSession,
        data: schemas.UserCreate
    ) -> schemas.UserTable:
        statement = insert(self.model).values(
            nickname = data.nickname,
            hashed_password = data.hashed_password
        ).returning(self.model)

        result = (await db.execute(statement)).first()
        if result is None or len(result) <= 0:
            raise FailuredToPost()

        return self.schemaRecord.model_validate(result[0])
    
    async def get_by_nickname(
        self,
        db: AsyncSession,
        nickname: str
    ) -> schemas.UserTable:
        statement = select(self.model).where(
            self.model.nickname == nickname
        )

        result = (await db.execute(statement)).first()
        if result is None or len(result) <= 0:
            raise ItemNotFound()
        
        return self.schemaRecord.model_validate(result[0])

user = User(
    model=tables.User,
    schemaRecord=schemas.UserTable
)