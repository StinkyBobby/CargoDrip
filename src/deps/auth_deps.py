from src.service.auth_service import AuthService
from src.repositories.employee_repo import EmployeeRepo

def get_auth_service() -> AuthService:
    return AuthService(employee_repo=EmployeeRepo()) 
