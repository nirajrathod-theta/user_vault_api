from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

Data = TypeVar('Data')

class BaseResponse(BaseModel, Generic[Data]):
    code: int
    success: bool
    message: str
    data: Optional[Data] = None

    def dump(self) -> JSONResponse:
        return JSONResponse(
            status_code=self.code,
            content=self.model_dump()
        )