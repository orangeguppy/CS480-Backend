from fastapi import APIRouter

router = APIRouter(
    prefix="/games"
)

@router.get("/")
def read_root():
    return {"message": "The games API is working:D"}