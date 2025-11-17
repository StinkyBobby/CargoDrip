from typing import List
from fastapi import APIRouter, Query, Depends
from src.scheme.employee_scheme import EmployeeCreate, EmployeeDTO
from src.service.employee_service import EmployeeService
from src.deps.employee_deps import get_employee_service

employee_router = APIRouter(
    tags=["Employee"],
    prefix="/employees",
)

@employee_router.post("", response_model=EmployeeDTO)
async def create_employee(
    employee: EmployeeCreate,
    employee_service: EmployeeService = Depends(get_employee_service)
) -> EmployeeDTO:
    db_employee = await employee_service.add_employee(employee)
    return db_employee

@employee_router.post("/more", response_model=List[EmployeeDTO])
async def create_more(
    employees: List[EmployeeCreate],
    employee_service: EmployeeService = Depends(get_employee_service)
) -> List[EmployeeDTO]:
    dto_employees = await employee_service.add_more(employees)
    return dto_employees

@employee_router.get("", response_model=List[EmployeeDTO])
async def get_employees(
    employee_service: EmployeeService = Depends(get_employee_service),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    order_by: str = ""
) -> List[EmployeeDTO]:
    employees = await employee_service.get_more(limit=limit, offset=offset, order_by=order_by)
    return employees

@employee_router.get("/{employee_id}", response_model=EmployeeDTO)
async def get_employee(
    employee_id: int,
    employee_service: EmployeeService = Depends(get_employee_service)
) -> EmployeeDTO:
    employee = await employee_service.get_single(id=employee_id)
    return employee

@employee_router.delete("/{employee_id}", response_model=EmployeeDTO)
async def delete_employee(
    employee_id: int,
    employee_service: EmployeeService = Depends(get_employee_service)
) -> EmployeeDTO:
    employee_delete = await employee_service.delete_employee(employee_id)
    return employee_delete

@employee_router.put("/{employee_id}", response_model=EmployeeDTO)
async def update_employee(
    employee_id: int,
    employee: EmployeeCreate,
    employee_service: EmployeeService = Depends(get_employee_service)
) -> EmployeeDTO:
    return await employee_service.update_employee(employee_id, employee)
