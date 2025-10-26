from src.repositories.sqlalchemy_repo import SQLalchemy
from src.models.employee import EmployeeORM
import bcrypt

from src.scheme.employee_scheme import EmployeeCreate

class EmployeeRepo(SQLalchemy):
    model=EmployeeORM

    async def create_with_hash(self, data: EmployeeCreate):
        hashed_password = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
        employee_dict = data.model_dump()
        employee_dict["password_hash"] = hashed_password
        del employee_dict["password"]
        return await self.create(employee_dict)

