import bcrypt
import jwt
from datetime import datetime, timedelta
from config import Config

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        Config.SECRET_KEY, 
        algorithm=Config.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str):
    return jwt.decode(
        token, 
        Config.SECRET_KEY, 
        algorithms=[Config.JWT_ALGORITHM]
    )