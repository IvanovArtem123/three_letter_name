from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from models.subscription import Subscription_Date_Levels
from crud.promocode import promocode_crud
from sqlalchemy.ext.asyncio import AsyncSession


def setup_end_date_subscription(start_date: datetime, level: int) -> datetime:
    """Установка даты окончания подписки."""
    match level:
        case Subscription_Date_Levels.DAY:
            return start_date + timedelta(days=1)
        case Subscription_Date_Levels.WEEK:
            return start_date + timedelta(weeks=1)
        case Subscription_Date_Levels.MONTH:
            return start_date + relativedelta(months=1)
        case Subscription_Date_Levels.THREE_MONTHS:
            return start_date + relativedelta(months=3)
        case Subscription_Date_Levels.HALF_YEAR:
            return start_date + relativedelta(months=6)
        case Subscription_Date_Levels.YEAR:
            return start_date + relativedelta(years=1)
        case _:
            raise ValueError(f'Неизвестный уровень подписки: {level}')
