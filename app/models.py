from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class Item(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: date


class ClockIn(BaseModel):
    email: EmailStr
    location: str


