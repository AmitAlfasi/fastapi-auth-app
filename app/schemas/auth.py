from pydantic import BaseModel, EmailStr, Field
from typing import Annotated

class ResendVerificationCodeRequest(BaseModel):
    email: EmailStr

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    code: Annotated[str, Field(min_length=6, max_length=6, examples=["123456"])]
