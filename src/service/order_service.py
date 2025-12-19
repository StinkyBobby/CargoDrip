from typing import List, Optional
from datetime import datetime

from fastapi import HTTPException
from starlette import status

from src.models.order import OrderStatus
from src.models.trucks import TrucksORM
from src.models.types import DeliveryStatus
from src.repositories.base_repo import AbstractRepo
from src.repositories.truck_repo import TrucksRepo
from src.repositories.shipments_repo import ShipmentsRepo
from src.repositories.order_repo import OrderRepo
from src.scheme.order_scheme import OrderCreate, OrderDTO, MoreOrdersDTO
from src.scheme.shipments_scheme import ShipmentsDTO, ShipmentsCreate


class OrderService:
    def __init__(
        self,
        order_repo: AbstractRepo,
        truck_repo: AbstractRepo,
        shipments_repo: AbstractRepo,
    ):
        self.order_repo = order_repo
        self.truck_repo = truck_repo
        self.shipments_repo = shipments_repo

    async def create_order(self, order: OrderCreate) -> OrderDTO:
        order_dict = order.model_dump()
        order_dict["status"] = OrderStatus.queued
        order_dict["truck_id"] = None

        db_order = await self.order_repo.create(order_dict)
        order_dto = OrderDTO.model_validate(db_order)

        await self._try_assign_truck_for_order(order_dto)

        updated = await self.order_repo.find(id=order_dto.id)
        return OrderDTO.model_validate(updated)

    async def _try_assign_truck_for_order(self, order: OrderDTO) -> bool:
        free_trucks: List[TrucksORM] = await self.truck_repo.find_all(available=True)
        if not free_trucks:
            return False

        truck = free_trucks[0]

        # создаём shipment
        shipment_create = ShipmentsCreate(
            cargo_id=order.cargo_id,
            truck_id=truck.id,
            from_location="Warehouse A",
            to_location=order.to_location,
            pickup_date=datetime.utcnow(),
            delivered_date=None,
            driver_deriver=None,  
            status=DeliveryStatus.on_way,
        )


        shipment_dict = shipment_create.model_dump()
        db_shipment = await self.shipments_repo.create(shipment_dict)
        ShipmentsDTO.model_validate(db_shipment)

        await self.truck_repo.update({"available": False}, id=truck.id)

        updated_order = await self.order_repo.update(
            {"status": OrderStatus.assigned, "truck_id": truck.id},
            id=order.id,
        )
        OrderDTO.model_validate(updated_order)

        return True

    async def get_queue(self) -> MoreOrdersDTO:
        orders = await self.order_repo.find_all(status=OrderStatus.queued)
        dto = [OrderDTO.model_validate(row) for row in orders]
        return MoreOrdersDTO(items=dto, total=len(dto))

    async def get_all(self) -> MoreOrdersDTO:
        orders = await self.order_repo.find_all()
        dto = [OrderDTO.model_validate(row) for row in orders]
        return MoreOrdersDTO(items=dto, total=len(dto))

    async def try_assign_for_truck(self, truck_id: int) -> Optional[OrderDTO]:
        truck = await self.truck_repo.find(id=truck_id)
        if truck is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Truck is not found",
            )

        queued_orders = await self.order_repo.find_all(status=OrderStatus.queued)
        if not queued_orders:
            return None

        order = queued_orders[0]
        order_dto = OrderDTO.model_validate(order)
        assigned = await self._try_assign_truck_for_order(order_dto)
        if not assigned:
            return None

        updated = await self.order_repo.find(id=order.id)
        return OrderDTO.model_validate(updated)
