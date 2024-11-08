from pydantic import BaseModel
from datetime import datetime

class Session(BaseModel):
    session_id: str
    username: str
    created_at: datetime
    expires_at: datetime