from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.user_schemas import ServiceProviderOut
from dependencies.user_dependencies import get_current_user

from crud.crud_public import search_providers_logic

router = APIRouter()


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
    is_approved: Optional[bool] = Query(None),
    is_deleted: Optional[bool] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    providers = search_providers_logic(
        db=db,
        current_user=current_user,
        city=city,
        state=state,
        area=area,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort=sort,
        lat=lat,
        lon=lon,
        distance=distance,
        rating=rating,
        experience_years=experience_years,
        available_at=available_at,
        is_approved=is_approved,
        is_deleted=is_deleted,
        limit=limit,
        offset=offset,
    )
    return [ServiceProviderOut.from_orm(p) for p in providers]
