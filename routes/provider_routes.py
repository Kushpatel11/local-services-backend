from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from crud.crud_provider import get_approved_providers, get_provider_by_id
from schemas.provider_schemas import ServiceProviderOut
from typing import List

router = APIRouter()


@router.get("/providers", response_model=List[ServiceProviderOut])
def list_service_providers(db: Session = Depends(get_db)):
    return get_approved_providers(db)


@router.get("/providers/{provider_id}", response_model=ServiceProviderOut)
def get_service_provider(provider_id: int, db: Session = Depends(get_db)):
    return get_provider_by_id(db, provider_id)
