from datetime import datetime
from typing import Optional

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class CompaniesORM(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    registration_number: Mapped[int]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    adress: Mapped[Optional[int | None]]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
