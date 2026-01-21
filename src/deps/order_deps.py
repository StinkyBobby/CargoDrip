from src.service.order_service import OrderService
from src.repositories.order_repo import OrderRepo
from src.repositories.truck_repo import TrucksRepo
from src.repositories.shipments_repo import ShipmentsRepo


def get_order_service() -> OrderService:
    return OrderService(
        order_repo=OrderRepo(),
        truck_repo=TrucksRepo(),
        shipments_repo=ShipmentsRepo(),
    )
