from fastapi import APIRouter

from .root import router as root_router
from .category import router as category_router
from .login import router as login_router

api_router = APIRouter()

api_router.include_router(root_router)
api_router.include_router(category_router, prefix="/category", tags=["Categories"])
api_router.include_router(login_router, prefix="/login", tags=["Login"])