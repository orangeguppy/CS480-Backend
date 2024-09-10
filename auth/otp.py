import os
import pyotp
from datetime import datetime, timezone, timedelta
import yagmail

OTP_SECRET_KEY = os.getenv("OTP_SECRET_KEY")
OTP_EMAIL_SENDER = os.getenv("OTP_EMAIL_SENDER")
OTP_EMAIL_SENDER_PW = os.getenv("OTP_EMAIL_SENDER_PW")
OTP_LIFESPAN = os.getenv("OTP_LIFESPAN")

def generate_otp():
    # Generate an OTP with the pyotp library (less predictable than random)
    otp = pyotp.TOTP(OTP_SECRET_KEY)
    totp_string = otp.now()
    totp_int = int(totp_string)

    # Set the timezone and expiration datetime using timedelta (example: UTC+9)
    sg_timezone = timezone(timedelta(hours=8))
    expiration_datetime = datetime.now(sg_timezone) + timedelta(minutes=int(OTP_LIFESPAN))
    return {"otp": totp_int, "expiration_datetime": expiration_datetime}

def send_otp_email(username, otp, expiration_datetime, new_acc):
    yag = yagmail.SMTP(OTP_EMAIL_SENDER, OTP_EMAIL_SENDER_PW)
    if not new_acc:
        yag.send(
            to=username,
            subject="Here's Your Password Reset OTP",
            contents=f"Use this OTP {otp} to reset your password in the app. Your OTP is valid until {expiration_datetime}."
        )
    else:
        yag.send(
            to=username,
            subject="Verify your account with this OTP",
            contents=f"Use this OTP {otp} to verify your account in the app. Your OTP is valid until {expiration_datetime}."
        )

def send_email_verification_otp(username, otp, expiration_datetime):
    yag = yagmail.SMTP(OTP_EMAIL_SENDER, OTP_EMAIL_SENDER_PW)
    yag.send(
        to=username,
        subject="Here's Your Password Reset OTP",
        contents=f"Use this OTP {otp} to reset your password in the app. Your OTP is valid until {expiration_datetime}."
    )