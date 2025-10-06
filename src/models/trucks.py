from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

class TrucksORM(Base):
    __tablename__ = "trucks"

    id: Mapped[int] = mapped_column(primary_key=True)
    plate_number: Mapped[str]
    model: Mapped[str]
    capacity_kg: Mapped[int]
    volume_m3: Mapped[int]
    is_refrigerated: Mapped[bool]
    available: Mapped[bool]