from datetime import datetime

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.types import DeliveryStatus

class ShipmentsORM(Base):
    __tablename__ = 'shipments'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    cargo_id: Mapped[int] = mapped_column(ForeignKey('cargos.id'))
    truck_id:Mapped[int] = mapped_column(ForeignKey('trucks.id'))
    assigned_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    status: Mapped[DeliveryStatus] = mapped_column(default=DeliveryStatus.waiting)
    completed_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
