from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from auth.authentication import create_access_token, get_current_user
from data.users import users_db

router = APIRouter(
    prefix="/token"
)

@router.get("/")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if user is None or user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
async def protected_route(username: str = Depends(get_current_user)):
    return {"message": f"Hello, {username}! This is a protected resource."}