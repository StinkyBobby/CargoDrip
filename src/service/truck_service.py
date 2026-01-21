from typing import Callable, List, Optional
from fastapi import HTTPException
from starlette import status
from src.models.types import DeliveryStatus
from src.repositories.base_repo import AbstractRepo
from src.repositories.shipments_repo import ShipmentsRepo
from src.scheme.shipments_scheme import ShipmentsDTO
from src.scheme.truck_scheme import MoreTruckDTO, TruckDTO, TruckCreate
from src.service.order_service import OrderService


class TruckService:
    def __init__(
        self,
        truck_repo: Callable[[], AbstractRepo],
        order_service: Optional[OrderService] = None,
    ):
        self.truck_repo: AbstractRepo = truck_repo
        self.order_service = order_service

    async def get_single(self, **filters) -> TruckDTO:
        truck = await self.truck_repo.find(**filters)
        if truck is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="truck is not found"
            )

        return TruckDTO.model_validate(truck)

    async def get_more(
        self, limit: int = 100, offset: int = 0, order_by: str = "", **filters
    ) -> MoreTruckDTO:
        truck = await self.truck_repo.find_all(limit=limit, offset=offset, **filters)

        truck_dto = [TruckDTO.model_validate(row) for row in truck]
        return MoreTruckDTO(items=truck_dto, total=len(truck_dto))

    async def add_truck(self, truck: TruckCreate) -> TruckDTO:
        truck_dict = truck.model_dump()
        truck = await self.truck_repo.create(truck_dict)

        return TruckDTO.model_validate(truck)

    async def add_more(self, truck: List[TruckCreate]) -> List[TruckDTO]:
        truck_dict = [row.model_dump() for row in truck]
        db_trucks = await self.truck_repo.create_more(truck_dict)

        list_trucks_dto = [TruckDTO.model_validate(row) for row in db_trucks]
        return list_trucks_dto

    async def update_truck(self, truck_id: int, truck: TruckCreate) -> TruckDTO:
        db_trucks = await self.truck_repo.find(id=truck_id)
        if db_trucks is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Truck is not found"
            )

        updated = await self.truck_repo.update(truck.model_dump(), id=truck_id)
        return TruckDTO.model_validate(updated)

    async def delete_truck(self, truck_id: int) -> TruckDTO:
        truck = await self.truck_repo.delete(id=truck_id)

        if truck is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Truck is not found"
            )

        return TruckDTO.model_validate(truck)

    async def set_availability(self, truck_id: int, available: bool) -> TruckDTO:
        truck = await self.truck_repo.find(id=truck_id)

        if truck is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Truck is not found"
            )

        updated = await self.truck_repo.update({"available": available}, id=truck_id)
        dto = TruckDTO.model_validate(updated)

        if available and self.order_service is not None:
            await self.order_service.try_assign_for_truck(truck_id)

        return dto


    async def get_status_report(self) -> dict:
        # свободные
        free_trucks = await self.truck_repo.find_all(available=True)
        free_trucks_dto = [TruckDTO.model_validate(t) for t in free_trucks]

        # все занятые
        busy_trucks = await self.truck_repo.find_all(available=False)
        busy_trucks_dto = [TruckDTO.model_validate(t) for t in busy_trucks]

        # активные 
        shipments_repo = ShipmentsRepo()
        active_shipments = await shipments_repo.find_all()
        active_shipments_dto = [
            ShipmentsDTO.model_validate(s) for s in active_shipments if s.status != DeliveryStatus.delivered
        ]

        return {
            "free_trucks": free_trucks_dto,
            "busy_trucks": busy_trucks_dto,
            "active_shipments": active_shipments_dto,
        }
