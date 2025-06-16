import razorpay
import hmac
import hashlib
from core.config import settings

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def create_razorpay_order(amount: float, receipt: str):
    order = client.order.create(
        {
            "amount": int(amount * 100),  # paise
            "currency": "INR",
            "receipt": receipt,
            "payment_capture": 1,
        }
    )
    return order


def verify_razorpay_signature(order_id, payment_id, signature):
    return client.utility.verify_payment_signature(
        {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }
    )


def verify_webhook_signature(body: bytes, signature: str, secret: str):
    generated_signature = hmac.new(
        bytes(secret, "utf-8"), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(generated_signature, signature)
