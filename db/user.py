from sqlalchemy import Column, String
from .database import Base

class User(Base):
    __tablename__ = 'users'
    username = Column(String(60), primary_key=True, index=True)
    password = Column(String(200), unique=False, index=True)
    role = Column(String(20), unique=False, index=True)

    def __repr__(self):
        return f'User {self.username}'