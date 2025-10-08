from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base

class CargoORM(Base):
    __tablename__ = "cargoes"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender: Mapped[str]
    weight: Mapped[int]
    volume: Mapped[int]

