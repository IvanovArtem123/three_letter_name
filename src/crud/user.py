from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from .base import CRUDBase
from models.user import User
from schemas.user import UserUpdate, TelegramLoginSchema
from core.security import hash_password


class CRUDUser(CRUDBase[User, TelegramLoginSchema, UserUpdate]):

    async def update_user_with_hash_password(
            self,
            db_obj: User,
            obj_in: UserUpdate,
            session: AsyncSession
    ) -> User:
        '''Обновить пользователя с хэшированием пароля.'''
        obj_in_data = obj_in.model_dump(exclude_unset=True)
        if 'password' in obj_in_data:
            password_hash = await hash_password(obj_in_data.pop('password'))
            obj_in_data['password_hash'] = password_hash
        for field, value in obj_in_data.items():
            setattr(db_obj, field, value)
            session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_uuid_by_id(
        self,
        user_id: int,
        session: AsyncSession
    ) -> str | None:
        '''Получить uuid пользователя по его id.'''
        result = await session.execute(
            select(User.uuid).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_tg_id(
        self,
        session: AsyncSession,
        tg_id: str
    ) -> User | None:
        '''Получить пользователя по его Telegram id.'''
        result = await session.execute(
            select(User).where(User.tg_id == tg_id)
        )
        return result.scalar_one_or_none()


user_crud = CRUDUser(User)
