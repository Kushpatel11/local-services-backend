import random
import smtplib
from email.mime.text import MIMEText


def generate_otp(length=6):
    """Generate a numeric OTP of given length."""
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def send_otp_email(to_email, otp):
    # Replace with your email and app password
    sender_email = "gamdhakush82@gmail.com"
    app_password = "wgyi xfmi audy aaww"
    subject = "Your Password Reset OTP"
    body = f"Your OTP for password reset is: {otp}\nIt is valid for 10 minutes."

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.sendmail(sender_email, [to_email], msg.as_string())
