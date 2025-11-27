from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    id: Optional[str] = None
    book_id: str
    quantity: int
    date: datetime
