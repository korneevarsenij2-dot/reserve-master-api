from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.security import hash_password, create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["Авторизация"])

# РЕГИСТРАЦИЯ
@router.post("/register",
response_model=UserResponse,
status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,detail="этот email уже занят")
    new_user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

# ЛОГИН
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="неверная почта или пароль"
        )
    access_token = create_access_token(data={"sub": user.email})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

