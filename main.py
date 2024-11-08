from fastapi import FastAPI
from sqlalchemy import create_engine, text
from db.database import engine, Base, get_db
from db import user, otp, qn, session

with engine.connect() as connection:
    connection.execute(text("DROP DATABASE IF EXISTS cs480"))
    connection.execute(text("CREATE DATABASE IF NOT EXISTS cs480"))
    connection.execute(text("USE cs480"))

# Setup databases
Base.metadata.create_all(engine)

from routers import users_routes as user_routes
from routers import games_routes as game_routes
from routers import auth_routes as token_routes
from routers import otp_routes as otp_routes
from routers import quiz_qn_routes as quiz_qn_routes
from routers import session_routes as session_routes

app = FastAPI() # Create app instance

# Include routers
app.include_router(user_routes.router)
app.include_router(game_routes.router)
app.include_router(token_routes.router)
app.include_router(otp_routes.router)
app.include_router(quiz_qn_routes.router)
app.include_router(session_routes.router)

@app.get("/")
def home():
    with engine.connect() as connection:
        result = connection.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result.fetchall()]
        return {"tables": tables}