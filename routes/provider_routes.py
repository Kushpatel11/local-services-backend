from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from core.database import get_db
from crud.crud_provider import (
    register_provider,
    provider_login,
    update_profile,
    delete_own_profile,
)
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
from typing import List
from schemas.booking_schemas import BookingOut
from crud.crud_booking import get_provider_bookings, provider_update_booking_status


router = APIRouter()


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ProviderProfileOut,
    summary="Register as a new service provider",
)
def register_service_provider(
    provider: ServiceProviderCreate, db: Session = Depends(get_db)
):
    """
    Register a new service provider.
    """
    return register_provider(db, provider)


@router.post("/login", status_code=status.HTTP_200_OK, summary="Provider login")
def providers_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Log in a service provider and return a JWT token.
    """
    return provider_login(form_data, db)


@router.get(
    "/profile",
    response_model=ProviderProfileOut,
    status_code=status.HTTP_200_OK,
    summary="Get current provider profile",
    dependencies=[Security(oauth2_provider_scheme)],
)
def get_profile(
    provider: dict = Depends(get_current_provider), db: Session = Depends(get_db)
):
    """
    Get the profile of the currently authenticated provider.
    """
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
    summary="Update current provider profile",
    dependencies=[Security(oauth2_provider_scheme)],
)
def update_profiles(
    update_data: ProviderUpdate,
    db: Session = Depends(get_db),
    provider: dict = Depends(get_current_provider),
):
    """
    Update the profile of the currently authenticated provider.
    """
    return update_profile(update_data, db, provider)


@router.delete(
    "/profile",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete current provider account",
    dependencies=[Security(oauth2_provider_scheme)],
)
def delete_profile(
    db: Session = Depends(get_db), provider: dict = Depends(get_current_provider)
):
    """
    Soft-delete the currently authenticated provider account.
    """
    return delete_own_profile(db, provider)


@router.get("/my_bookings", response_model=List[BookingOut])
def list_my_bookings(
    db: Session = Depends(get_db), provider: dict = Depends(get_current_provider)
):
    db_user = (
        db.query(ServiceProvider)
        .filter(ServiceProvider.email == provider["sub"])
        .first()
    )
    bookings = get_provider_bookings(db, provider_id=db_user.id)
    return bookings


@router.patch("/{booking_id}/status", response_model=BookingOut)
def update_booking_status(
    booking_id: int,
    status: str,
    db: Session = Depends(get_db),
    provider: dict = Depends(get_current_provider),
):
    # Example: status='completed'
    db_user = (
        db.query(ServiceProvider)
        .filter(ServiceProvider.email == provider["sub"])
        .first()
    )
    booking = provider_update_booking_status(
        db, provider_id=db_user.id, booking_id=booking_id, new_status=status
    )
    return booking
