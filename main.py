from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, refresh_token
from app.routes import auth


app = FastAPI()
app.include_router(auth.router)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Auth App"}
