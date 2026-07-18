"""Routes for analytics, insights, and calendar heatmap."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from database import get_db
from models.user import User
from models.journal import JournalEntry
from auth.dependencies import get_current_user
import services.analytics_service as analytics_service
import services.insights_service as insights_service

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


def get_user_entries(db: Session, user_id: int) -> List[JournalEntry]:
    """Helper to fetch all journals for the current user."""
    return db.query(JournalEntry).filter(JournalEntry.user_id == user_id).all()


@router.get("/emotions")
def get_emotions_distribution(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the distribution of emotions across all user's journals."""
    entries = get_user_entries(db, current_user.id)
    
    stats = {}
    for entry in entries:
        if entry.emotion:
            stats[entry.emotion] = stats.get(entry.emotion, 0) + 1
            
    return stats


@router.get("/stats")
def get_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get basic journaling stats and streaks."""
    entries = get_user_entries(db, current_user.id)
    return analytics_service.get_basic_stats(entries)


@router.get("/trends")
def get_trends(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get emotion trends over a specified period (default 7 days)."""
    entries = get_user_entries(db, current_user.id)
    return analytics_service.get_emotion_trends(entries, days)


@router.get("/calendar")
def get_calendar(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get data for the GitHub-style contribution calendar heatmap."""
    entries = get_user_entries(db, current_user.id)
    return analytics_service.get_calendar_heatmap(entries)


@router.get("/insights")
def get_insights(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated programmatic insights."""
    entries = get_user_entries(db, current_user.id)
    return insights_service.generate_insights(entries)
