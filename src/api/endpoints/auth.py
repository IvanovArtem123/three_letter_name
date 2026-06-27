import re
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from transliterate import translit
from core.db import get_async_session
from core.oauth import oauth
from models.user import User, UserRole
import uuid as uuid_lib

router = APIRouter(prefix='/auth', tags=['Аутентификация'])


@router.get("/google/login", summary="Вход через Google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/google/callback", summary="Callback от Google")
async def google_callback(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_async_session)],
):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        raise HTTPException(
            status_code=400,
            detail={"code": 400,
                    "message": "Не удалось получить данные от Google"}
        )

    stmt = select(User).where(User.google_id == user_info["sub"]).limit(1)
    user = await session.scalar(stmt)

    if not user:
        user = User(
            google_id=user_info["sub"],
            email=user_info["email"],
            username=_generate_username(user_info),
            role=int(UserRole.USER),
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)

    request.session["user_id"] = str(user.id)
    request.session["user_role"] = str(user.role)

    return RedirectResponse("/")


@router.get("/logout", summary="Выход")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/")


def _generate_username(user_info: dict) -> str:
    '''Генерирует уникальное имя пользователя на основе данных из Google.'''
    base = user_info.get("name", "").replace(" ", "_").lower()
    base = translit(base, "ru", reversed=True)
    base = re.sub(r'[^a-z0-9_]', '', base)
    base = base[:15] or "user"
    return f"{base}_{str(uuid_lib.uuid4())[:6]}"
