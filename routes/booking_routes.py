from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from crud.crud_booking import (
    create_booking,
    get_booking_by_id,
    update_booking,
    cancel_booking,
)
from dependencies.user_dependencies import get_current_user
from core.database import get_db
from models import User, Service, Booking
from schemas.booking_schemas import BookingCreate, BookingOut, BookingUpdate

router = APIRouter()


@router.post(
    "/bookings",
    response_model=BookingOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new booking",
)
def create_booking_endpoint(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new service booking for the current user.
    """
    # Validate service existence
    service = db.query(Service).filter(Service.id == booking_in.service_id).first()
    if not service:
        raise HTTPException(status_code=400, detail="Invalid service ID")
    # Get user object
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_booking(db, booking_in, user.id)


@router.get(
    "/bookings",
    response_model=List[BookingOut],
    summary="List all bookings for the current user",
)
def list_bookings(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Records to skip (for pagination)"),
    limit: int = Query(10, ge=1, le=50, description="Records per page (max 50)"),
    status: Optional[str] = Query(None, description="Filter by booking status"),
):
    """
    Paginated list of bookings for the current user. Optional filter by status.
    """
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    query = db.query(Booking).filter(Booking.user_id == user.id)
    if status:
        query = query.filter(Booking.status == status)
    bookings = query.order_by(Booking.created_at.desc()).offset(skip).limit(limit).all()
    return bookings


@router.get(
    "/bookings/{id}",
    response_model=BookingOut,
    summary="Get booking details by ID",
)
def get_booking(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieve booking details by booking ID. Only for the current user.
    """
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    booking = get_booking_by_id(db, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if booking.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to view this booking"
        )
    return booking


@router.put(
    "/bookings/{id}",
    response_model=BookingOut,
    summary="Update a booking",
)
def update_booking_endpoint(
    id: int,
    booking_update: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update a booking (date, address, etc.). Only for the current user.
    """
    # You should check inside update_booking for ownership and valid status to update.
    return update_booking(id, booking_update, db, current_user)


@router.delete(
    "/bookings/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel a booking",
)
def cancel_booking_endpoint(
    id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Cancel a booking by ID. Only for the current user.
    Will fail if booking is already cancelled or completed.
    """
    booking = get_booking_by_id(db, id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    if (
        booking.user_id
        != db.query(User).filter(User.email == current_user["sub"]).first().id
    ):
        raise HTTPException(
            status_code=403, detail="Not authorized to cancel this booking"
        )
    if booking.status in ("cancelled", "completed"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot cancel a booking that is already {booking.status}",
        )
    cancel_booking(id, db, current_user)
    return None  # 204 No Content
