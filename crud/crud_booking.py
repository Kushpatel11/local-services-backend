# crud/booking.py

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from models import Booking, BookingAddress, User
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


def get_booking_by_id(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()


def update_booking(
    id,
    booking_update,
    db,
    user_payload,
):
    if "sub" not in user_payload:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(User).filter(User.email == user_payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this booking"
        )

    # Main booking fields
    update_data = booking_update.dict(exclude_unset=True)
    address_data = update_data.pop("address", None)

    for key, value in update_data.items():
        setattr(booking, key, value)

    # Address update (nested)
    if address_data:
        if booking.booking_address:
            for key, value in address_data.items():
                setattr(booking.booking_address, key, value)
        else:
            # Create a new address if not exists
            new_address = BookingAddress(**address_data, booking_id=booking.id)
            db.add(new_address)

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


def cancel_booking(id, db, current_user):

    user = db.query(User).filter(User.email == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    booking = db.query(Booking).filter(Booking.id == id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to cancel this booking"
        )

    # db.delete(booking)
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)

    return booking
