from pydantic import BaseModel

class ActivateAccountRequest(BaseModel):
    username: str
    otp: int