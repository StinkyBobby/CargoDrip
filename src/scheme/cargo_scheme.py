from pydantic import BaseModel, Field


class CargoCreate(BaseModel):
    sender: str = Field(max_length=100)
    weight: int
    volume: int

class CargoDTO(CargoCreate):
    id: int

    class Config:
        from_attributes = True
