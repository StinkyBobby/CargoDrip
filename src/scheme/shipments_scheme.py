from typing import List
from pydantic import BaseModel, Field, field_validator
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

    @field_validator("pickup_date", "delivered_date", mode="after")
    def make_naive(cls, v: datetime) -> datetime:
        if v and v.tzinfo:
            return v.replace(tzinfo=None)
        return v


class ShipmentsDTO(ShipmentsCreate):
    id: int
    
    class Config:
        from_attributes = True


class MoreShipmentsDTO(BaseModel):
    items: List[ShipmentsDTO]
    total: int
    
    class Config:
        from_attributes = True
