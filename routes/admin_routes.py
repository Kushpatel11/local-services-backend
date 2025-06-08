from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Security, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.booking_schemas import BookingOut
from dependencies.admin_dependencies import get_current_admin, oauth2_admin_scheme
from models import ServiceProvider
from crud.crud_admin import (
    authenticate_admin,
    list_all_bookings,
    approve_booking,
    reject_booking,
    create_service_category,
)
from core.database import get_db
from schemas.admin_schemas import ServiceCategoryCreate

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK, summary="Admin login")
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Log in as an admin and receive a JWT token.
    """
    return authenticate_admin(form_data, db)


@router.get(
    "/bookings",
    response_model=List[BookingOut],
    summary="List all bookings (paginated)",
    dependencies=[Security(oauth2_admin_scheme)],
)
def get_all_bookings(
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
    skip: int = Query(0, ge=0, description="Records to skip (for pagination)"),
    limit: int = Query(10, ge=1, le=50, description="Records per page (max 50)"),
    status: str = Query(None, description="Filter by booking status"),
):
    """
    List all bookings in the system with optional pagination and status filter.
    """
    return list_all_bookings(current_admin, db, skip=skip, limit=limit, status=status)


@router.post(
    "/bookings/{id}/approve",
    summary="Approve a booking",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(oauth2_admin_scheme)],
)
def approve_bookings(
    id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    """
    Approve a pending booking by ID.
    """
    return approve_booking(id, db, current_admin)


@router.post(
    "/bookings/{id}/reject",
    summary="Reject a booking",
    status_code=status.HTTP_200_OK,
    dependencies=[Security(oauth2_admin_scheme)],
)
def reject_bookings(
    id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    """
    Reject a pending booking by ID.
    """
    return reject_booking(id, db, current_admin)


@router.post("/{id}/approve", status_code=200, summary="Approve a provider")
def approve_provider(
    id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    """
    Approve a service provider by ID.
    """
    provider = db.query(ServiceProvider).filter(ServiceProvider.id == id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    provider.is_approved = True
    db.commit()
    return {"detail": "Provider approved"}


@router.post("/{id}/reject", status_code=200, summary="Reject and delete a provider")
def reject_provider(
    id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    """
    Reject (delete) a service provider by ID.
    """
    provider = db.query(ServiceProvider).filter(ServiceProvider.id == id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    db.delete(provider)
    db.commit()
    return {"detail": "Provider rejected and deleted"}


@router.delete(
    "/{id}/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete a provider",
)
def delete_provider(
    id: int, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    """
    Soft-delete a service provider by ID (mark as deleted and unapproved).
    """
    provider = (
        db.query(ServiceProvider)
        .filter(
            ServiceProvider.id == id, ServiceProvider.is_deleted == False  # noqa: E712
        )  # noqa: E712
        .first()
    )
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    provider.is_deleted = True
    provider.is_approved = False
    provider.deleted_at = datetime.utcnow()
    db.commit()
    return None


@router.post(
    "/service-categories",
    response_model=ServiceCategoryCreate,
    status_code=status.HTTP_201_CREATED,
    summary="Add a new service category",
    dependencies=[Depends(oauth2_admin_scheme)],
)
def add_service_category(
    category_in: ServiceCategoryCreate,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    """
    Add a new service category (optionally nested under another category).
    """
    try:
        category = create_service_category(db, category_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return category
