from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud.crud_booking import (
    create_booking,
    get_booking_by_id,
    update_booking,
    cancel_booking,
)
from dependencies.user_dependencies import get_current_user
from core.database import get_db
from models import User, Service
from schemas.booking_schemas import BookingCreate, BookingOut, BookingUpdate

router = APIRouter()


@router.post("/create_booking", status_code=status.HTTP_201_CREATED)
def create_bookings(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = db.query(Service).filter(Service.id == booking_in.service_id).first()
    if not service:
        raise HTTPException(status_code=400, detail="Invalid service ID")
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_booking(db, booking_in, user.id)


@router.get("/bookings/{id}", response_model=BookingOut)
def get_booking(
    id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if "sub" not in user:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.email == user["sub"]).first()
    booking = get_booking_by_id(db, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this booking"
        )
    return booking


@router.put("/bookings/{id}", response_model=BookingOut)
def update_bookings(
    id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    user_payload: dict = Depends(get_current_user),
):
    return update_booking(id, booking_update, db, user_payload)


@router.delete("/bookings/{id}", response_model=BookingOut)
def cancel_bookings(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    return cancel_booking(id, db, current_user)
