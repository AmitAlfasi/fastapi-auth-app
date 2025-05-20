from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, SecretStr
from os import getenv

conf = ConnectionConfig(
    MAIL_USERNAME=getenv("MAIL_USERNAME") or "",
    MAIL_PASSWORD=SecretStr(getenv("MAIL_PASSWORD") or ""),
    MAIL_FROM=getenv("MAIL_FROM") or "no-reply@example.com",
    MAIL_PORT=int(getenv("MAIL_PORT", 587)),
    MAIL_SERVER=getenv("MAIL_SERVER") or "smtp.example.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_verification_email(email: EmailStr, code: str):
    message = MessageSchema(
        subject="Your Verification Code",
        recipients=[email],
        body=f"Your verification code is: {code}",
        subtype=MessageType.plain 
    )

    fm = FastMail(conf)
    await fm.send_message(message)
