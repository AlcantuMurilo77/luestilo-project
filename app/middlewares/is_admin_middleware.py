
from fastapi import  Depends, status, HTTPException
import jwt
from sqlalchemy.orm import Session

import core.security as security
from utils.database import get_db
from models.models import User

from app.network.oauth import oauth2_scheme

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid access level",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        email = payload.get("sub")

        if not email:
            raise credentials_exception

        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise credentials_exception

        return user
    except:
        raise credentials_exception


def user_access_admin_middleware(current_user: dict = Depends(get_current_user)):
    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not an admin"
        )
    return current_user 
