from typing import Any
from fastapi import APIRouter, Depends, status, HTTPException, Response
from app import schemas, daos
from app.core import hash_password
from app.api.session import get_session, AsyncSession
from app.daos.utils import exeptions as dao_exeptions

router = APIRouter()

@router.get("/test",
    responses={
        status.HTTP_200_OK: {
            "model": schemas.User
        },
        status.HTTP_201_CREATED: {
            "description": "Usuário criado.",
            "model": schemas.User
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description":"Algum erro aconteceu."
        },
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Não foi possivel criar o usuário.",

        }
    }
)
async def get_login_test(
    response: Response,
    Session: AsyncSession = Depends(get_session)
) -> schemas.User:
    NICKNAME = "Lucas"
    PASSWORD = "#5TPd42ç"
    async with Session as db, db.begin():
        try:
            user = await daos.user.get_by_nickname(db, NICKNAME)

            response.status_code = status.HTTP_200_OK
            return user.to_base_model()
        except dao_exeptions.ItemNotFound:
            try:
                hash = hash_password(PASSWORD)
                new_user = await daos.user.create(db,
                    schemas.UserCreate(
                        nickname=NICKNAME,
                        hashed_password=hash
                    )
                )
                
                response.status_code = status.HTTP_201_CREATED
                return new_user.to_base_model()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                    detail="Serviço indisponível. Tente novamente mais tarde."
                )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )