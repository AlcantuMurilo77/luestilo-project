from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.network.schemas.user import UserCreate, UserRead, Token
from models.models import User
from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password, create_access_token
from utils.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register", 
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Register a new user",
    description="Create a new user with email and password. Email must be unique.",
    response_description="The created user object"
)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    - **email**: Unique email of the user
    - **password**: Password for the user account
    """
    repo = UserRepository(session)
    existing = await repo.get_by_email(user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    await repo.create(user)
    return user

@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user and get access token",
    description="Authenticate user with username (email) and password, returns JWT token.",
    response_description="Access token for authorized requests"
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db)
):
    """
    User login to get JWT token.
    - **username**: The email of the user
    - **password**: The user's password
    """
    repo = UserRepository(session)
    user = await repo.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = create_access_token({"sub": str(user.id), "is_admin": user.is_admin})
    return {"access_token": token, "token_type": "bearer"}
