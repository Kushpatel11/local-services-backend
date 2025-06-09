from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from models import User, PasswordResetOTP
from core.database import get_db
from utils.otp_email import generate_otp, send_otp_email
from utils.hashing import hash_password
from schemas.user_schemas import (
    ForgotPasswordRequest,
    OTPVerifyRequest,
    ResetPasswordRequest,
)

router = APIRouter()


@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=10)
    db_otp = PasswordResetOTP(user_id=user.id, otp=otp, expires_at=expires_at)
    db.add(db_otp)
    db.commit()
    send_otp_email(user.email, otp)
    return {"msg": "OTP sent to your email."}


@router.post("/verify-otp")
def verify_otp(req: OTPVerifyRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_obj = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.user_id == user.id,
            PasswordResetOTP.otp == req.otp,
            PasswordResetOTP.is_used == False,
            PasswordResetOTP.expires_at > datetime.utcnow(),
        )
        .first()
    )

    if not otp_obj:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    return {"msg": "OTP is valid."}


@router.post("/reset-password")
def reset_password(req: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_obj = (
        db.query(PasswordResetOTP)
        .filter(
            PasswordResetOTP.user_id == user.id,
            PasswordResetOTP.otp == req.otp,
            PasswordResetOTP.is_used == False,
            PasswordResetOTP.expires_at > datetime.utcnow(),
        )
        .first()
    )

    if not otp_obj:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # Mark OTP as used
    otp_obj.is_used = True
    user.hashed_password = hash_password(
        req.new_password
    )  # implement hash_password as you do for signup
    db.commit()

    return {"msg": "Password has been reset successfully."}
