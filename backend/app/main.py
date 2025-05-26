"""
Main FastAPI application module.
This module initializes the FastAPI application, configures middleware,
sets up routes, and handles database initialization.
"""

from fastapi import FastAPI
from backend.app.database import Base, engine
from backend.app.models import user, refresh_token, verification_code
from backend.app.routes import auth, user
from dotenv import load_dotenv
from backend.app.utils.openapi import custom_openapi 
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8000", "http://127.0.0.1:8000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: Welcome message for the API
    """
    return {"message": "Welcome to FastAPI Auth App"}

# Custom OpenAPI override
app.openapi = lambda: custom_openapi(app)
