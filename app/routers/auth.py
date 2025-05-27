from fastapi import APIRouter, Depends, HTTPException 
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.network.schemas.user import  UserCreate, UserRead, Token
from models.models import User
from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password, create_access_token
from utils.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    existing =  repo.get_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    repo.create(user)
    return user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    repo = UserRepository(session)
    user = repo.get_by_email(form_data.username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}



