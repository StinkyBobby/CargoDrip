from pydantic import BaseModel, Field
from src.models.types import UserType
from datetime import datetime

class EmployeeCreate(BaseModel):
    username: str = Field(max_length=100)
    password_hash: int
    role: UserType
    email: str
    created_at: datetime


class EmployeeDTO(EmployeeCreate):
    id: int

    class Config:
        from_attributes = True

