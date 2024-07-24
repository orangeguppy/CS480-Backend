from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
import requests

from models.user import User

SECRET_KEY = "1234" # key for signing JWT tokens
ALGORITHM = "HS256" # for encoding/decoding JWT tokens
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # validity period of JWT in minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token") # tells FastAPI to expect an OAuth2 token in the Authorization header of the request. 
                                                       # tokenUrl is the endpoint where users can obtain a token.

def create_access_token(data: dict):
    """
    This encodes user information (username, password, role etc) into an access token
    """
    to_encode = data.copy() # contains user information
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt # returns encoded JWT

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception