from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
# from env import MAIL_USERNAME,MAIL_PASSWORD,MAIL_FROM,MAIL_PORT,MAIL_SERVER
# import os
# from dotenv import load_dotenv
# load_dotenv()


conf = ConnectionConfig(
    MAIL_USERNAME ="bakhtiarmuhiboffice@gmail.com",
    MAIL_PASSWORD = "omjsssijtklcmzqe",
    MAIL_FROM = "bakhtiarmuhiboffice@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)




