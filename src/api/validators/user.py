from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from api.exceptions import bad_request
from sqlalchemy import select, or_

from schemas.user import UserCreate
from models.user import User


async def check_unique_email_username_phone_tgid(
        user_obj: UserCreate,
        session: AsyncSession
) -> None:
    """Проверка на уникальность полей модели пользователя:
    email
    username
    phone
    tg_id"""
    conditions = []
    if user_obj.username:
        conditions.append(User.username == user_obj.username)
    if user_obj.email:
        conditions.append(User.email == user_obj.email)
    if user_obj.phone:
        conditions.append(User.phone == user_obj.phone)
    if conditions:
        existing_users = await session.execute(
            select(User).where(or_(*conditions))
        )
        existing_users = existing_users.scalars().all()
        if existing_users:
            message = 'Поля уже заняты: '
            for existing in existing_users:
                if (user_obj.username and
                        existing.username == user_obj.username):
                    message += 'username, '
                if user_obj.email and existing.email == user_obj.email:
                    message += 'email, '
                if user_obj.phone and existing.phone == user_obj.phone:
                    message += 'phone, '
            result = message[:-2] + '.'
            raise bad_request(result)
    return None
