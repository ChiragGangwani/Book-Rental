from typing import List
from fastapi import APIRouter,Response
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel
from .config import credidentials
from .schemas import email

conf = ConnectionConfig(
    MAIL_USERNAME =credidentials.MAIL_USERNAME,
    MAIL_PASSWORD = credidentials.MAIL_PASSWORD,
    MAIL_FROM = credidentials.MAIL_FROM,
    MAIL_PORT = credidentials.MAIL_PORT,
    MAIL_SERVER = credidentials.MAIL_SERVER,
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


async def send_email(email:email,content:str,subject:str):

    message = MessageSchema(
        subject=subject,
        recipients=email,
        body=content,
        subtype=MessageType.plain)

    fm = FastMail(conf)
    await fm.send_message(message)
    return Response(status_code=200)