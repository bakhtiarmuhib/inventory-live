from typing import List
from config.emailConfig import conf
from fastapi_mail import FastMail, MessageSchema, MessageType
from jwtAuthentication.jwtOuth2 import create_access_token



link = "localhost:8000"

def token_format(email):
    token = create_access_token(email,"org")
    list_tokrn = token.split(".")
    return f"{list_tokrn[0]}/{list_tokrn[1]}/{list_tokrn[2]}"




async def mail_sender(email):

    message = MessageSchema(
        subject="Email Varification",
        recipients=[email],
        body="""click here to varify email 
        <a href="localhost">Click</a>
        """,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    
