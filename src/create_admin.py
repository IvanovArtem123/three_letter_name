import asyncio
import sys
from sqlalchemy import select
from core.db import AsyncSessionLocal
from models.user import User, UserRole


async def create_admin(email: str):
    async with AsyncSessionLocal() as session:
        stmt = select(User).where(User.email == email).limit(1)
        user = await session.scalar(stmt)
        if user is None:
            print(f'❌ Пользователь с email {email!r} не найден')
            print('Сначала залогинься через Google.')
            return
        if user.role == int(UserRole.ADMIN):
            print(f'✅ {email} уже админ')
            return
        user.role = int(UserRole.ADMIN)
        await session.commit()
        print(f'✅ {email} теперь админ')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Использование: python -m scripts.create_admin your@email.com')
        sys.exit(1)

    asyncio.run(create_admin(sys.argv[1]))
