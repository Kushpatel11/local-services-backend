from pydantic import BaseModel, Field
from datetime import date, datetime, time
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
    service_id: int = Field(..., gt=0)
    booking_date: date
    booking_time: time
    address: BookingAddressCreate


class BookingAddressOut(BookingAddressCreate):  # reuse fields ✅
    model_config = {"from_attributes": True}


class BookingOut(BaseModel):
    id: int
    user_id: int
    service_id: int
    booking_date: date
    booking_time: time
    status: str
    created_at: datetime
    updated_at: datetime
    booking_address: Optional[BookingAddressOut]

    model_config = {"from_attributes": True}


class BookingAddressUpdate(BaseModel):
    city: Optional[str]
    district: Optional[str]
    state: Optional[str]
    country: Optional[str]
    pincode: Optional[str] = Field(None, max_length=6)
    latitude: Optional[float]
    longitude: Optional[float]
    label: Optional[str] = None


class BookingUpdate(BaseModel):
    service_id: Optional[int] = Field(None, gt=0)
    booking_date: Optional[date]
    booking_time: Optional[time]
    address: Optional[BookingAddressUpdate]
