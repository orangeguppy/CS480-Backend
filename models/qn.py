from pydantic import BaseModel
from typing import List

# Pydantic schema for request data (without 'id')
class Question(BaseModel):
    category: str
    sub: str
    question_text: str
    option_1: str
    option_2: str
    option_3: str
    option_4: str
    correct_answer: List[str]

    class Config:
        orm_mode = True

# Pydantic schema for response data (including 'id')
class QuestionResponse(Question):
    id: int