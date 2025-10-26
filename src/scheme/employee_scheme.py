from pydantic import BaseModel, Field, EmailStr
from src.models.types import role_enum_new
from datetime import datetime

# Схема для регистрации или создания сотрудника
class EmployeeCreate(BaseModel):
    username: str = Field(..., max_length=100)
    password: str = Field(..., min_length=6, max_length=72)
    role: role_enum_new
    email: EmailStr

# Схема для возврата данных о сотруднике (DTO)
class EmployeeDTO(BaseModel):
    id: int
    username: str
    role: role_enum_new
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# Схема для входа
class EmployeeLogin(BaseModel):
    username: str
    password: str

# Схема для токена
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
