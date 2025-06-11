from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Booking, BookingStatus, ServiceRating


def create_rating(db: Session, user_id: int, data):
    # Only allow if booking is completed and belongs to user, and no rating exists yet
    booking = db.query(Booking).filter(Booking.id == data.booking_id).first()
    print(booking)
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.user_id != user_id:
        raise HTTPException(403, "Not your booking")
    if booking.status != BookingStatus.completed:

        raise HTTPException(400, "Can only review completed bookings")
    if booking.rating:
        raise HTTPException(400, "Already rated")
    rating = ServiceRating(
        service_id=booking.service_id,
        user_id=user_id,
        booking_id=booking.id,
        rating=data.rating,
        comment=data.comment,
    )
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


def get_service_reviews(db: Session, service_id: int):
    return db.query(ServiceRating).filter(ServiceRating.service_id == service_id).all()
