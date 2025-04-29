from fastapi import Depends, HTTPException
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from schemas.user_schemas import (
    UserCreate,
    UserLogin,
)  # Make sure these schemas exist in your code
from models import User  # Ensure the User model is defined with the correct fields
from core.database import get_db
from core.security import hash_password, verify_password, create_access_token


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


def login_user(user: UserLogin, db: Session = Depends(get_db)):
    result = db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
