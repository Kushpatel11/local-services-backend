from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from crud.crud_public import search_providers_by_location
from schemas.user_schemas import ServiceProviderOut

router = APIRouter()


@router.get("/providers/by-location", response_model=List[ServiceProviderOut])
def providers_by_location(
    area: Optional[str] = Query(None, description="District/area name (optional)"),
    city: Optional[str] = Query(None, description="City name (optional)"),
    state: Optional[str] = Query(None, description="State name (optional)"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Get approved, not deleted providers filtered by area, city, or state.
    All filters are independent and optional.
    """
    providers = search_providers_by_location(
        db=db,
        area=area,
        city=city,
        state=state,
        limit=limit,
        offset=offset,
    )
    if not providers:
        raise HTTPException(404, "No providers found for the given location.")
    return [ServiceProviderOut.from_orm(p) for p in providers]
