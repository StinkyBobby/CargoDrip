from .truck import truck_router
from .auth import auth_router
from .cargo import cargo_router
from .shipment import shipments_router
from .employee import employee_router

__all__ = [
    "truck_router",
    "cargo_router",
    "auth_router",
    "shipments_router",
    "employee_router",
]