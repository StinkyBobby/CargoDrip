from src.service.shipments_service import ShipmentsService
from src.repositories.shipments_repo import ShipmentsRepo 

def get_shipments_service() -> ShipmentsService:
    return ShipmentsService(shipments_repo=ShipmentsRepo())
