from typing import Callable, List

from fastapi import HTTPException
from starlette import status
from src.repositories.base_repo import AbstractRepo
from src.schemas.book import BookDTO, BookCreateDTO


class TruckService():