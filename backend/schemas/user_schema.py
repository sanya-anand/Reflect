"""Pydantic schemas for user authentication endpoints."""

from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for user registration."""
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    """Schema for user login."""
    email: str
    password: str


class UserResponse(BaseModel):
    """Public user profile (no password hash)."""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """JWT token returned after login/signup."""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ChangePassword(BaseModel):
    """Schema for password change."""
    current_password: str
    new_password: str
