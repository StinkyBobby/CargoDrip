from fastapi import APIRouter, Depends
from typing import Annotated
from src.service import auth_service
from src.scheme.auth_scheme import EmployeeLogin, TokenResponse
from src.service.auth_service import AuthService

from src.deps.auth_deps import get_auth_service

auth_router = APIRouter(
    prefix="/auth", 
    tags=["Auth"]
    )

@auth_router.post("/login", response_model=TokenResponse)
async def login(
    credentials: EmployeeLogin,
    auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    token, role, redirect_url = await auth_service.login(credentials)
    return TokenResponse(access_token=token, role=role, redirect_url=redirect_url)

@auth_router.post("/login")
async def login(credentials: EmployeeLogin):
    token, role, redirect_url = await auth_service.login(credentials)
    return {
        "access_token": token,
        "role": role,
        "redirect_url": redirect_url
    }
