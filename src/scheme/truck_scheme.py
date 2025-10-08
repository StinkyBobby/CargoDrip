from pydantic import BaseModel, Field

from typing import List

class TruckCreate(BaseModel):
    plate_number: str = Field(max_length=100)
    model: str = Field(max_length=100)
    capacity_kg: int
    volume_m3: int 
    available: bool


class TruckDTO(TruckCreate):
    id: int

    class Config:
        from_attributes = True

class MoreTruckDTO(BaseModel):
    items: List[TruckDTO] 
    total: int
    class Config:
        from_attributes = True
