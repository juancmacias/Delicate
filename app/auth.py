from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt
import os 
from dotenv import load_dotenv
load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")  # Cambiar por un valor seguro
ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de expiración del token

def create_access_token_1(data: dict, expires_delta: Optional[timedelta] = None):
    """Genera un token JWT con los datos proporcionados"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    return encoded_jwt

def decode_access_token(token: str):
    """Decodifica el token JWT"""
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expirado
    except jwt.InvalidTokenError:
        return None  # Token inválido
    
# Función para verificar contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Función para hashear contraseñas
def hash_password(password: str) -> str:
    return pwd_context.hash(password)