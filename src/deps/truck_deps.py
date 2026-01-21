from src.service.truck_service import TruckService
from src.service.order_service import OrderService
from src.repositories.truck_repo import TrucksRepo
from src.repositories.order_repo import OrderRepo
from src.repositories.shipments_repo import ShipmentsRepo


def get_truck_service() -> TruckService:
    order_service = OrderService(
        order_repo=OrderRepo(),
        truck_repo=TrucksRepo(),
        shipments_repo=ShipmentsRepo(),
    )
    return TruckService(truck_repo=TrucksRepo(), order_service=order_service)
