from fastapi import Depends, HTTPException, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from auth.authentication import create_access_token, get_current_user
from data.users import users_db
import requests
import os

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

router = APIRouter(
    prefix="/auth"
)

#---------------------------------------------------------------------------------------------------------
# Native Login API
#---------------------------------------------------------------------------------------------------------
@router.get("/login/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)

    # KIV: Implement check_credentials() to make a call to an external DB, but this is what it is for now
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role":user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    # return current_user
    return {"message": f"Hello, {current_user['username']}! This is a protected resource. You're a {current_user['role']}"}

#---------------------------------------------------------------------------------------------------------
# Google Login API
#---------------------------------------------------------------------------------------------------------
@router.get("/google/login")
async def login_google():
    return {
        "url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email&access_type=offline"
    }

@router.get("/google/user")
async def auth_google(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "Authorization code not found"}
    token_url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    access_token = response.json().get("access_token")
    user_info = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return user_info.json()