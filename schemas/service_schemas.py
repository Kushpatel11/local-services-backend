from pydantic import BaseModel
from typing import Optional


class ServiceCreate(BaseModel):
    title: str
    service_category_id: int
    description: Optional[str]
    min_price: Optional[float]
    max_price: Optional[float]
    available: Optional[bool] = True


class ServiceOut(ServiceCreate):
    id: int
    provider_id: int

    class Config:
        from_attributes = True  # For Pydantic v2; use orm_mode = True for v1
