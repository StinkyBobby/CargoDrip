from .cargo_deps import get_cargo_service
from .truck_deps import get_truck_service
from .auth_deps import get_auth_service
from .shipment_deps import get_shipments_service
from .employee_deps import get_employee_service
from .order_deps import get_order_service


__all__ = [
    "get_cargo_service",
    "get_truck_service",
    "get_auth_service",
    "get_shipments_service",
    "get_employee_service",
    "get_order_service",
]
