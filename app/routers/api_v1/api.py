from fastapi import APIRouter

from app.routers.api_v1.endpoints import login, shorturl, users, utils

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(shorturl.router, prefix="/urls", tags=["shorturls"])
