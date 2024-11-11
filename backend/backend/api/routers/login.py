from fastapi import APIRouter, Depends, Body, HTTPException
from backend import schemas, daos
from backend.db import models
from backend.core import hash_password
from backend.api.session import get_session, AsyncSession
from backend.daos.utils import exeptions as dao_exeptions

router = APIRouter()

@router.get("/test")
async def get_login_test(
    Session: AsyncSession = Depends(get_session),
) -> schemas.User:
    NICKNAME:str = "Lucas"
    PASSWORD:str = "#5TPd42ç"
    async with Session as db, db.begin():
        try:
            user = await daos.user.get_by_nickname(db, NICKNAME)
            print(f"user: {user}")
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
                return new_user.to_base_model()
            except Exception as inst:
                print(inst)
                raise HTTPException(
                    status_code=503, detail="Serviço indisponível. Tente novamente mais tarde."
                )
        except:
            raise HTTPException(
                status_code=500
            )