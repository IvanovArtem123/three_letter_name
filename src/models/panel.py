from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import BaseModel
from .many_to_many import subscription_panels


class Panel(BaseModel):
    """Модель панели."""

    path = Column(String(150), nullable=False)
    domain = Column(String(150), nullable=False)
    login = Column(String(150), nullable=False)
    password_hash = Column(String(255), nullable=False)
    country = Column(String(150), nullable=False)
    subscriptions = relationship(
        "Subscription",
        secondary=subscription_panels,
        back_populates="panels",
        lazy='selectin'
    )
