from .base_repo import AbstractRepo

from .truck_repo import TrucksRepo
from .cargo_repo import CargoRepo
from .employee_repo import EmployeeRepo
from .shipments_repo import ShipmentsRepo

from .sqlalchemy_repo import SQLalchemy

__all__ = [
'AbstractRepo',
'TrucksRepo',
'CargoRepo',
'EmployeeRepo',
'ShipmentsRepo',
'SQLalchemy'
]