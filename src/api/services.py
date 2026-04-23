from typing import Annotated, Optional

from fastapi import Depends, HTTPException, Request, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from core.db import get_async_session
from core.security import TokenError, decode_token
from models.user import User
from schemas.user import UserInfo, UserRole

bearer_scheme = HTTPBearer(auto_error=False)
bearer_optional = HTTPBearer(auto_error=False)


USER_FIELDS_TO_LOAD = [
    User.id,
    User.username,
    User.uuid,
    User.email,
    User.phone,
    User.tg_id,
    User.role,
    User.created_at,
    User.updated_at,
]


async def get_current_user(
    _: Response,
    creds: Annotated[
        Optional[HTTPAuthorizationCredentials],
        Security(bearer_scheme),
    ],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserInfo:
    """Возвращает текущего пользователя по Bearer-токену."""
    if creds is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    token = creds.credentials
    try:
        payload = decode_token(token)
    except TokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    sub = payload.get('sub')
    try:
        user_id = int(sub)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    query = (
        select(User)
        .where(User.id == user_id)
        .options(load_only(*USER_FIELDS_TO_LOAD))
    )
    result = await session.execute(query)
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='User not found',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return UserInfo.model_validate(user)
