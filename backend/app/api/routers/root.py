from fastapi import APIRouter, Depends, Response
from app.db import tables
from app.api.session import get_session, AsyncSession
from sqlalchemy import select

router = APIRouter()

@router.get("/")
async def root(
    response: Response,
    Session: AsyncSession = Depends(get_session)
) -> str:
    try:
        async with Session as db, db.begin():
            statement = select(tables.User)
            result = (await db.execute(statement)).first()
            print(f"Conexão estabelecida com sucesso: {result}")
    except Exception as e:
        print(f'Erro ao conectar: {e}')

    return "Hello, World!"