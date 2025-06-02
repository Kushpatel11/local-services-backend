from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class ProviderAddressCreate(BaseModel):
    city: str
    district: str
    state: str
    country: str
    pincode: str = Field(..., max_length=6)
    latitude: float
    longitude: float
    label: Optional[str] = None


class ServiceProviderCreate(BaseModel):
    name: str
    mobile: str
    email: EmailStr
    experience_years: int
    service_category_id: int
    addresses: List[ProviderAddressCreate]


class ProviderLogin(BaseModel):
    email: EmailStr
    password: str


class ProviderAddressUpdate(BaseModel):
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    pincode: Optional[str] = Field(None, max_length=6)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    label: Optional[str] = None


class ProviderUpdate(BaseModel):
    name: Optional[str] = None
    mobile: Optional[str] = None
    experience_years: Optional[int] = None
    service_category_id: Optional[int] = None
    addresses: Optional[List[ProviderAddressUpdate]] = None


class ProviderAddressOut(BaseModel):
    id: int
    city: str
    district: str
    state: str
    country: str
    pincode: str
    latitude: float
    longitude: float
    label: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ProviderProfileOut(BaseModel):
    id: int
    name: str
    mobile: str
    email: str
    experience_years: int
    service_category_id: int
    is_approved: bool
    created_at: datetime
    updated_at: datetime
    addresses: List[ProviderAddressOut]

    class Config:
        orm_mode = True
