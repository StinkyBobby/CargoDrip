from fastapi import APIRouter

from src.api import (
    truck_router
)


def get_apps_routes() -> APIRouter:
    router = APIRouter()

    router.include_router(truck_router)

    return router