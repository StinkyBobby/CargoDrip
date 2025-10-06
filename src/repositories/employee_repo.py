from sqlalchemy_repo import SQLalchemy
from src.models.employee import EmployeeORM

class EmployeeRepo(SQLalchemy):
    model=EmployeeORM
