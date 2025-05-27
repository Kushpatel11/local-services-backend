from pydantic import BaseModel, EmailStr, HttpUrl, constr
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
    phone_number: str  # for Indian numbers
    city: Optional[str] = None
    address: Optional[str] = None
    profile_picture_url: Optional[HttpUrl] = None
    preferred_language: Optional[str] = "en"
    saved_payment_methods: Optional[List[str]] = (
        []
    )  # or custom type if storing more detail
    notification_preferences: Optional[List[str]] = ["email", "sms"]  # or Enum
    date_of_birth: Optional[date] = None
