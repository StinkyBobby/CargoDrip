from fastapi import APIRouter

from src.api import (
    auth_router,
    cargo_router,
    truck_router,
    shipments_router,
    employee_router,
)

def get_apps_routes():
    return [
        auth_router,
        cargo_router,
        truck_router,
        shipments_router,
        employee_router,
    ]