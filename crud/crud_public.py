from sqlalchemy.orm import Session, joinedload
from typing import Optional
from datetime import datetime
import math

from models import ServiceProvider, ProviderAddress, ServiceCategory


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def search_providers_logic(
    db: Session,
    city: Optional[str] = None,
    state: Optional[str] = None,
    area: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    sort: Optional[str] = None,
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    distance: Optional[float] = None,
    rating: Optional[float] = None,
    experience_years: Optional[int] = None,
    available_at: Optional[datetime] = None,
    is_approved: Optional[bool] = None,
    is_deleted: Optional[bool] = None,
    limit: int = 20,
    offset: int = 0,
):
    query = (
        db.query(ServiceProvider)
        .join(ServiceProvider.addresses)
        .join(ServiceProvider.category)
        .options(
            joinedload(ServiceProvider.addresses), joinedload(ServiceProvider.category)
        )
    )

    # Dynamic filters
    if city:
        query = query.filter(ProviderAddress.city.ilike(f"%{city}%"))
    if state:
        query = query.filter(ProviderAddress.state.ilike(f"%{state}%"))
    if area:
        query = query.filter(ProviderAddress.district.ilike(f"%{area}%"))
    if category:
        query = query.filter(ServiceCategory.name.ilike(f"%{category}%"))
    if experience_years is not None:
        query = query.filter(ServiceProvider.experience_years >= experience_years)

    # Add available_at logic if needed

    providers = query.all()

    # Location-based filtering
    if lat is not None and lon is not None and distance is not None:
        filtered = []
        for p in providers:
            for addr in p.addresses:
                dist = haversine(lat, lon, addr.latitude, addr.longitude)
                if dist <= distance:
                    p._distance = dist
                    filtered.append(p)
                    break
        providers = filtered

    # Sorting
    if sort == "price_asc":
        providers.sort(key=lambda p: getattr(p, "min_price", 0))
    elif sort == "price_desc":
        providers.sort(key=lambda p: getattr(p, "max_price", 0), reverse=True)
    elif sort == "distance" and lat is not None and lon is not None:
        providers.sort(key=lambda p: getattr(p, "_distance", float("inf")))
    elif sort == "rating":
        providers.sort(key=lambda p: getattr(p, "rating", 0), reverse=True)
    elif sort == "experience":
        providers.sort(key=lambda p: getattr(p, "experience_years", 0), reverse=True)

    # Pagination
    providers = providers[offset : offset + limit]
    return providers
