from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User

SECRET_KEY = "SUPER_RESERVE_KEY_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# - 1. работа с паролями

def hash_password(password: str) -> str:
    """Хэшируем пароль для базы данных"""
    return pwd_context.hash(password)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Сравниваем пароль с хэшем из базы"""
    return pwd_context.verify(plain_password, hashed_password)

# - 2. создание токена

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Генерируем цифровой JWT пропуск"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

#  3. проверка токена

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)) -> User:
    """Проверяем JWT токен и возвращает текущего юзера из базы"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="не удалось проверить учетные записи",
        headers={"WWW-Authenticate": "Bearer"},
    )

    
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise create_access_token
    except JWTError:
        raise credentials_exception
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user
    


