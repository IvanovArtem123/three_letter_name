from typing import Annotated

from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_async_session
from core.security import create_access_token, verify_password
from schemas.auth import AuthData, AuthToken
from models.user import User


router = APIRouter(prefix='/auth', tags=['Аутентификация'])


async def authenticate_user(
    session: AsyncSession,
    login: str,
    password: str,
) -> User:
    """Найти пользователя по email/phone."""
    login = login.strip()

    stmt = (
        select(User)
        .where((User.email == login) | (User.phone == login))
        .limit(1)
    )
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail={'code': 401, 'message': 'Неверный логин или пароль'})
    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail={'code': 401, 'message': 'Неверный логин или пароль'})
    return user


@router.post(
    '/login',
    response_model=AuthToken,
    summary='Вход',
)
async def login(
    form: Annotated[AuthData, Depends(AuthData.as_form)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> AuthToken:
    """Авторизация пользователя по логину и паролю."""
    user = await authenticate_user(session, form.login, form.password)
    token = create_access_token(subject=str(user.id))
    return AuthToken(access_token=token, token_type='bearer')
