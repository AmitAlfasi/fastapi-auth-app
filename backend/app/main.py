"""
Main FastAPI application module.
This module initializes the FastAPI application, configures middleware,
sets up routes, and handles database initialization.
"""

from fastapi import FastAPI
from backend.app.database import Base, engine
from backend.app.models import user
from backend.app.routes import auth, user
from backend.app.utils.openapi import custom_openapi 
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
load_dotenv()

from backend.app.config import get_settings
settings = get_settings()

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS, 
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
