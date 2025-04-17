from fastapi import Depends, HTTPException
from uuid import uuid4
from pydantic import BaseModel, EmailStr
from base_models import BaseResponse
from database.db_schemas import DBUser
from sqlalchemy.orm import Session
from utility.crypt import hash_password
from utility.transform import to_model

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

class RegisterResponseData(BaseModel):
    id: str
    name: str
    email: str

class RegisterResponse(BaseResponse[RegisterResponseData]):
    pass

async def register(request: RegisterRequest, db: Session) -> RegisterResponse:
    
    existing_user = db.query(DBUser).filter(DBUser.email == request.email).first()
    if existing_user:
        return RegisterResponse(
            code=400,
            success=False,
            message="Email already registered.",
        )

    user_id = str(uuid4())
    user_dict = request.model_dump()
    user_dict.update({
        "id": user_id,
        "password": hash_password(request.password)
    })

    new_user = DBUser(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    data = to_model(RegisterResponseData, new_user.__dict__, exclude_fields={"password"})    
    response = RegisterResponse(code=201, success=True, message=f"Welcome {request.name}!", data=data)
    
    return response