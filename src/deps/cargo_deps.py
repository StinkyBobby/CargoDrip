from src.service.cargo_service import CargoService
from src.repositories.cargo_repo import CargoRepo  # или твоя реализация

def get_cargo_service() -> CargoService:
    return CargoService(cargo_repo=CargoRepo())
