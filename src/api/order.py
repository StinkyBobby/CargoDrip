from fastapi import APIRouter, Depends, HTTPException, status


from src.deps.order_deps import get_order_service
from src.scheme.order_scheme import OrderCreate, OrderDTO, MoreOrdersDTO
from src.service.order_service import OrderService

order_router = APIRouter(
    tags=["Orders"],
    prefix="/orders",
)

@order_router.post("", response_model=OrderDTO)
async def create_order(
    order: OrderCreate,
    order_service: OrderService = Depends(get_order_service),
) -> OrderDTO:
    return await order_service.create_order(order)


@order_router.get("/queue", response_model=MoreOrdersDTO)
async def get_queue(
    order_service: OrderService = Depends(get_order_service),
) -> MoreOrdersDTO:
    return await order_service.get_queue()


@order_router.get("", response_model=MoreOrdersDTO)
async def get_orders(
    order_service: OrderService = Depends(get_order_service),
) -> MoreOrdersDTO:
    return await order_service.get_all()


@order_router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    order_service: OrderService = Depends(get_order_service),
):
    await order_service.delete_order(order_id)
    return None
