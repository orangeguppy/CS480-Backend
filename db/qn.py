from sqlalchemy import Column, String, Integer, JSON
from .database import Base
class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    sub = Column(String(50), nullable=False)
    question_text = Column(String(255), nullable=False)
    option_1 = Column(String(255), nullable=False)
    option_2 = Column(String(255), nullable=False)
    option_3 = Column(String(255), nullable=False)
    option_4 = Column(String(255), nullable=False)
    correct_answer = Column(JSON, nullable=False)