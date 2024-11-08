from sqlalchemy import Column, String, DateTime
from .database import Base

class Session(Base):
    __tablename__ = 'sessions'
    
    session_id = Column(String(60), primary_key=True, index=True)
    username = Column(String(60), index=True)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<Session(session_id={self.session_id}, username={self.username}, created_at={self.created_at}, expires_at={self.expires_at})>"