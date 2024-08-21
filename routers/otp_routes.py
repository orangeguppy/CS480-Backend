from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import otp as otp_db
from models import otp as otp_request
from auth import otp

router = APIRouter(
    prefix="/otp"
)

@router.get("/")
def get_all_otps(db_session: Session = Depends(get_db)):
    otp_records = db_session.query(otp_db.OTP).all()
    return otp_records

@router.post("/", status_code=status.HTTP_201_CREATED)
def generate_otp(otp_req: otp_request.OTPRequest, db_session: Session = Depends(get_db)):
    # Generate OTP and expiration datetime
    otp_json = otp.generate_otp()
    otp_int, expiration_datetime = otp_json["otp"], otp_json["expiration_datetime"]

    # Check if an OTP entry for the user already exists
    otp_entry = db_session.query(otp_db.OTP).filter(otp_db.OTP.username == otp_req.username).first()

    if otp_entry:
        # Update the existing entry
        otp_entry.otp = otp_int
        otp_entry.expiration_datetime = expiration_datetime
    else:
        # Create a new OTP entry
        otp_entry = otp_db.OTP(username=otp_req.username, otp=otp_int, expiration_datetime=expiration_datetime)
        db_session.add(otp_entry)
    
    db_session.commit()
    db_session.refresh(otp_entry)

    otp.send_otp_email(otp_req.username, otp_int, expiration_datetime)

    return {"message": f"OTP updated successfully for {otp_req.username}"}