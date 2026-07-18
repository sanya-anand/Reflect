"""Authentication routes: signup, login, profile, password change, account deletion."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import logging

from database import get_db
from models.user import User
from models.journal import JournalEntry
from schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    ChangePassword,
)
from auth.jwt_handler import create_access_token
from auth.password import hash_password, verify_password
from auth.dependencies import get_current_user

logger = logging.getLogger("reflect")

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user and return a JWT token."""

    # Check for existing email
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check for existing username
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hash_password(user_data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info(f"New user registered: {user.username}")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Authenticate user and return a JWT token."""

    user = db.query(User).filter(User.email == credentials.email).first()

    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    logger.info(f"User logged in: {user.username}")

    token = create_access_token({"sub": str(user.id)})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user),
    )


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get the currently authenticated user's profile."""
    return current_user


@router.put("/change-password")
def change_password(
    data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change the current user's password."""

    if not verify_password(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    current_user.password_hash = hash_password(data.new_password)
    db.commit()

    logger.info(f"Password changed for user: {current_user.username}")
    return {"message": "Password changed successfully"}


@router.delete("/delete-account")
def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete the current user's account and all their journals."""

    username = current_user.username

    # Cascade delete handles journals via relationship config,
    # but explicit delete ensures clarity
    db.query(JournalEntry).filter(JournalEntry.user_id == current_user.id).delete()
    db.delete(current_user)
    db.commit()

    logger.info(f"Account deleted: {username}")
    return {"message": "Account deleted successfully"}
