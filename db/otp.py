from sqlalchemy import Column, Integer, DateTime, String
from .database import Base

class OTP(Base):
    __tablename__ = 'otp'
    username = Column(String(60), primary_key=True, index=True)
    otp = Column(Integer, unique=False, index=True)
    expiration_datetime = Column(DateTime, unique=False, index=True)