from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.booking_schemas import BookingCreate
from crud.crud_booking import create_booking
from dependencies.user_dependencies import get_current_user
from core.database import get_db
from models import User

router = APIRouter()


@router.post("/create_booking", status_code=status.HTTP_201_CREATED)
def create_bookings(
    booking_in: BookingCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_booking(db, booking_in, user.id)
