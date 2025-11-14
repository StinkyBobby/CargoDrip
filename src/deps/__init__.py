# src/deps/__init__.py
from .cargo_deps import get_cargo_service
from .truck_deps import get_truck_service
from .auth_deps import get_auth_service
from .shipment_deps import get_shipments_service

__all__ = [
    "get_cargo_service",
    "get_truck_service",
    "get_auth_service",
    "get_shipments_service"
]
