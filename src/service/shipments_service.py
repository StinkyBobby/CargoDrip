from typing import Callable, List

from fastapi import HTTPException
from starlette import status
from src.repositories.base_repo import AbstractRepo
from src.scheme.shipments_scheme import ShipmentsDTO, MoreShipmentsDTO, ShipmentsCreate


class ShipmentsService():
    def __init__(self, shipments_repo: Callable[[], AbstractRepo]):
        self.shipments_repo: AbstractRepo = shipments_repo

    async def get_single(self, **filters) -> ShipmentsDTO:
        shipment = await self.shipments_repo.find(**filters)
        if shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment is not found"
            )
        return ShipmentsDTO.model_validate(shipment)

    async def get_more(
        self, limit: int = 100, offset: int = 0, order_by: str = "", **filters
    ) -> MoreShipmentsDTO:
        shipments = await self.shipments_repo.find_all(
            limit=limit, offset=offset, order_by=order_by, **filters
        )
        shipments_dto = [ShipmentsDTO.model_validate(row) for row in shipments]
        return MoreShipmentsDTO(items=shipments_dto, total=len(shipments_dto))

    async def add_shipment(self, shipment: ShipmentsCreate) -> ShipmentsDTO:
        shipment_dict = shipment.model_dump()
        db_shipment = await self.shipments_repo.create(shipment_dict)
        return ShipmentsDTO.model_validate(db_shipment)

    async def add_more(self, shipments: List[ShipmentsCreate]) -> List[ShipmentsDTO]:
        shipments_dict = [row.model_dump() for row in shipments]
        db_shipments = await self.shipments_repo.create_more(shipments_dict)
        return [ShipmentsDTO.model_validate(row) for row in db_shipments]

    async def update_shipment(self, shipment_id: int, shipment: ShipmentsCreate) -> ShipmentsDTO:
        db_shipment = await self.shipments_repo.find(id=shipment_id)
        if db_shipment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Shipment is not found"
            )
        updated = await self.shipments_repo.update(shipment.model_dump(), id=shipment_id)
        return ShipmentsDTO.model_validate(updated)

    async def delete_shipment(self, shipment_id: int) -> ShipmentsDTO:
        shipment = await self.shipments_repo.delete(id=shipment_id)
        return ShipmentsDTO.model_validate(shipment)
