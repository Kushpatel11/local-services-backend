from typing import List, Optional
from pydantic import BaseModel


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
