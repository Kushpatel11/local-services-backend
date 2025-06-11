from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ServiceRatingCreate(BaseModel):
    booking_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ServiceRatingOut(BaseModel):
    id: int
    service_id: int
    user_id: int
    booking_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
