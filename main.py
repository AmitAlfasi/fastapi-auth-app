from fastapi import FastAPI
from app.database import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Auth App"}
