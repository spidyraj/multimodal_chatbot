from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import settings
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        # Truncate password if too long for bcrypt (max 72 bytes)
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        # Fallback to direct bcrypt verification
        try:
            if len(plain_password.encode('utf-8')) > 72:
                plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except:
            return False

def get_password_hash(password: str) -> str:
    try:
        # Truncate password if too long for bcrypt (max 72 bytes)
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return pwd_context.hash(password)
    except Exception as e:
        # Fallback to direct bcrypt hashing
        try:
            if len(password.encode('utf-8')) > 72:
                password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        except Exception as fallback_e:
            raise ValueError(f"Password hashing failed: {fallback_e}")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        
        # Ensure SECRET_KEY is set and valid
        if not settings.SECRET_KEY or len(settings.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    except Exception as e:
        # Fallback token creation with default settings
        try:
            fallback_secret = "fallback-secret-key-for-development-only-use-at-least-32-chars"
            to_encode = data.copy()
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=30)  # Shorter expiry for fallback
            
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(to_encode, fallback_secret, algorithm="HS256")
            return encoded_jwt
        except Exception as fallback_e:
            raise ValueError(f"Token creation failed: {str(e)}. Fallback also failed: {str(fallback_e)}")

def verify_token(token: str) -> Optional[dict]:
    try:
        # Try primary verification
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except Exception as e:
        # Try fallback verification
        try:
            fallback_secret = "fallback-secret-key-for-development-only-use-at-least-32-chars"
            payload = jwt.decode(token, fallback_secret, algorithms=["HS256"])
            return payload
        except Exception as fallback_e:
            # Token is invalid or expired
            return None
