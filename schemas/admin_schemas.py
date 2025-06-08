from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class AdminLogin(BaseModel):
    email: EmailStr
    password: str


class ServiceCategoryCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the service category")
    description: Optional[str] = Field(
        None, description="Description of the service category"
    )
    parent_id: Optional[int] = Field(
        None, description="ID of the parent category, if any"
    )
