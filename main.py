from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, refresh_token, verification_code
from app.routes import auth, user
from dotenv import load_dotenv
from app.utils.openapi import custom_openapi 

load_dotenv()

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Auth App"}

app.openapi = lambda: custom_openapi(app)