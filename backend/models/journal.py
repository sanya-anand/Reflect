from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class JournalEntry(Base):
    """A single journal entry with AI-detected emotion."""

    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, default="Untitled")
    content = Column(Text, nullable=False)
    emotion = Column(String, index=True)
    confidence = Column(Float)
    tags = Column(String, default="")  # Comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship back to User
    owner = relationship("User", back_populates="journals")