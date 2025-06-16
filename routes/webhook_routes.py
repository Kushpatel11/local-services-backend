from fastapi import APIRouter, Request, HTTPException, status, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from models import Payment, PaymentStatus, Booking, BookingStatus
from utils.razorpay_client import verify_webhook_signature
from core.config import settings
import os

router = APIRouter()

RAZORPAY_WEBHOOK_SECRET = settings.RAZORPAY_WEBHOOK_SECRET


@router.post("/razorpay/webhook")
async def razorpay_webhook(request: Request, db: Session = Depends(get_db)):
    body = await request.body()
    signature = request.headers.get("x-razorpay-signature")
    if not signature or not verify_webhook_signature(
        body, signature, RAZORPAY_WEBHOOK_SECRET
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature"
        )

    payload = await request.json()
    event = payload.get("event")
    payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})

    razorpay_payment_id = payment_entity.get("id")
    payment = (
        db.query(Payment).filter_by(razorpay_payment_id=razorpay_payment_id).first()
    )
    if not payment:
        # Optionally create Payment here if not found
        return {"status": "payment not found"}

    # Handle events
    if event == "payment.captured":
        payment.status = PaymentStatus.succeeded
        booking = db.query(Booking).filter_by(id=payment.booking_id).first()
        if booking and booking.status != BookingStatus.completed:
            booking.status = BookingStatus.completed
    elif event == "payment.failed":
        payment.status = PaymentStatus.failed
    db.commit()
    return {"status": "ok"}
