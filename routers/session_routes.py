from fastapi import APIRouter
from models import session as session_model
from fastapi import APIRouter, HTTPException, status, Depends
from db.database import get_db
from db import session as session_db
from sqlalchemy.orm import Session
from auth import session as session_utils
from datetime import datetime, timezone, timedelta
import os

SESSION_LIFESPAN = os.getenv("OTP_LIFESPAN")

router = APIRouter(
    prefix="/session"
)

@router.get("/")
def read_root():
    return {"message": "The session API is working:D"}

def update_session(username: str, db_session: Session = Depends(get_db)):
    # Check if the user already has an active session by querying the session database
    existing_session = db_session.query(session_db.Session).filter(session_db.Session.username == username).first()

    # Invalidate the session if it already exists previously
    if existing_session:
        db_session.delete(existing_session)
        db_session.commit()  # Commit the transaction to delete the session

    # For generating created_at and expires_at datetimes
    sg_timezone = timezone(timedelta(hours=8))
    created_at_datetime = datetime.now(sg_timezone)
    expiration_datetime =  created_at_datetime + timedelta(minutes=int(SESSION_LIFESPAN))

    new_session_id = session_utils.generate_new_session_id() # Generate this uniquely

    # Create a new session
    new_session = session_db.Session(
        session_id=new_session_id,
        username=username,
        created_at=created_at_datetime,
        expires_at=expiration_datetime  # Session expires in 1 hour
    )

    # Add the new session to the database session and commit
    db_session.add(new_session)
    db_session.commit()
    db_session.refresh(new_session)
    
    return new_session