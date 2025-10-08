from src.repositories import TrucksRepo
from src.service import TruckService

class Deps:
    @staticmethod
    def truck_service():
        return TruckService(TrucksRepo)
