from datetime import datetime
from sqlalchemy import Integer, text, Enum
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base
from src.models.types import RoleEnum

class EmployeeORM(Base):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, name="roleenum", create_type=False),
        default=RoleEnum.driver,
        nullable=False
    )

    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
