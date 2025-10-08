from typing import List, Annotated

from fastapi import APIRouter, Query, Depends

from src.deps import Deps
from src.scheme import TruckDTO
from src.scheme.truck_scheme import TruckCreate, TruckDTO, MoreTruckDTO
from src.service.truck_service import TruckService
from src.utils.error import Forbidden

truck_router = APIRouter(
    tags=["Truck"],
    prefix="/trucks",
)


@truck_router.post("")
async def create_truck(
    truck: TruckCreate,
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)],
) -> TruckDTO:
    db_truck = await truck_service.add_truck(truck)
    return db_truck


@truck_router.post("/more")
async def create_more(
    trucks: List[TruckCreate],
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)]
) -> List[TruckDTO]:
    dto_trucks = await truck_service.add_more(trucks)
    return dto_trucks


@truck_router.get("")
async def get_trucks(
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)],
) -> MoreTruckDTO:
    trucks = await truck_service.get_more()
    return trucks


@truck_router.get("/{truck_id}")
async def get_truck(
    truck_id: int, 
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)]
) -> TruckDTO:
    truck = await truck_service.get_single(id=truck_id)
    return truck


@truck_router.delete("")
async def delete_truck(
    truck_id: int,
    truck_service: Annotated[TruckService, Depends(Deps.truck_service)]
) -> TruckDTO:
    truck_delete = await truck_service.delete_truck(truck_id)
    return truck_delete


# @book_router.put("/{id}")
# async def update_book(
#     book_id: int,
#     new_book: BookCreateDTO,
#     book_service: Annotated[BookService, Depends(Deps.book_service)],
# ) -> BookDTO:
#     updated_book = await book_service.update_book(book_id, new_book)
#     return updated_book




# @book_router.post("/requests")
# async def create_request(
#     book_id: int,
#     current_user: Annotated[UserDTO, Depends(OAuth2Utility.get_current_user)],
#     request_service: Annotated[RequestService, Depends(Deps.request_service)]
# ) -> RequestDTO:
#     request = await request_service.create_request(book_id, current_user.id)
#     return request