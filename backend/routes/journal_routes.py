"""Journal CRUD routes with authentication and search/filter support."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime
from typing import Optional, List
import logging

from database import get_db
from models.journal import JournalEntry
from models.user import User
from schemas.journal_schema import JournalCreate, JournalUpdate, JournalResponse
from services.emotion_service import analyze_emotion
from auth.dependencies import get_current_user

logger = logging.getLogger("reflect")

router = APIRouter(prefix="/api/journals", tags=["Journals"])


@router.post("/", response_model=JournalResponse, status_code=201)
def create_entry(
    entry: JournalCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new journal entry with automatic emotion analysis."""

    # Analyze emotion from content
    emotion_result = analyze_emotion(entry.content)

    new_entry = JournalEntry(
        user_id=current_user.id,
        title=entry.title,
        content=entry.content,
        emotion=emotion_result["primary_emotion"],
        confidence=emotion_result["confidence"],
        tags=entry.tags,
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    logger.info(f"Journal created: id={new_entry.id}, emotion={new_entry.emotion}")
    return new_entry


@router.get("/", response_model=List[JournalResponse])
def get_entries(
    search: Optional[str] = Query(None, description="Search in title and content"),
    emotion: Optional[str] = Query(None, description="Filter by emotion"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    sort: Optional[str] = Query("newest", description="Sort: newest or oldest"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List journal entries with optional search, filter, and sort."""

    query = db.query(JournalEntry).filter(JournalEntry.user_id == current_user.id)

    # Search in title and content
    if search:
        query = query.filter(
            or_(
                JournalEntry.title.ilike(f"%{search}%"),
                JournalEntry.content.ilike(f"%{search}%"),
            )
        )

    # Filter by emotion
    if emotion:
        query = query.filter(JournalEntry.emotion == emotion)

    # Filter by tag (substring match in comma-separated tags)
    if tag:
        query = query.filter(JournalEntry.tags.ilike(f"%{tag}%"))

    # Sort
    if sort == "oldest":
        query = query.order_by(JournalEntry.created_at.asc())
    else:
        query = query.order_by(JournalEntry.created_at.desc())

    return query.all()


@router.get("/{journal_id}", response_model=JournalResponse)
def get_entry(
    journal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a single journal entry by ID."""

    entry = db.query(JournalEntry).filter(
        JournalEntry.id == journal_id,
        JournalEntry.user_id == current_user.id,
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    return entry


@router.put("/{journal_id}", response_model=JournalResponse)
def update_entry(
    journal_id: int,
    update_data: JournalUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update a journal entry. Re-analyzes emotion if content changes."""

    entry = db.query(JournalEntry).filter(
        JournalEntry.id == journal_id,
        JournalEntry.user_id == current_user.id,
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    # Update provided fields
    if update_data.title is not None:
        entry.title = update_data.title

    if update_data.content is not None:
        entry.content = update_data.content
        # Re-analyze emotion when content changes
        emotion_result = analyze_emotion(entry.content)
        entry.emotion = emotion_result["primary_emotion"]
        entry.confidence = emotion_result["confidence"]

    if update_data.tags is not None:
        entry.tags = update_data.tags

    entry.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(entry)

    logger.info(f"Journal updated: id={entry.id}")
    return entry


@router.delete("/{journal_id}")
def delete_entry(
    journal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a journal entry."""

    entry = db.query(JournalEntry).filter(
        JournalEntry.id == journal_id,
        JournalEntry.user_id == current_user.id,
    ).first()

    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")

    db.delete(entry)
    db.commit()

    logger.info(f"Journal deleted: id={journal_id}")
    return {"message": "Journal entry deleted successfully"}

