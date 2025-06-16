from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from core.database import get_db
from models import Booking, BookingStatus
from models import Payment, PaymentStatus
from models import (
    ProviderWallet,
    WalletTransaction,
    TransactionType,
    TransactionStatus,
)
from utils.razorpay_client import create_razorpay_order
from pydantic import BaseModel
from utils.razorpay_client import client

router = APIRouter()


class CreatePaymentRequest(BaseModel):
    booking_id: int
    amount: float


@router.post("/initiate")
def initiate_payment(req: CreatePaymentRequest, db: Session = Depends(get_db)):
    booking = (
        db.query(Booking)
        .options(joinedload(Booking.service))
        .filter_by(id=req.booking_id)
        .first()
    )
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.status != BookingStatus.pending:
        raise HTTPException(400, "Booking is not pending")
    order = create_razorpay_order(req.amount, receipt=f"booking_{booking.id}")
    payment = Payment(
        booking_id=booking.id,
        razorpay_order_id=order["id"],
        amount=req.amount,
        status=PaymentStatus.created,
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return {
        "order_id": order["id"],
        "amount": req.amount,
        "currency": "INR",
        "payment_id": payment.id,
        "razorpay": order,
    }


class PaymentSuccessRequest(BaseModel):
    payment_id: int


@router.post("/simulate_success")
def simulate_success(req: PaymentSuccessRequest, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter_by(id=req.payment_id).first()
    if not payment:
        raise HTTPException(404, "Payment not found")
    payment.status = PaymentStatus.succeeded
    payment.razorpay_payment_id = payment.razorpay_payment_id or f"fakepay_{payment.id}"
    booking = db.query(Booking).filter_by(id=payment.booking_id).first()
    if booking:
        booking.status = BookingStatus.completed
    db.commit()
    return {"detail": "Payment marked as succeeded, booking marked as paid"}


class BookingCompleteRequest(BaseModel):
    booking_id: int


@router.get("/booking/{booking_id}/payment_logs")
def get_payment_logs(booking_id: int, db: Session = Depends(get_db)):
    booking = db.query(Booking).filter_by(id=booking_id).first()
    if not booking:
        raise HTTPException(404, "Booking not found")
    payments = booking.payments
    return {
        "payments": [
            {
                "id": p.id,
                "status": p.status.value,
                "amount": p.amount,
                "currency": p.currency,
                "created_at": p.created_at,
                "updated_at": p.updated_at,
                "razorpay_order_id": p.razorpay_order_id,
                "razorpay_payment_id": p.razorpay_payment_id,
            }
            for p in payments
        ]
    }


@router.post("/complete_booking_and_credit_wallet")
def complete_booking_and_credit_wallet(
    req: BookingCompleteRequest, db: Session = Depends(get_db)
):
    booking = (
        db.query(Booking)
        .options(joinedload(Booking.service))
        .filter_by(id=req.booking_id)
        .first()
    )
    if not booking:
        raise HTTPException(404, "Booking not found")
    if booking.status != BookingStatus.completed:
        raise HTTPException(400, "Booking is not completed")
    # Find latest succeeded payment
    successful_payments = [
        p for p in booking.payments if p.status == PaymentStatus.succeeded
    ]
    if not successful_payments:
        raise HTTPException(400, "No successful payment found for this booking")
    payment = successful_payments[-1]

    provider_id = booking.service.provider_id
    wallet = db.query(ProviderWallet).filter_by(provider_id=provider_id).first()
    if not wallet:
        wallet = ProviderWallet(provider_id=provider_id, balance=0.0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    commission = 0.10 * payment.amount
    earning = payment.amount - commission
    wallet.balance += earning
    db.add(
        WalletTransaction(
            wallet_id=wallet.id,
            amount=earning,
            type=TransactionType.earning,
            status=TransactionStatus.completed,
            related_booking_id=booking.id,
            note="Earning for completed booking",
        )
    )
    db.commit()
    return {"detail": f"Booking completed, provider credited ₹{earning}"}


@router.post("/refund")
def refund_payment(
    payment_id: int, amount: float = None, db: Session = Depends(get_db)
):
    payment = db.query(Payment).filter_by(id=payment_id).first()
    if not payment or payment.status != PaymentStatus.succeeded:
        raise HTTPException(404, "Payment not found or not successful")
    # Use full amount if not specified
    refund = client.payment.refund(
        payment.razorpay_payment_id, {"amount": int(amount * 100) if amount else None}
    )
    payment.status = PaymentStatus.failed  # or add a new RefundStatus if needed
    db.commit()
    return {"refund": refund}
