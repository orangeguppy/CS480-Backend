from fastapi import FastAPI
from routers import users_routes as user_routes
from routers import games_routes as game_routes
from routers import token_gen_routes as token_routes

app = FastAPI() # Create app instance

# Include routers
app.include_router(user_routes.router)
app.include_router(game_routes.router)
app.include_router(token_routes.router)

@app.get("/")
def home():
    return {
        "message": "Hello World:)"
    }