from src.repositories import TrucksRepo
from src.service import TruckService

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.utils.token import decode_token
from src.scheme.employee_scheme import EmployeeDTO
from src.repositories.employee_repo import EmployeeRepo
from typing import Annotated
from src.service.cargo_service import CargoService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    repo: EmployeeRepo = Depends(),
) -> EmployeeDTO:
    try:
        payload = decode_token(token)
        user = await repo.find(id=int(payload["sub"]))
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return EmployeeDTO.model_validate(user)
    except Exception:
        raise HTTPException(status_code=401, detail="Невалидный токен")

def driver_only(current_user: Annotated[EmployeeDTO, Depends(get_current_user)]):
    if current_user.role.value != "Worker":
        raise HTTPException(status_code=403, detail="Доступ запрещён: только для водителей")
    return current_user

def admin_only(current_user: Annotated[EmployeeDTO, Depends(get_current_user)]):
    if current_user.role.value != "Admin":
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return current_user


class Deps:
    @staticmethod
    def cargo_service() -> CargoService:
        return CargoService()

class Deps:
    @staticmethod
    def truck_service():
        return TruckService(TrucksRepo)
