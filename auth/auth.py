from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from .register import register, RegisterRequest, RegisterResponse
from .login import login, LoginRequest

auth_router = APIRouter()

@auth_router.post("/register")
async def register_endpoint(request: RegisterRequest, db: Session = Depends(get_db)):
    return (await register(request=request, db=db)).dump()

@auth_router.post("/login")
async def login_endpoint(request: LoginRequest, db: Session = Depends(get_db)):
    return (await login(request=request, db=db)).dump()