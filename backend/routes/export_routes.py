"""Routes for exporting journal entries."""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from models.journal import JournalEntry
from auth.dependencies import get_current_user
import services.export_service as export_service

router = APIRouter(prefix="/api/export", tags=["Export"])


def get_entry_or_404(db: Session, journal_id: int, user_id: int) -> JournalEntry:
    entry = db.query(JournalEntry).filter(
        JournalEntry.id == journal_id,
        JournalEntry.user_id == user_id
    ).first()
    
    if not entry:
        raise HTTPException(status_code=404, detail="Journal entry not found")
        
    return entry


def get_all_entries(db: Session, user_id: int):
    return db.query(JournalEntry).filter(JournalEntry.user_id == user_id).order_by(JournalEntry.created_at.desc()).all()


@router.get("/txt")
def export_all_txt(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entries = get_all_entries(db, current_user.id)
    content = export_service.export_all_to_txt(entries)
    
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename=reflect_journals.txt"}
    )


@router.get("/md")
def export_all_md(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entries = get_all_entries(db, current_user.id)
    content = export_service.export_all_to_markdown(entries)
    
    return Response(
        content=content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=reflect_journals.md"}
    )


@router.get("/pdf")
def export_all_pdf(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    entries = get_all_entries(db, current_user.id)
    
    try:
        pdf_bytes = export_service.export_all_to_pdf(entries)
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=reflect_journals.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")


@router.get("/{journal_id}/txt")
def export_txt(
    journal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export journal entry to a plain text file."""
    entry = get_entry_or_404(db, journal_id, current_user.id)
    content = export_service.export_to_txt(entry)
    
    # Format filename
    filename = f"Journal_{entry.created_at.strftime('%Y%m%d')}.txt"
    
    return Response(
        content=content,
        media_type="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/{journal_id}/md")
def export_md(
    journal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export journal entry to a Markdown file."""
    entry = get_entry_or_404(db, journal_id, current_user.id)
    content = export_service.export_to_markdown(entry)
    
    filename = f"Journal_{entry.created_at.strftime('%Y%m%d')}.md"
    
    return Response(
        content=content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.get("/{journal_id}/pdf")
def export_pdf(
    journal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Export journal entry to a PDF file."""
    entry = get_entry_or_404(db, journal_id, current_user.id)
    
    try:
        pdf_bytes = export_service.export_to_pdf(entry)
        
        filename = f"Journal_{entry.created_at.strftime('%Y%m%d')}.pdf"
        
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")
