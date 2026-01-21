from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base


class OrderStatus(str, Enum):
    queued = "queued"
    assigned = "assigned"
    completed = "completed"

class OrderORM(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    cargo_id: Mapped[int] = mapped_column(ForeignKey("cargoes.id"))
    to_location: Mapped[str]
    distance_km: Mapped[int]
    price: Mapped[float] = mapped_column(default=0.0)
    estimated_days: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.queued)
    truck_id: Mapped[Optional[int]] = mapped_column(ForeignKey("trucks.id"), nullable=True)
