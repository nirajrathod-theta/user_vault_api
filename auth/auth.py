from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from .register import register, RegisterRequest

auth_router = APIRouter()

@auth_router.post("/register")
async def register_endpoint(request: RegisterRequest, db: Session = Depends(get_db)):
    return (await register(request=request, db=db)).dump()