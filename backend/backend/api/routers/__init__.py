from fastapi import APIRouter

from .root import router as root_router

api_router = APIRouter()

api_router.include_router(root_router)