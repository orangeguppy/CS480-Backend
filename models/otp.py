from pydantic import BaseModel
from datetime import datetime

class OTP(BaseModel):
    username: str
    otp: int
    expiration_datetime: datetime

class OTPRequest(BaseModel):
    username: str