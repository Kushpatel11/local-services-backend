# crud/admin.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models import Admin, Booking, ServiceCategory
from utils.hashing import verify_password
from core.database import get_db
from core.security import create_access_token
from sqlalchemy.future import select


def authenticate_admin(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    admin = db.execute(select(Admin).where(Admin.email == form_data.username))
    db_user = admin.scalars().first()
    if not admin or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": db_user.email, "role": "admin"})
    return {"access_token": access_token, "token_type": "bearer"}


def list_all_bookings(current_admin, db):
    bookings = db.query(Booking).all()
    return bookings


def approve_booking(id, db, current_admin):
    booking = db.query(Booking).filter(Booking.id == id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == "approved":
        raise HTTPException(status_code=400, detail="Booking is already approved")

    booking.status = "approved"
    db.commit()
    db.refresh(booking)

    return {"message": "Booking approved successfully", "booking_id": booking.id}


def reject_booking(id, db, current_admin):
    booking = db.query(Booking).filter(Booking.id == id).first()

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.status == "rejected":
        raise HTTPException(status_code=400, detail="Booking is already rejected")

    booking.status = "rejected"
    db.commit()
    db.refresh(booking)

    return {"message": "Booking rejected successfully", "booking_id": booking.id}


def create_service_category(db: Session, category_in):
    # If parent_id is provided, verify it exists
    if category_in.parent_id:
        parent = (
            db.query(ServiceCategory)
            .filter(ServiceCategory.id == category_in.parent_id)
            .first()
        )
        if not parent:
            raise ValueError("Parent category does not exist.")
    category = ServiceCategory(
        name=category_in.name,
        description=category_in.description,
        parent_id=category_in.parent_id,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category
