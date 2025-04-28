from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str
    mobile: Optional[str] = None
    role: str = "user"
