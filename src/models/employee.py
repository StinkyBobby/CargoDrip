from datetime import datetime

from sqlalchemy import ForeignKey, Integer, func, text
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base
from src.models.types import UserType

class EmployeeORM(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    password_hash: Mapped[int]
    role: Mapped[UserType] = mapped_column(default=UserType.worker)
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))  