from typing import AsyncGenerator
from sqlalchemy.engine import URL, create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

database_async = "postgresql+asyncpg://postgres:changethis@database:5432/app"
database_url = "postgresql://postgres:changethis@database:5432/app"
engine = create_async_engine(database_async)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    yield async_sessionmaker(autocommit=False, autoflush=False, bind=engine)()