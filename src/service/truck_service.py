from typing import Callable, List

from fastapi import HTTPException
from starlette import status
from src.repositories.base_repo import AbstractRepo
from src.scheme.truck_scheme import MoreTruckDTO, TruckDTO, TruckCreate


class TruckService():
    def __init__(self, truck_repo: Callable[[], AbstractRepo]):
        self.truck_repo: AbstractRepo = truck_repo()
    
    async def get_single(self, **filters) -> TruckDTO:
        truck = await self.truck_repo.find(**filters)
        if truck is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="truck is not found"
            )
        
        return TruckDTO.model_validate(truck)
    
    async def get_more(self, limit: int = 100, offset: int = 0, order_by: str = "", **filters) -> List[TruckDTO]:
        truck = await self.truck_repo.find_all(limit=limit, offset=offset, **filters)
        
        truck_dto = [TruckDTO.model_validate(row) for row in truck]
        return MoreTruckDTO(items=truck_dto, total=0)
    
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
    
    async def set_availability(self, truck_id : int, available: bool) -> TruckDTO:
        truck = await self.truck_repo.find(id=truck_id)
        
        if truck is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Truck is not found"
            )
            
        updated = await self.truck_repo.update({"available": available}, id=truck_id)
        return TruckDTO.model_validate(updated)