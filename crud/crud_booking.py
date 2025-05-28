# crud/booking.py

from sqlalchemy.orm import Session
from models import Booking, BookingAddress
from schemas.booking_schemas import BookingCreate


def create_booking(db: Session, booking_data: BookingCreate, user_id: int):
    # Create main booking
    new_booking = Booking(
        user_id=user_id,
        service_id=booking_data.service_id,
        booking_date=booking_data.booking_date,
        booking_time=booking_data.booking_time,
        status="pending",
    )
    db.add(new_booking)
    db.flush()  # ensures new_booking.id is available

    # Create associated address
    address = BookingAddress(
        booking_id=new_booking.id,
        city=booking_data.address.city,
        district=booking_data.address.district,
        state=booking_data.address.state,
        country=booking_data.address.country,
        pincode=booking_data.address.pincode,
        latitude=booking_data.address.latitude,
        longitude=booking_data.address.longitude,
        label=booking_data.address.label,
    )
    db.add(address)
    db.commit()
    db.refresh(new_booking)
    return new_booking
