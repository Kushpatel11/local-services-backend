from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from dependencies.provider_dependencies import get_current_provider
from dependencies.admin_dependencies import get_current_admin
from models import (
    ProviderWallet,
    WalletTransaction,
    WithdrawalRequest,
    TransactionType,
    TransactionStatus,
    WithdrawalStatus,
    ServiceProvider,
)
from schemas.provider_wallet_schemas import (
    WalletResponse,
    TransactionResponse,
    WithdrawalRequestIn,
)


from typing import List
from datetime import datetime

router = APIRouter()


@router.get("/wallet", response_model=WalletResponse)
def get_wallet(
    db: Session = Depends(get_db),
    current_provider: ServiceProvider = Depends(get_current_provider),
):
    email = current_provider["sub"]
    provider = db.query(ServiceProvider).filter_by(email=email).first()
    wallet = db.query(ProviderWallet).filter_by(provider_id=provider.id).first()
    if not wallet:
        wallet = ProviderWallet(provider_id=provider.id, balance=0.0)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db),
    current_provider: ServiceProvider = Depends(get_current_provider),
):
    email = current_provider["sub"]
    provider = db.query(ServiceProvider).filter_by(email=email).first()
    wallet = db.query(ProviderWallet).filter_by(provider_id=provider.id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return [
        TransactionResponse(
            id=txn.id,
            amount=txn.amount,
            type=txn.type.value,
            status=txn.status.value,
            note=txn.note,
            created_at=txn.created_at,
        )
        for txn in wallet.transactions
    ]


@router.post("/withdraw", status_code=status.HTTP_201_CREATED)
def request_withdrawal(
    req: WithdrawalRequestIn,
    db: Session = Depends(get_db),
    current_provider: ServiceProvider = Depends(get_current_provider),
):
    email = current_provider["sub"]
    provider = db.query(ServiceProvider).filter_by(email=email).first()
    wallet = db.query(ProviderWallet).filter_by(provider_id=provider.id).first()
    if not wallet or req.amount > wallet.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")
    # Minimum withdrawal logic
    if req.amount < 100:
        raise HTTPException(status_code=400, detail="Minimum withdrawal is ₹100")
    # Deduct and lock funds
    wallet.balance -= req.amount
    withdrawal = WithdrawalRequest(
        provider_id=current_provider.id,
        amount=req.amount,
        upi_id=req.upi_id,
        status=WithdrawalStatus.requested,
    )
    db.add(withdrawal)
    db.add(
        WalletTransaction(
            wallet_id=wallet.id,
            amount=-req.amount,
            type=TransactionType.withdrawal,
            status=TransactionStatus.pending,
            note=f"Withdrawal requested (UPI: {req.upi_id})",
        )
    )
    db.commit()
    return {"detail": "Withdrawal request submitted"}


# Admin: approve or reject withdrawal
@router.post("/admin/withdrawals/{withdrawal_id}/approve")
def approve_withdrawal(
    withdrawal_id: int,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin),
):
    withdrawal = db.query(WithdrawalRequest).get(withdrawal_id)
    if not withdrawal or withdrawal.status != WithdrawalStatus.requested:
        raise HTTPException(
            status_code=404, detail="Withdrawal not found or already processed"
        )
    withdrawal.status = WithdrawalStatus.approved
    withdrawal.processed_at = datetime.utcnow()
    # Simulate payout (in real app, trigger Razorpay Payouts API)
    withdrawal.status = WithdrawalStatus.processed
    db.commit()
    return {"detail": "Withdrawal approved and processed"}


@router.post("/admin/withdrawals/{withdrawal_id}/reject")
def reject_withdrawal(
    withdrawal_id: int,
    reason: str,
    db: Session = Depends(get_db),
    admin_user=Depends(get_current_admin),
):
    withdrawal = db.query(WithdrawalRequest).get(withdrawal_id)
    if not withdrawal or withdrawal.status != WithdrawalStatus.requested:
        raise HTTPException(
            status_code=404, detail="Withdrawal not found or already processed"
        )
    withdrawal.status = WithdrawalStatus.rejected
    withdrawal.admin_note = reason
    withdrawal.processed_at = datetime.utcnow()
    # Refund to wallet
    wallet = (
        db.query(ProviderWallet).filter_by(provider_id=withdrawal.provider_id).first()
    )
    wallet.balance += withdrawal.amount
    db.add(
        WalletTransaction(
            wallet_id=wallet.id,
            amount=withdrawal.amount,
            type=TransactionType.refund,
            status=TransactionStatus.completed,
            note=f"Withdrawal rejected: {reason}",
        )
    )
    db.commit()
    return {"detail": "Withdrawal rejected, funds returned to wallet"}
