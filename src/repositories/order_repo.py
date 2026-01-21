from src.repositories.sqlalchemy_repo import SQLalchemy
from src.models.order import OrderORM

class OrderRepo(SQLalchemy):
    model = OrderORM
