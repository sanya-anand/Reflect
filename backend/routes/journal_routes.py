from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.journal import JournalEntry
from schemas.journal_schema import JournalCreate
from services.emotion_service import detect_emotion

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/entry")
def create_entry(entry: JournalCreate, db: Session = Depends(get_db)):

    emotion, confidence = detect_emotion(entry.content)

    new_entry = JournalEntry(
        content=entry.content,
        emotion=emotion
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry

@router.get("/entries")
def get_entries(db: Session = Depends(get_db)):
    entries = db.query(JournalEntry).all()
    return entries

@router.get("/analytics/emotions")
def emotion_stats(db: Session = Depends(get_db)):
    
    entries = db.query(JournalEntry).all()

    stats = {}

    for entry in entries:
        emotion = entry.emotion
        stats[emotion] = stats.get(emotion, 0) + 1

    return stats