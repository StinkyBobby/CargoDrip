from typing import List
from fastapi import HTTPException
from starlette import status
from src.repositories.base_repo import AbstractRepo
from src.scheme.cargo_scheme import CargoDTO, CargoCreate, MoreCargoDTO


class CargoService():
    def __init__(self, cargo_repo: AbstractRepo):
        self.cargo_repo = cargo_repo 
        
    async def get_single(self, **filters) -> CargoDTO:
        cargo = await self.cargo_repo.find(**filters)
        if cargo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="cargo is not found"
            )

        return CargoDTO.model_validate(cargo)
    
    async def get_more(self, limit: int = 100, offset: int = 0, order_by: str = "",**filters) -> MoreCargoDTO:
        cargo = await self.cargo_repo.find_all(limit=limit, offset=offset, **filters)
        
        cargo_dto = [CargoDTO.model_validate(row) for row in cargo]
        return MoreCargoDTO(items=cargo_dto, total=0)
    
    async def add_cargo(self, cargo: CargoCreate) -> CargoDTO:
        cargo_dict = cargo.model_dump()
        cargo = await self.cargo_repo.create(cargo_dict)
        
        return CargoDTO.model_validate(cargo)
    
    async def add_more(self, cargo: List[CargoCreate]) -> List[CargoDTO]:
        cargo_dict = [row.model_dump() for row in cargo]
        db_cargo = await self.cargo_repo.create_more(cargo_dict)
        
        list_cargo_dto = [CargoDTO.model_validate(row) for row in db_cargo]
        return list_cargo_dto
    
    async def update_cargo(self, cargo_id: int, cargo: CargoCreate) -> CargoDTO:
        db_cargo = await self.cargo_repo.find(id=cargo_id)
        if db_cargo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cargo is not found"
            )
            
        updated = await self.cargo_repo.update(cargo.model_dump(), id=cargo_id)
        return CargoDTO.model_validate(updated)
    
    async def delete_cargo(self, cargo_id: int) -> CargoDTO:
        cargo = await self.cargo_repo.delete(id=cargo_id)
        if cargo is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Cargo is not found"
            )
            
        return CargoDTO.model_validate(cargo) 
