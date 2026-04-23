from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import hash_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create_hash_password(
            self,
            obj_in: UserCreate,
            session: AsyncSession
    ) -> User:
        """Создать пользователя с хэшированным паролем."""
        password_hash = await hash_password(obj_in.password)
        obj_in_data = obj_in.model_dump(exclude={'password'})
        db_obj = User(**obj_in_data, password_hash=password_hash)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


user_crud = CRUDUser(User)
