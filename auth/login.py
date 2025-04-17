from pydantic import BaseModel, EmailStr
from base_models import BaseResponse
from database.db_schemas import DBUser
from sqlalchemy.orm import Session
from utility.crypt import verify_password
from utility.transform import to_model

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponseData(BaseModel):
    id: str
    name: str
    email: str

class LoginResponse(BaseResponse[LoginResponseData]):
    pass

async def login(request: LoginRequest, db: Session) -> LoginResponse:
    
    user = db.query(DBUser).filter(DBUser.email == request.email).first()
    
    if user:
        if verify_password(request.password, user.password):
            data = to_model(LoginResponseData, user.__dict__, exclude_fields={"password"})    
            return LoginResponse(
                code=200,
                success=True,
                message=f"Welcome back, {user.name}",
                data=data 
            )
        else:
            return LoginResponse(
                code=400,
                success=False,
                message="Invalid email or password!"
            )
    else:
        return LoginResponse(
            code=404,
            success=False,
            message="User not found!"
        )