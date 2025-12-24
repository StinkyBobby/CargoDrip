from typing import List, Optional
from datetime import datetime
import math

from fastapi import HTTPException
from starlette import status

from src.models.order import OrderStatus
from src.models.trucks import TrucksORM
from src.models.types import DeliveryStatus
from src.models.cargo import CargoORM
from src.models.shipments import ShipmentsORM

from src.repositories.base_repo import AbstractRepo
from src.repositories.truck_repo import TrucksRepo
from src.repositories.shipments_repo import ShipmentsRepo
from src.repositories.order_repo import OrderRepo
from src.repositories.cargo_repo import CargoRepo

from src.scheme.order_scheme import OrderCreate, OrderDTO, MoreOrdersDTO
from src.scheme.shipments_scheme import ShipmentsDTO, ShipmentsCreate

BASE_RATE_PER_KM = 1.5       
AVG_KM_PER_DAY = 400         


class OrderService:
    def __init__(
        self,
        order_repo: AbstractRepo,
        truck_repo: AbstractRepo,
        shipments_repo: AbstractRepo,
    ):
        self.order_repo: OrderRepo = order_repo  # type: ignore
        self.truck_repo: TrucksRepo = truck_repo  # type: ignore
        self.shipments_repo: ShipmentsRepo = shipments_repo  # type: ignore

    async def create_order(self, order: OrderCreate) -> OrderDTO:
        order_dict = order.model_dump()
        order_dict["status"] = OrderStatus.queued
        order_dict["truck_id"] = None

        distance = order_dict["distance_km"]
        price = distance * BASE_RATE_PER_KM
        estimated_days = max(1, math.ceil(distance / AVG_KM_PER_DAY))

        order_dict["price"] = price
        order_dict["estimated_days"] = estimated_days

        db_order = await self.order_repo.create(order_dict)
        order_dto = OrderDTO.model_validate(db_order)

        await self._try_assign_truck_for_order(order_dto)

        updated = await self.order_repo.find(id=order_dto.id)
        return OrderDTO.model_validate(updated)

    async def _try_assign_truck_for_order(self, order: OrderDTO) -> bool:
        cargo_repo = CargoRepo()
        cargo: CargoORM | None = await cargo_repo.find(id=order.cargo_id)
        if cargo is None:
            return False

        cargo_weight = cargo.weight

        trucks: List[TrucksORM] = await self.truck_repo.find_all()

        shipments_repo = ShipmentsRepo()

        for truck in trucks:
            shipments: List[ShipmentsORM] = await shipments_repo.find_all(
                truck_id=truck.id
            )

            total_weight = 0
            has_active_same_direction = False
            has_any_active = False

            for sh in shipments:
                if sh.status == DeliveryStatus.delivered:
                    continue

                has_any_active = True

                sh_cargo: CargoORM | None = await cargo_repo.find(id=sh.cargo_id)
                if sh_cargo:
                    total_weight += sh_cargo.weight

                if sh.to_location == order.to_location:
                    has_active_same_direction = True

            if total_weight + cargo_weight > truck.capacity_kg:
                continue

            if not has_any_active:
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

            if has_active_same_direction:
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

                updated_order = await self.order_repo.update(
                    {"status": OrderStatus.assigned, "truck_id": truck.id},
                    id=order.id,
                )
                OrderDTO.model_validate(updated_order)
                return True

        return False

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

    async def delete_order(self, order_id: int) -> None:
        order = await self.order_repo.find(id=order_id)
        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with id={order_id} not found",
            )

        await self.order_repo.delete(id=order_id)
