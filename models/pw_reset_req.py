from pydantic import BaseModel

class UpdatePasswordRequest(BaseModel):
    username: str
    otp: int
    password: str