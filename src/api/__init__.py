from fastapi import APIRouter


from .endpoints import panel as panel_router
from .endpoints import user as user_router
from .endpoints import auth as auth_router


api_router = APIRouter()

api_router.include_router(panel_router.router)
api_router.include_router(user_router.router)
api_router.include_router(auth_router.router)
