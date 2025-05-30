# api/routes/admin_auth.py

from typing import List
from fastapi import APIRouter, Depends, status, Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.booking_schemas import BookingOut
from dependencies.admin_dependencies import get_current_admin, oauth2_admin_scheme


from crud.crud_admin import (
    authenticate_admin,
    list_all_bookings,
    approve_booking,
    reject_booking,
)

from core.database import get_db

router = APIRouter()


@router.post("/login", status_code=status.HTTP_200_OK)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    return authenticate_admin(form_data, db)


@router.get(
    "/bookings",
    response_model=List[BookingOut],
    dependencies=[Security(oauth2_admin_scheme)],
)
def get_all_bookings(
    current_admin: dict = Depends(get_current_admin), db: Session = Depends(get_db)
):
    return list_all_bookings(current_admin, db)


@router.post("/bookings/{id}/approve", dependencies=[Security(oauth2_admin_scheme)])
def approve_bookings(
    id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return approve_booking(id, db, current_admin)


@router.post("/bookings/{id}/reject", dependencies=[Security(oauth2_admin_scheme)])
def reject_bookings(
    id: int,
    db: Session = Depends(get_db),
    current_admin: dict = Depends(get_current_admin),
):
    return reject_booking(id, db, current_admin)
