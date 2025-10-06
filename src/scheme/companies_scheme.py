from pydantic import BaseModel, Field, EmailStr
from src.models.types import UserType
from datetime import datetime

class CompanyCreate(BaseModel):
    name: str = Field(max_length=100)
    registration_number: int
    email: EmailStr # что такое
    phone: str
    adress: int | None
    created_at: datetime


class CompanyDTO(CompanyCreate):
    id: int

    class Config:
        from_attributes = True


