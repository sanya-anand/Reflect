"""Pydantic schemas for journal CRUD endpoints."""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class JournalCreate(BaseModel):
    """Schema for creating a new journal entry."""
    title: str = "Untitled"
    content: str
    tags: str = ""


class JournalUpdate(BaseModel):
    """Schema for updating an existing journal entry. All fields optional."""
    title: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[str] = None


class JournalResponse(BaseModel):
    """Full journal entry returned from API."""
    id: int
    user_id: int
    title: str
    content: str
    emotion: Optional[str] = None
    confidence: Optional[float] = None
    tags: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True