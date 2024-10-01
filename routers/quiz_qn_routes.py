from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db import qn as qn_db
import pandas as pd
import json
from db.database import get_db
from db.qn import Question

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

router = APIRouter(
    prefix="/questions"
)

@router.get("/")
def get_all_questions(db_session: Session = Depends(get_db)):
    # Insert all entries first
    try:
        load_csv_to_db("db/quizzes_rows.csv", db_session)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed")
    # Query to get all users
    questions = db_session.query(qn_db.Question).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No users found")
    return questions

# Read the CSV and load the data
def load_csv_to_db(csv_file, db_session):
    # Read CSV file into DataFrame
    data = pd.read_csv(csv_file)
    insert_data(data, db_session)  # Pass the session to insert_data

# Function to insert data into the database
def insert_data(data: pd.DataFrame, db_session: Session):
    for _, row in data.iterrows():
        # Parse the correct_answer safely using json.loads
        correct_answer = json.loads(row["correct_answer"])

        question = Question(
            category=row["category"],
            sub=row["sub"],
            question_text=row["question_text"],
            option_1=row["option_1"],
            option_2=row["option_2"],
            option_3=row["option_3"],
            option_4=row["option_4"],
            correct_answer=correct_answer
        )
        print(f"Inserted question: {question}")
        logging.info(f"Inserted question: {question}")
        db_session.add(question)
        db_session.commit()
        logging.info("Data committed successfully")