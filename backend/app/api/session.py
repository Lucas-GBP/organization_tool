from typing import AsyncGenerator
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import (
    AsyncSession as AsyncSession, 
    create_async_engine, 
    async_sessionmaker
)

DATABASE_ASYNC = "postgresql+asyncpg://postgres:changethis@database:5432/app"
DATABASE_URL = "postgresql://postgres:changethis@database:5432/app"
engine = create_async_engine(DATABASE_ASYNC)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    yield async_sessionmaker(autocommit=False, autoflush=False, bind=engine)()