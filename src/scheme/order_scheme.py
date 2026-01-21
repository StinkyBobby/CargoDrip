from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from src.models.order import OrderStatus

class OrderCreate(BaseModel):
    cargo_id: int
    to_location: str = Field(max_length=255)
    distance_km: int = Field(ge=1)

class OrderDTO(OrderCreate):
    id: int
    status: OrderStatus
    truck_id: int | None
    created_at: datetime

    price: float
    estimated_days: int

    class Config:
        from_attributes = True


class MoreOrdersDTO(BaseModel):
    items: List[OrderDTO]
    total: int

    class Config:
        from_attributes = True
