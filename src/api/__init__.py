from .truck import truck_router
from .auth import auth_router
from .cargo import cargo_router

__all__ = [
    "truck_router",
    "cargo_router",
    "auth_router",
]