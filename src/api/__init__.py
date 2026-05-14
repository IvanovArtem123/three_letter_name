from fastapi import APIRouter


from .endpoints.panel import router as panel_router
from .endpoints.user import router as user_router
from .endpoints.auth import router as auth_router
from .endpoints.subscription import router as subscription_router


api_router = APIRouter(prefix='/api')

api_router.include_router(panel_router)
api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(subscription_router)
