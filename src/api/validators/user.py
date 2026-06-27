from sqlalchemy.ext.asyncio import AsyncSession
from api.exceptions import bad_request, not_found, forbidden
from sqlalchemy import select, or_

from schemas.user import UserUpdate
from models.user import User, UserRole
from crud.user import user_crud


async def check_unique_email_username_phone_tgid(
    user_obj: UserUpdate,
    session: AsyncSession
) -> None:
    """Проверка на уникальность tg_id."""
    conditions = []
    if user_obj.tg_id:
        conditions.append(User.tg_id == user_obj.tg_id)
    if conditions:
        existing_users = await session.execute(
            select(User).where(or_(*conditions))
        )
        existing_obj_users = existing_users.scalars().all()
        if existing_obj_users:
            message = 'Поля уже заняты: '
            for existing in existing_obj_users:
                if user_obj.tg_id and existing.tg_id == user_obj.tg_id:
                    message += 'tg_id, '
            result = message[:-2] + '.'
            raise bad_request(result)
    return None


async def check_current_user_admin(
    user: User
) -> bool:
    """Проверка является юзер админом или суперюзером."""
    if user.role == UserRole.ADMIN or user.role == UserRole.SUPER_USER:
        return True
    return False


async def get_user_or_404(
    user_id: int,
    session: AsyncSession
) -> User:
    """Получить пользователя по id или 404 ошибку."""
    result = await user_crud.get(session=session, obj_id=user_id)
    if not result:
        raise not_found('Пользователь не найден.')
    return result


async def get_user_by_tg_id_or_404(
    tg_id: int,
    session: AsyncSession
) -> User:
    """Получить пользователя по Telegram id или 404 ошибку."""
    result = await user_crud.get_by_tg_id(session=session, tg_id=tg_id)
    if not result:
        raise not_found('Пользователь не найден.')
    return result


async def check_permission_values(
    user_in: UserUpdate, user: User
) -> None:
    '''
    Проверяем может ли пользователь изменять поля:
    role
    '''
    if user_in.role and (
        user.role != UserRole.ADMIN or user.role != UserRole.SUPER_USER
    ):
        raise forbidden('У Вас недостаточно прав для изменения своей роли.')
