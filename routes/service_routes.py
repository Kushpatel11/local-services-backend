from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from schemas.service_schemas import ServiceCreate, ServiceOut
from core.database import get_db
from dependencies.provider_dependencies import (
    get_current_provider,
    oauth2_provider_scheme,
)
from crud.crud_service import create_service

router = APIRouter()


@router.post(
    "/add_services",
    response_model=ServiceOut,
    status_code=status.HTTP_201_CREATED,
    summary="Provider creates a new service",
    dependencies=[Security(oauth2_provider_scheme)],
)
def add_service(
    service_in: ServiceCreate,
    db: Session = Depends(get_db),
    provider: dict = Depends(get_current_provider),
):
    """
    Authorized provider can create a new service (offering/job) under their profile.
    """
    try:
        return create_service(db=db, provider=provider, service_in=service_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
