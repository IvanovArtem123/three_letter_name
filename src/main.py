from fastapi import FastAPI

from api import api_router
from core.config import settings

app = FastAPI(title=settings.app_title)

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
