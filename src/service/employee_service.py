from typing import List
from fastapi import HTTPException
from starlette import status
from src.repositories.base_repo import AbstractRepo
from src.scheme.employee_scheme import EmployeeDTO, EmployeeCreate


class EmployeeService:
    def __init__(self, employee_repo: AbstractRepo):
        self.employee_repo = employee_repo

    async def get_single(self, **filters) -> EmployeeDTO:
        employee = await self.employee_repo.find(**filters)
        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee is not found"
            )
        return EmployeeDTO.model_validate(employee)

    async def get_more(
        self, limit: int = 100, offset: int = 0, order_by: str = "", **filters
    ) -> List[EmployeeDTO]:
        employees = await self.employee_repo.find_all(
            limit=limit, offset=offset, order_by=order_by, **filters
        )
        return [EmployeeDTO.model_validate(row) for row in employees]

    async def add_employee(self, employee: EmployeeCreate) -> EmployeeDTO:
        employee_dict = employee.model_dump()
        # преобразуем password → password_hash
        employee_dict["password_hash"] = employee_dict.pop("password")
        # здесь можно добавить хэширование, например bcrypt
        db_employee = await self.employee_repo.create(employee_dict)
        return EmployeeDTO.model_validate(db_employee)

    async def add_more(self, employees: List[EmployeeCreate]) -> List[EmployeeDTO]:
        employees_dict = []
        for row in employees:
            row_dict = row.model_dump()
            row_dict["password_hash"] = row_dict.pop("password")
            employees_dict.append(row_dict)
        db_employees = await self.employee_repo.create_more(employees_dict)
        return [EmployeeDTO.model_validate(row) for row in db_employees]

    async def update_employee(self, employee_id: int, employee: EmployeeCreate) -> EmployeeDTO:
        db_employee = await self.employee_repo.find(id=employee_id)
        if db_employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee is not found"
            )
        employee_dict = employee.model_dump()
        employee_dict["password_hash"] = employee_dict.pop("password")
        updated = await self.employee_repo.update(employee_dict, id=employee_id)
        return EmployeeDTO.model_validate(updated)

    async def delete_employee(self, employee_id: int) -> EmployeeDTO:
        employee = await self.employee_repo.delete(id=employee_id)
        if employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Employee is not found"
            )
        return EmployeeDTO.model_validate(employee)
