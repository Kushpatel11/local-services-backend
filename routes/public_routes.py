from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime

from core.database import get_db
from models import ServiceProvider, ProviderAddress, ServiceCategory
from schemas.user_schemas import ServiceProviderOut
from dependencies.user_dependencies import get_current_user

import math

router = APIRouter()


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


@router.get("/search/providers", response_model=List[ServiceProviderOut])
def search_providers(
    city: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    area: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    sort: Optional[str] = Query(
        None, description="Sort by: price_asc, price_desc, distance, rating, experience"
    ),
    lat: Optional[float] = Query(None),
    lon: Optional[float] = Query(None),
    distance: Optional[float] = Query(None, description="Distance in km for 'near me'"),
    rating: Optional[float] = Query(None),
    experience_years: Optional[int] = Query(None),
    available_at: Optional[datetime] = Query(None),
    is_approved: Optional[bool] = Query(None),  # For admin use
    is_deleted: Optional[bool] = Query(None),  # For admin use
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Unified provider search endpoint with advanced filtering and role-aware access.
    """
    query = (
        db.query(ServiceProvider)
        .join(ServiceProvider.addresses)
        .join(ServiceProvider.category)
        .options(
            joinedload(ServiceProvider.addresses), joinedload(ServiceProvider.category)
        )
    )

    # Role-based filtering
    if current_user.role == "user":
        query = query.filter(
            ServiceProvider.is_approved == True, ServiceProvider.is_deleted == False
        )
    elif current_user.role == "provider":
        query = query.filter(ServiceProvider.id == current_user.id)
    elif current_user.role == "admin":
        # Allow admin to override is_approved/is_deleted filters
        if is_approved is not None:
            query = query.filter(ServiceProvider.is_approved == is_approved)
        if is_deleted is not None:
            query = query.filter(ServiceProvider.is_deleted == is_deleted)

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
    if rating is not None:
        query = query.filter(
            ServiceProvider.rating >= rating
        )  # Assuming you have a 'rating' column
    if min_price is not None or max_price is not None:
        # You may need to join with a Service/Price model if price is not on provider
        query = query.filter(
            and_(
                (
                    ServiceProvider.min_price >= min_price
                    if min_price is not None
                    else True
                ),
                (
                    ServiceProvider.max_price <= max_price
                    if max_price is not None
                    else True
                ),
            )
        )
    # Add available_at logic if you have a booking/availability model to query

    # Fetch results for location filtering (if needed)
    providers = query.all()

    # Location-based filtering (in Python for demonstration; use DB for large datasets)
    if lat is not None and lon is not None and distance is not None:
        filtered = []
        for p in providers:
            for addr in p.addresses:
                dist = haversine(lat, lon, addr.latitude, addr.longitude)
                if dist <= distance:
                    p._distance = dist
                    filtered.append(p)
                    break  # Only need one address within range
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

    # Output serialization (replace with ProviderOut schema as needed)
    return [ServiceProviderOut.from_orm(p) for p in providers]
