from typing import List
from fastapi import APIRouter, Query, Depends

from src.scheme.cargo_scheme import CargoCreate, CargoDTO, MoreCargoDTO
from src.service.cargo_service import CargoService

from src.deps.cargo_deps import get_cargo_service



cargo_router = APIRouter(
    tags=["Cargo"],
    prefix="/cargoes",
)

@cargo_router.post("", response_model=CargoDTO)
async def create_cargo(
    cargo: CargoCreate,
    cargo_service: CargoService = Depends(get_cargo_service)
) -> CargoDTO:
    db_cargo = await cargo_service.add_cargo(cargo)
    return db_cargo

@cargo_router.post("/more", response_model=List[CargoDTO])
async def create_more(
    cargoes: List[CargoCreate],
    cargo_service: CargoService = Depends(get_cargo_service)

) -> List[CargoDTO]:
    dto_cargoes = await cargo_service.add_more(cargoes)
    return dto_cargoes

@cargo_router.get("", response_model=MoreCargoDTO)
async def get_cargoes(
    cargo_service: CargoService = Depends(get_cargo_service),
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    order_by: str = ""
) -> MoreCargoDTO:
    cargoes = await cargo_service.get_more(limit=limit, offset=offset, order_by=order_by)
    return cargoes

@cargo_router.get("/{cargo_id}", response_model=CargoDTO)
async def get_cargo(
    cargo_id: int,
    cargo_service: CargoService = Depends(get_cargo_service)

) -> CargoDTO:
    cargo = await cargo_service.get_single(id=cargo_id)
    return cargo

@cargo_router.delete("/{cargo_id}", response_model=CargoDTO)
async def delete_cargo(
    cargo_id: int,
    cargo_service: CargoService = Depends(get_cargo_service)

) -> CargoDTO:
    cargo_delete = await cargo_service.delete_cargo(cargo_id)
    return cargo_delete

@cargo_router.put("/{cargo_id}", response_model=CargoDTO)
async def update_cargo(
    cargo_id: int,
    cargo: CargoCreate,
    cargo_service: CargoService = Depends(get_cargo_service)
) -> CargoDTO:
    return await cargo_service.update_cargo(cargo_id, cargo)
