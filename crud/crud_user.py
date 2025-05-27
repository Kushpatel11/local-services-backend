from fastapi import Depends, HTTPException, Response
from datetime import datetime

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.future import select
from schemas.user_schemas import (
    UserCreate,
    UserProfile,
)  # Make sure these schemas exist in your code
from models import (
    User,
    UserOtherDetails,
    UserAddress,
)  # Ensure the User model is defined with the correct fields
from core.database import get_db
from core.security import create_access_token
from utils.hashing import hash_password, verify_password
from dependencies.user_dependencies import get_current_user


def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    existing_user = db.execute(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)

    db_user = User(
        fullname=user.fullname,
        email=user.email,
        hashed_password=hashed_password,
        mobile=user.mobile,
        role="user",  # Or another default role based on your system
        created_at=datetime.utcnow(),  # Use UTC time for consistency
        updated_at=datetime.utcnow(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    result = db.execute(select(User).where(User.email == form_data.username))
    db_user = result.scalars().first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}


def user_profile(
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    db_user = (
        db.query(User)
        .filter(User.email == user["sub"])
        .options(joinedload(User.other_details), joinedload(User.user_addresses))
        .first()
    )

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    other = db_user.other_details
    address = db_user.user_addresses[0] if db_user.user_addresses else None

    return {
        "full_name": db_user.fullname,
        "email": db_user.email,
        "phone_number": db_user.mobile,
        "city": address.city if address else None,
        "address": (
            {
                "state": address.state,
                "country": address.country,
                "pincode": address.pincode,
            }
            if address
            else None
        ),
        "profile_picture_url": other.profile_picture_url if other else None,
        "preferred_language": other.preferred_language if other else None,
        "notification_preferences": other.notification_preferences if other else None,
        "date_of_birth": other.date_of_birth if other else None,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at,
    }
