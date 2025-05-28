from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional


class BookingAddressCreate(BaseModel):
    city: str
    district: str
    state: str
    country: str
    pincode: str = Field(..., max_length=6)
    latitude: float
    longitude: float
    label: Optional[str] = None


class BookingCreate(BaseModel):
    service_id: int
    booking_date: date
    booking_time: time
    address: BookingAddressCreate
