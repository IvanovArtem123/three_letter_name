from typing import Sequence

from datetime import datetime
from sqlalchemy import select

from schemas.subscription import SubscriptionCreate, SubscriptionUpdate
from sqlalchemy.ext.asyncio import AsyncSession

from models.panel import Panel
from .base import CRUDBase
from models.subscription import Subscription
from .services import setup_end_date_subscription


class CRUDSub(CRUDBase[Subscription, SubscriptionCreate, SubscriptionUpdate]):
    """CRUD для пользовательской подписки."""

    async def create_subscription(
        self,
        obj_in: SubscriptionCreate,
        panels: list[Panel],
        session: AsyncSession
    ):
        """Создание подписки."""
        end_date = setup_end_date_subscription(
            start_date=datetime.now(),
            level=obj_in.end_date_level
        )
        subscription = Subscription(
            user_id=obj_in.user_id,
            end_date=end_date,
            status=obj_in.status,
            panels=panels,
            is_trial=obj_in.is_trial,
            is_gift=obj_in.is_gift
        )
        session.add(subscription)
        await session.commit()
        await session.refresh(subscription)
        return subscription

    async def get_subs_by_user_id(
        self,
        user_id: int,
        session: AsyncSession
    ) -> Sequence[Subscription]:
        """Получить все подписки пользователя по его id."""
        result = await session.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        subscriptions = result.scalars().all()
        return subscriptions

    async def get_subscription_by_sub_code(
        self,
        sub_code: str,
        session: AsyncSession
    ) -> Subscription | None:
        """Получить подписку по ее коду."""
        result = await session.execute(
            select(Subscription).where(Subscription.code == sub_code)
        )
        subscription = result.scalars().first()
        return subscription


sub_crud = CRUDSub(Subscription)
