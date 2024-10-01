from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models import user as user_model
from db.database import get_db
from db import user as user_db
from db import otp as otp_db
from models import pw_reset_req, acc_activation_req, otp
from routers import otp_routes

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users"
)

# Utility function to hash passwords
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.get("/")
def get_all_users(db_session: Session = Depends(get_db)):
    # Query to get all users
    users = db_session.query(user_db.User).all()
    
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    
    return users

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: user_model.User, db_session: Session = Depends(get_db)):
    # Check if the user already exists
    db_user = db_session.query(user_db.User).filter(user_db.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=409, detail="There already exists an account with this email address")
    
    # Hash the password and create the new user
    hashed_password = get_password_hash(user.password)
    new_user = user_db.User(username=user.username, password=hashed_password, role="unverified")
    otp_routes.generate_otp(otp.OTPRequest(username=user.username, new_acc=True), db_session=db_session)
    
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    
    return {"message": f"User {user.username} created successfully!"}

@router.post("/update-password", status_code=status.HTTP_201_CREATED)
def update_user_password(request: pw_reset_req.UpdatePasswordRequest, db_session: Session = Depends(get_db)):
    # Check if the user exists
    db_user = db_session.query(user_db.User).filter(user_db.User.username == request.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the OTP is correct
    user_otp = db_session.query(otp_db.OTP).filter(otp_db.OTP.username == request.username, otp_db.OTP.otp == request.otp).first()
    if user_otp is None:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    # Check that the OTP hasn't expired, only update if the expiration datetime is still valid
    sg_timezone = timezone(timedelta(hours=8))
    current_datetime = datetime.now(sg_timezone)
    current_datetime = current_datetime.replace(tzinfo=None)
    if current_datetime <= user_otp.expiration_datetime:
        # Hash the new password and update the user
        hashed_password = get_password_hash(request.password)
        db_user.password = hashed_password
        
        # Commit the changes to the database
        db_session.commit()
        return {"message": "Password updated successfully"}
    else:
        raise HTTPException(status_code=401, detail="OTP has expired")
    
@router.post("/activate-account", status_code=status.HTTP_201_CREATED)
def activate_account(request: acc_activation_req.ActivateAccountRequest, db_session: Session = Depends(get_db)):
    # Check if the user exists
    db_user = db_session.query(user_db.User).filter(user_db.User.username == request.username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the OTP is correct
    user_otp = db_session.query(otp_db.OTP).filter(otp_db.OTP.username == request.username, otp_db.OTP.otp == request.otp).first()
    if user_otp is None:
        raise HTTPException(status_code=401, detail="Invalid OTP")
    
    # Check that the OTP hasn't expired, only update if the expiration datetime is still valid
    sg_timezone = timezone(timedelta(hours=8))
    current_datetime = datetime.now(sg_timezone)
    current_datetime = current_datetime.replace(tzinfo=None)
    if current_datetime <= user_otp.expiration_datetime:
        # Hash the new password and update the user
        db_user.role = "user"
        
        # Commit the changes to the database
        db_session.commit()
        return {"message": "User account activated!"}
    else:
        raise HTTPException(status_code=401, detail="OTP has expired")