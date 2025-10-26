from pydantic import BaseModel

class EmployeeLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    role: str
    redirect_url: str
