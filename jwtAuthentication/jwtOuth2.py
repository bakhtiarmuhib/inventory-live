from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from cryptography.fernet import Fernet


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


key = b'YYB7mpZFHyNW6b0QYfb9k_vaTXUv3b7my8862v02_X8='
#key = Fernet.generate_key()


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)

def encrypt_data(id,role):
    f = Fernet(key)
    d = (f"{id},{role}")
    return f.encrypt(d.encode())

def dencrypt_data(data):
    f = Fernet(key)
    data = (data[2:len(data)-1].encode())
    return f.decrypt(data).decode()
    

def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
        
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
         
    
    to_encode = {"exp": expires_delta, "data": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
     
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "data": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def decodeJWT(jwtoken: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM)
        return payload
    except:
        return None
    

def verify_jwt(jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

def get_current_user_info(header : str):
    
    if header:
        token_devided = header.split(" ")
        
        if token_devided [0] != "Bearer":
            raise Exception("Invalid authentication scheme.")
        if not verify_jwt(token_devided [1]):
            raise Exception("Invalid token or expired token.")
        return decodeJWT(token_devided [1])
    else: 
        raise Exception("Access token not found.")


    

