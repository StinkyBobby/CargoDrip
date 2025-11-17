from src.service.employee_service import EmployeeService
from src.repositories.employee_repo import EmployeeRepo

def get_employee_service() -> EmployeeService:
    return EmployeeService(employee_repo=EmployeeRepo()) 
