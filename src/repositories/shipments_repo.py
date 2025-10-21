from src.repositories.sqlalchemy_repo import SQLalchemy
from src.models.shipments import ShipmentsORM

class ShipmentsRepo(SQLalchemy):
    model=ShipmentsORM
