from fastapi import HTTPException
from src.repositories.employee_repo import EmployeeRepo
from src.scheme.auth_scheme import EmployeeLogin
from src.scheme.employee_scheme import EmployeeDTO
from src.utils.token import create_token

class AuthService:
    def __init__(self, employee_repo: EmployeeRepo): 
        self.repo = employee_repo

    async def authenticate(self, username: str, password: str) -> EmployeeDTO:
        user = await self.repo.find(username=username)
        if user is None or user.password_hash != hash(password):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        return EmployeeDTO.model_validate(user)

    async def login(self, credentials: EmployeeLogin) -> str:
        user = await self.authenticate(credentials.username, credentials.password)
        return create_token(user.id, user.role.value)
