from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

from src.models.types import AcceptionStatus
from src.models.base import Base

class CargoORM(Base):
    __tablename__ = "cargos"

    id: Mapped[int] = mapped_column(primary_key=True)
    cargo_from_company: Mapped[str] = mapped_column(ForeignKey('companies.id'))
    description: Mapped[str]
    weight: Mapped[int]
    volume: Mapped[int]
    fragile: Mapped[bool]  #хрупкость
    hazardous: Mapped[bool]
    temperature_sensitive: Mapped[bool]
    from_location: Mapped[str]
    to_location: Mapped[str]
    pickup_date: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    delivered_date: Mapped[datetime] = mapped_column(default=datetime.now(), onupdate=datetime.now())
    status: Mapped[AcceptionStatus] = mapped_column(default=AcceptionStatus.in_process)
