from pydantic import BaseModel, Field


class TruckCreate(BaseModel):
    plate_number: str = Field(max_length=100)
    model: str = Field(max_length=100)
    capacity_kg: int
    volume_m3: int 
    is_refrigerated: bool
    available: bool


class TruckDTO(TruckCreate):
    id: int

    class Config:
        from_attributes = True

