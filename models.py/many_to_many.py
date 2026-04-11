from sqlalchemy import Table, Column, Integer, ForeignKey

from core.db import Base


subscription_panels = Table(
    'subscription_panels',
    Base.metadata,
    Column('subscription_id', Integer, ForeignKey('subscriptions.id')),
    Column('panel_id', Integer, ForeignKey('panels.id'))
)
