from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class ParcelCreate(BaseModel):
    name: str
    weight: Decimal = Field(..., gt=0)
    type_id: int
    declared_value_usd: Decimal = Field(..., ge=0)

class ParcelOut(BaseModel):
    id: str
    name: str
    weight: Decimal
    declared_value_usd: Decimal
    type_name: str
    delivery_cost_rub: Optional[Decimal | str]

    class Config:
        orm_mode = True

class ParcelTypeCreate(BaseModel):
    name: str

class ParcelTypeOut(BaseModel):
    id: int
    name: str