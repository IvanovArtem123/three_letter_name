from string import ascii_uppercase, digits
import json
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from core.db import get_async_session
from models.user import User
from schemas.user import UserInfo
from models.subscription import Subscription
from core.config import settings
from crud.promocode import promocode_crud
from string import ascii_uppercase, digits
from random import choices

USER_FIELDS_TO_LOAD = [
    User.id,
    User.username,
    User.uuid,
    User.email,
    User.tg_id,
    User.new,
    User.role,
    User.created_at,
    User.updated_at,
]


async def get_current_user(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> UserInfo:
    """Возвращает текущего пользователя по сессии."""
    bot_secret = request.headers.get("X-Bot-Secret")
    if bot_secret is not None:
        if bot_secret != settings.TG_BOT_SECRET:
            raise HTTPException(status_code=403, detail="Forbidden")
        tg_id = request.headers.get("X-TG-ID")
        if tg_id is None:
            raise HTTPException(status_code=400,
                                detail="X-TG-ID header required")
        query = select(User).where(
            User.tg_id == int(tg_id)).options(load_only(*USER_FIELDS_TO_LOAD))
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return UserInfo.model_validate(user)
    user_id = request.session.get("user_id")

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session",
        )

    query = (
        select(User)
        .where(User.id == user_id)
        .options(load_only(*USER_FIELDS_TO_LOAD))
    )
    result = await session.execute(query)
    user = result.scalars().first()

    if user is None:
        request.session.clear()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return UserInfo.model_validate(user)


async def get_list_inbound_id(data: str) -> list[int]:
    '''Получаем id инбаундов панели.'''
    data = json.loads(data)
    obj = data['obj']
    result = []
    for inbound in obj:
        inbound_id = inbound['id']
        result.append(int(inbound_id))
    return result


async def data_user_config(
        inbound_id: int, user: User, sub: Subscription,
        transport: str
        ) -> dict:
    '''Формируем data для запроса на добавления пользователя в inbound.'''
    if transport == 'xhttp':
        flow = ''
    if transport == 'tcp':
        flow = 'xtls-rprx-vision'
    end_date = sub.end_date
    expiry_time = int(end_date.timestamp() * 1000)
    settings_data = {
        'clients': [
            {
                'id': user.uuid,
                'flow': flow,
                'email': user.email,
                'limitIp': 0,
                'totalGB': 0,
                'expiryTime': expiry_time,
                'enable': True,
                'tgId': user.tg_id,
                'subId': sub.code,
                'comment': user.username,
                'reset': 0
            }
        ]
    }
    data = {
        'id': inbound_id,
        'settings': json.dumps(settings_data)
    }
    return data


async def get_inbound_transport(
        response_text: str
) -> str:
    '''Получаем транспорт инбаунда.'''
    obj_response = json.loads(response_text)
    obj = obj_response['obj']['streamSettings']
    return obj['network']


async def making_promocode(code_len: int = 10) -> str:
    """Генерация случайного промокода."""
    import random
    import string

    characters = string.ascii_uppercase + string.digits
    promocode = ''.join(random.choice(characters) for _ in range(code_len))
    return promocode.upper()


async def generate_unique_code(session: AsyncSession, length: int = 10) -> str:
    """
    Генерирует уникальный код.
    """
    while True:
        code = ''.join(choices(ascii_uppercase + digits, k=length))
        existing = await promocode_crud.get_code(session=session, code=code)
        if existing is None:
            return code
