from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from auth.authentication import create_access_token, get_current_user
import requests
import os
import bcrypt
from . import session_routes

# For connecting to the users database
from db.database import get_db
from db import user as user_db
from sqlalchemy.orm import Session

# To send an OTP for email verification
from routers import otp_routes
from models.otp import OTPRequest

router = APIRouter(
    prefix="/auth"
)

@router.get("/")
async def home_route():
    # return current_user
    return {"Hello World!"}

#---------------------------------------------------------------------------------------------------------
# Native Login API
#---------------------------------------------------------------------------------------------------------
@router.post("/login/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
    username = form_data.username
    result = db_session.query(user_db.User).filter(user_db.User.username == username).first()

    if result is None or bcrypt.checkpw(form_data.password.encode('utf-8'), result.password.encode('utf-8')) is False:
        raise HTTPException(status_code=401, detail="You have entered an invalid username or password")
    
    if result.role == "unverified":
        # Create an OTP request
        otp_req = OTPRequest(username=result.username, new_acc=True)
        # Generate an OTP and send to the user
        otp_routes.generate_otp(otp_req, db_session=db_session)
        raise HTTPException(status_code=403, detail="Account not verified yet, please verify it using the OTP we've emailed you")
    
    # We need to invalidate the old session and create a new one
    updated_session = session_routes.update_session(result.username)

    access_token = create_access_token(data={"sub": result.username, "role":result.role})
    return {"access_token": access_token, "token_type": "bearer", "session": updated_session}

@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    # return current_user
    return {"message": f"Hello, {current_user['username']}! This is a protected resource. You're a {current_user['role']}"}