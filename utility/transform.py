from pydantic import BaseModel
from typing import Type, TypeVar

T = TypeVar("T", bound=BaseModel)

def to_model(model_cls: Type[T], source_obj: BaseModel | dict, exclude_fields: set[str] = None) -> T:
    if isinstance(source_obj, BaseModel):
        source_obj = source_obj.model_dump()
    exclude_fields = exclude_fields or set()
    filtered_data = {k: v for k, v in source_obj.items() if k not in exclude_fields}
    return model_cls(**filtered_data)
