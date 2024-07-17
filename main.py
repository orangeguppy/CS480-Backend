from fastapi import FastAPI
from users import routes as user_routes
from games import routes as game_routes

app = FastAPI() # Create app instance

# Include routers
app.include_router(user_routes.router)
app.include_router(game_routes.router)

@app.get("/")
def home():
    return {
        "message": "Hello World:)"
    }