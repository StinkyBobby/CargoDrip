from typing import List, Annotated

from fastapi import APIRouter, Query, Depends

from src.deps import Deps
from src.scheme import TruckDTO
from src.scheme.truck_scheme import TruckCreate, TruckDTO, MoreTruckDTO
from src.service.truck_service import TruckService
from src.utils.error import Forbidden

truck_router = APIRouter(
    tags=["Truck"],
    prefix="/trucks",
)


@truck_router.post("")
async def create_truck(
    truck: TruckCreate,
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)],
) -> TruckDTO:
    db_truck = await truck_service.add_truck(truck)
    return db_truck


@truck_router.post("/more")
async def create_more(
    trucks: List[TruckCreate],
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)]
) -> List[TruckDTO]:
    dto_trucks = await truck_service.add_more(trucks)
    return dto_trucks


@truck_router.get("")
async def get_trucks(
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)],
) -> MoreTruckDTO:
    trucks = await truck_service.get_more()
    return trucks




@truck_router.get("/{truck_id}")
async def get_truck(
    truck_id: int, 
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)]
) -> TruckDTO:
    truck = await truck_service.get_single(id=truck_id)
    return truck


@truck_router.delete("")
async def delete_truck(
    truck_id: int,
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)]
) -> TruckDTO:
    truck_delete = await truck_service.delete_truck(truck_id)
    return truck_delete


@truck_router.put("/{truck_id}")
async def update_truck(
    truck_id: int,
    truck: TruckCreate,
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)],
) -> TruckDTO:
    return await truck_service.update_truck(truck_id, truck)

@truck_router.patch("/{truck_id}/availability")
async def available_truck(
    truck_id: int,
    available: bool,
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)],
) -> TruckDTO:
    return await truck_service.set_availability(truck_id, available)
