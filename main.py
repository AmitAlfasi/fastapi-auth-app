from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, refresh_token, verification_code
from app.routes import auth
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
app.include_router(auth.router)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Auth App"}
