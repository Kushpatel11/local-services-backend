from typing import List
from fastapi import Depends, HTTPException, Response, status
from datetime import datetime

from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.future import select
from schemas.user_schemas import (
    UserCreate,
    UserProfileUpdate,
)
from models import (
    ServiceProvider,
    User,
    UserOtherDetails,
    UserAddress,
)
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
    access_token = create_access_token(data={"sub": db_user.email, "role": "user"})
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
        "address": (
            {
                "address_line": address.address_line if address else None,
                "city": address.city if address else None,
                "state": address.state if address else None,
                "country": address.country if address else None,
                "pincode": address.pincode if address else None,
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


def update_user_profile(
    payload: UserProfileUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    if "sub" not in user:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.email == user["sub"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.full_name is not None:
        user.fullname = payload.full_name
    if payload.phone_number is not None:
        user.mobile = payload.phone_number

    # Update multiple addresses if provided
    if payload.addresses:
        db.query(UserAddress).filter(UserAddress.user_id == user.id).delete()
        db.flush()
        for addr_payload in payload.addresses:
            new_address = UserAddress(
                user_id=user.id,
                address_line=addr_payload.address_line,
                city=addr_payload.city if addr_payload.city is not None else None,
                district=(
                    addr_payload.district if addr_payload.district is not None else None
                ),
                state=addr_payload.state if addr_payload.state is not None else None,
                country=(
                    addr_payload.country if addr_payload.country is not None else None
                ),
                pincode=(
                    addr_payload.pincode if addr_payload.pincode is not None else None
                ),
                label=addr_payload.label or "",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
            )
            user.user_addresses.append(new_address)
            db.add(new_address)

    # Update other profile details
    other = user.other_details
    if other is None:
        other = UserOtherDetails(user_id=user.id)
        db.add(other)

    if payload.profile_picture_url is not None:
        other.profile_picture_url = payload.profile_picture_url
    if payload.preferred_language is not None:
        other.preferred_language = payload.preferred_language
    if payload.notification_preferences is not None:
        other.notification_preferences = payload.notification_preferences
    if payload.date_of_birth is not None:
        other.date_of_birth = payload.date_of_birth

    db.commit()
    return JSONResponse(
        status_code=200, content={"message": "Profile updated successfully"}
    )


def get_approved_providers(db: Session) -> List[ServiceProvider]:
    return db.query(ServiceProvider).filter(ServiceProvider.is_approved == True).all()


def get_provider_by_id(db: Session, provider_id: int) -> ServiceProvider:
    provider = (
        db.query(ServiceProvider)
        .filter(ServiceProvider.id == provider_id, ServiceProvider.is_approved == True)
        .first()
    )
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service provider not found"
        )
    return provider
