from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from database import Base

class JournalEntry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    emotion = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)