from sqlalchemy import Table, Column, Integer, ForeignKey

from .base import BaseModel


subscription_panels = Table(
    'subscription_panels',
    BaseModel.metadata,
    Column('subscription_id', Integer, ForeignKey('subscriptions.id')),
    Column('panel_id', Integer, ForeignKey('panels.id'))
)
