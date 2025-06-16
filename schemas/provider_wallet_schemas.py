from pydantic import BaseModel
from datetime import datetime


class WalletResponse(BaseModel):
    balance: float
    updated_at: datetime


class TransactionResponse(BaseModel):
    id: int
    amount: float
    type: str
    status: str
    note: str = None
    created_at: datetime


class WithdrawalRequestIn(BaseModel):
    amount: float
    upi_id: str
