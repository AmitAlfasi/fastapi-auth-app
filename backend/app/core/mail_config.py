from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr, SecretStr, BaseModel, ConfigDict
from pydantic_settings import BaseSettings
from functools import lru_cache


# Load email-related environment variables
class MailSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: SecretStr
    MAIL_FROM: EmailStr
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"
    )


@lru_cache()
def get_mail_settings() -> MailSettings:
    return MailSettings()


# Use the config to build FastMail connection
mail_settings = get_mail_settings()

conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.MAIL_USERNAME,
    MAIL_PASSWORD=mail_settings.MAIL_PASSWORD,
    MAIL_FROM=mail_settings.MAIL_FROM,
    MAIL_PORT=mail_settings.MAIL_PORT,
    MAIL_SERVER=mail_settings.MAIL_SERVER,
    MAIL_STARTTLS=mail_settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=mail_settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=mail_settings.USE_CREDENTIALS,
    VALIDATE_CERTS=mail_settings.VALIDATE_CERTS
)


# Send verification email
async def send_verification_email(email: EmailStr, code: str):
    message = MessageSchema(
        subject="Your Verification Code",
        recipients=[email],
        body=f"Your verification code is: {code}",
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    await fm.send_message(message)
