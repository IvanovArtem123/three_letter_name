from fastapi import APIRouter


from .endpoints import panel as panel_router


api_router = APIRouter()

api_router.include_router(panel_router.router)
