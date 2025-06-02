from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from crud.crud_provider import register_provider, provider_login, update_profile
from schemas.provider_schemas import (
    ProviderProfileOut,
    ServiceProviderCreate,
    ProviderUpdate,
)
from dependencies.provider_dependencies import (
    get_current_provider,
    oauth2_provider_scheme,
)
from models import ServiceProvider


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_service_provider(
    provider: ServiceProviderCreate, db: Session = Depends(get_db)
):
    return register_provider(db, provider)


@router.post("/login", status_code=status.HTTP_200_OK)
def providers_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    return provider_login(form_data, db)


@router.get(
    "/profile",
    response_model=ProviderProfileOut,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(oauth2_provider_scheme)],
)
def get_profile(
    provider: dict = Depends(get_current_provider), db: Session = Depends(get_db)
):
    db_user = (
        db.query(ServiceProvider)
        .filter(ServiceProvider.email == provider["sub"])
        .first()
    )
    if not db_user:
        raise HTTPException(status_code=404, detail="Provider not found")
    return db_user


@router.put(
    "/profile",
    response_model=ProviderProfileOut,
    dependencies=[Security(oauth2_provider_scheme)],
)
def update_profiles(
    update_data: ProviderUpdate,
    db: Session = Depends(get_db),
    provider: dict = Depends(get_current_provider),
):
    return update_profile(update_data, db, provider)
