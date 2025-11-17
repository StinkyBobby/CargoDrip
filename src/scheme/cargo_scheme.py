from pydantic import BaseModel, Field
from typing import List

class CargoCreate(BaseModel):
    sender: str = Field(max_length=100)
    recipient: str = Field(max_length=100)
    weight: int
    volume: int
    title: str = Field(max_length=500)

class CargoDTO(CargoCreate):
    id: int

    class Config:
        from_attributes = True

class MoreCargoDTO(BaseModel):
    items: List[CargoDTO] 
    total: int
    class Config:
        from_attributes = True