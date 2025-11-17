from typing import List
from fastapi import APIRouter, Depends

from src.deps.shipment_deps import get_shipments_service
from src.scheme.shipments_scheme import ShipmentsCreate, ShipmentsDTO, MoreShipmentsDTO
from src.service.shipments_service import ShipmentsService

shipments_router = APIRouter(
    tags=["Shipments"],
    prefix="/shipments",
)


@shipments_router.post("")
async def create_shipment(
    shipment: ShipmentsCreate,
    shipments_service: ShipmentsService = Depends(get_shipments_service),
) -> ShipmentsDTO:
    db_shipment = await shipments_service.add_shipment(shipment)
    return db_shipment


@shipments_router.post("/more")
async def create_more(
    shipments: List[ShipmentsCreate],
    shipments_service: ShipmentsService = Depends(get_shipments_service),
) -> List[ShipmentsDTO]:
    dto_shipments = await shipments_service.add_more(shipments)
    return dto_shipments


@shipments_router.get("")
async def get_shipments(
    shipments_service: ShipmentsService = Depends(get_shipments_service),
) -> MoreShipmentsDTO:
    shipments = await shipments_service.get_more()
    return shipments


@shipments_router.get("/{shipment_id}")
async def get_shipment(
    shipment_id: int,
    shipments_service: ShipmentsService = Depends(get_shipments_service),
) -> ShipmentsDTO:
    shipment = await shipments_service.get_single(id=shipment_id)
    return shipment


@shipments_router.delete("/{shipment_id}")
async def delete_shipment(
    shipment_id: int,
    shipments_service: ShipmentsService = Depends(get_shipments_service),
) -> ShipmentsDTO:
    shipment_delete = await shipments_service.delete_shipment(shipment_id)
    return shipment_delete


@shipments_router.put("/{shipment_id}")
async def update_shipment(
    shipment_id: int,
    shipment: ShipmentsCreate,
    shipments_service: ShipmentsService = Depends(get_shipments_service),
) -> ShipmentsDTO:
    return await shipments_service.update_shipment(shipment_id, shipment)


@shipments_router.patch("/{shipment_id}/status")
async def update_status(
    shipment_id: int,
    status: str,
    shipments_service: ShipmentsService = Depends(get_shipments_service),
) -> ShipmentsDTO:
    updated = await shipments_service.shipments_repo.update({"status": status}, id=shipment_id)
    return ShipmentsDTO.model_validate(updated)
