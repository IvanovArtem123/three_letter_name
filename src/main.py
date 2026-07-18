from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from api import api_router
from core.config import settings


app = FastAPI(title=settings.app_title)


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET,
    max_age=60 * 60 * 24 * 7,
    https_only=False,
    same_site='lax',
)


app.include_router(api_router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
