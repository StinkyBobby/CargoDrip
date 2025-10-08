from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.types import DeliveryStatus

class ShipmentsORM(Base):
    __tablename__ = 'shipments'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cargo_id: Mapped[int] = mapped_column(ForeignKey('cargoes.id'))
    truck_id:Mapped[int] = mapped_column(ForeignKey('trucks.id'))
    from_location: Mapped[str]
    to_location: Mapped[str]
    pickup_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    delivered_date: Mapped[Optional[datetime]]
    status: Mapped[DeliveryStatus] = mapped_column(default=DeliveryStatus.on_way)