from src.repositories.sqlalchemy_repo import SQLalchemy
from src.models.trucks import TrucksORM


class TrucksRepo(SQLalchemy):
    model=TrucksORM
