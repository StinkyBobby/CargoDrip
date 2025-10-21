from src.repositories.sqlalchemy_repo import SQLalchemy
from src.models.cargo import CargoORM

class CargoRepo(SQLalchemy):
    model=CargoORM
