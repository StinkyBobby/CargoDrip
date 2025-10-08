from pydantic import BaseModel, Field
from src.models.types import DeliveryStatus
from datetime import datetime


class ShipmentsCreate(BaseModel):
    cargo_id: int
    truck_id: int
    from_location: str
    to_location: str
    pickup_date: datetime
    delivered_date: datetime
    status: DeliveryStatus


class ShipmentsDTO(ShipmentsCreate):
    id: int
    

    class Config:
        from_attributes = True
