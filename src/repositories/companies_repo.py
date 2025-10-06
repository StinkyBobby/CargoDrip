from sqlalchemy_repo import SQLalchemy
from src.models.companies import CompaniesORM

class CompaniesRepo(SQLalchemy):
    model=CompaniesORM
