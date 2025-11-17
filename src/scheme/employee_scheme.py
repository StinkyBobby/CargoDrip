from pydantic import BaseModel, Field, EmailStr
from src.models.types import role_enum_new
from datetime import datetime

class EmployeeCreate(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=72)
    role: role_enum_new
    email: EmailStr

class EmployeeDTO(BaseModel):
    id: int
    username: str
    role: role_enum_new
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class EmployeeLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
