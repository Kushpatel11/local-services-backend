from pydantic import BaseModel, EmailStr, HttpUrl
from datetime import date
from typing import Optional, List


class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    mobile: Optional[str] = None
    role: str = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str
    address_line: Optional[str]
    city: Optional[str] = None
    address: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    preferred_language: Optional[str] = "en"
    saved_payment_methods: Optional[List[str]] = []
    notification_preferences: Optional[List[str]] = ["email", "sms"]
    date_of_birth: Optional[date] = None


class AddressUpdate(BaseModel):
    address_line: Optional[str]
    state: Optional[str]
    district: Optional[str]
    country: Optional[str]
    pincode: Optional[str]
    city: Optional[str]
    label: Optional[str]  # address type


class UserProfileUpdate(BaseModel):
    full_name: Optional[str]
    phone_number: Optional[str]
    date_of_birth: Optional[date]
    profile_picture_url: Optional[str]
    preferred_language: Optional[str]
    notification_preferences: Optional[List[str]] = ["email", "sms"]
    addresses: Optional[List[AddressUpdate]]


class ProviderAddressOut(BaseModel):
    city: str
    district: str
    state: str
    country: str
    pincode: str
    latitude: float
    longitude: float
    label: Optional[str]

    model_config = {"from_attributes": True}


class ServiceCategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = {"from_attributes": True}


class ServiceProviderOut(BaseModel):
    id: int
    name: str
    mobile: str
    email: str
    experience_years: int
    category: ServiceCategoryOut
    addresses: List[ProviderAddressOut]

    model_config = {"from_attributes": True}
