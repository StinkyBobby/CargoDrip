from src.service.truck_service import TruckService
from src.repositories.truck_repo import TrucksRepo  

def get_truck_service() -> TruckService:
    return TruckService(truck_repo=TrucksRepo())
