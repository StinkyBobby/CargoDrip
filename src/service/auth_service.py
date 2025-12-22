from fastapi import HTTPException
from typing import Tuple

from src.repositories.employee_repo import EmployeeRepo
from src.scheme.auth_scheme import EmployeeLogin
from src.scheme.employee_scheme import EmployeeDTO
from src.utils.token import create_token
from src.utils.password import verify_password  


class AuthService:
    def __init__(self, employee_repo: EmployeeRepo):
        self.repo = employee_repo

    async def authenticate(self, username: str, password: str) -> EmployeeDTO:
        user = await self.repo.find(username=username)

        if user is None or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")

        return EmployeeDTO.model_validate(user)

    async def login(self, credentials: EmployeeLogin) -> Tuple[str, str, str]:
        user = await self.authenticate(credentials.username, credentials.password)
        token = create_token(user.id, user.role.value)

        if user.role.value == "admin":
            redirect_url = "/admin_dashboard"
        elif user.role.value == "driver":
            redirect_url = "/driver_dashboard"
        else:
            redirect_url = "/"

        return token, user.role.value, redirect_url
