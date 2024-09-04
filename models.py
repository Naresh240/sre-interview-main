from pydantic import BaseModel
from typing import Optional

class BaseApiModel(BaseModel):
    name: str

class Item(BaseApiModel):
    price: Optional[float] = None
    quantity: int
    description: Optional[str] = None
