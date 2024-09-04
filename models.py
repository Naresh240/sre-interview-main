from typing import Optional
from main import BaseApiModel


class Item(BaseApiModel):
    price: Optional[float] = None
    quantity: int
    description: Optional[str] = None
