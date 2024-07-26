from fastapi import APIRouter

router = APIRouter(
    prefix="/users"
)

@router.get("/")
def read_root():
    return {"message": "The users API is working:D"}

