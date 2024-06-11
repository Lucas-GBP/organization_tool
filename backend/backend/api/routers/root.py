from fastapi import APIRouter, Depends
from backend.api.session import get_session, AsyncSession
from sqlalchemy import text

router = APIRouter()

@router.get("/")
async def root(
    Session: AsyncSession = Depends(get_session)
) -> str:
    try:
        async with Session as db, db.begin():
            test = (await db.execute(text("select * from  \"user\";"))).first()
            print(f"Conexão estabelecida com sucesso: {test}")
    except Exception as e:
        print(f'Erro ao conectar: {e}')

    return "Hello World"