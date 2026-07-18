"""Service for exporting journal entries to various formats."""

from typing import List
from models.journal import JournalEntry
from fpdf import FPDF
import io


def export_all_to_txt(entries: List[JournalEntry]) -> str:
    return "\n\n========================================\n\n".join([export_to_txt(e) for e in entries])


def export_all_to_markdown(entries: List[JournalEntry]) -> str:
    return "\n\n---\n\n".join([export_to_markdown(e) for e in entries])


def export_all_to_pdf(entries: List[JournalEntry]) -> bytes:
    pdf = FPDF()
    
    if not entries:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, txt="No journals to export.", ln=True, align='L')
        return bytes(pdf.output())

    for entry in entries:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, txt=entry.title, ln=True, align='L')
        pdf.set_font("Arial", 'I', 10)
        date_str = entry.created_at.strftime("%B %d, %Y at %I:%M %p")
        pdf.cell(0, 6, txt=f"Date: {date_str}", ln=True, align='L')
        if entry.emotion:
            conf = int((entry.confidence or 0) * 100)
            pdf.cell(0, 6, txt=f"Emotion: {entry.emotion.capitalize()} ({conf}%)", ln=True, align='L')
        if entry.tags:
            pdf.cell(0, 6, txt=f"Tags: {entry.tags}", ln=True, align='L')
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 8, txt=entry.content)
        
    return bytes(pdf.output())


def export_to_txt(entry: JournalEntry) -> str:
    """Export a single journal entry to plain text."""
    date_str = entry.created_at.strftime("%Y-%m-%d %H:%M:%S")
    
    lines = [
        f"Title: {entry.title}",
        f"Date: {date_str}",
        f"Emotion: {entry.emotion or 'None'} (Confidence: {entry.confidence or 0.0:.2f})",
        f"Tags: {entry.tags or 'None'}",
        "-" * 40,
        "",
        entry.content
    ]
    return "\n".join(lines)


def export_to_markdown(entry: JournalEntry) -> str:
    """Export a single journal entry to markdown format."""
    date_str = entry.created_at.strftime("%B %d, %Y")
    
    md = f"# {entry.title}\n\n"
    md += f"**Date:** {date_str}  \n"
    if entry.emotion:
        md += f"**Emotion:** {entry.emotion.capitalize()} ({int((entry.confidence or 0) * 100)}%)  \n"
    if entry.tags:
        tags = " ".join([f"`{t.strip()}`" for t in entry.tags.split(",") if t.strip()])
        md += f"**Tags:** {tags}  \n"
        
    md += "\n---\n\n"
    md += entry.content
    
    return md


def export_to_pdf(entry: JournalEntry) -> bytes:
    """Export a single journal entry to PDF format.
    Returns the raw bytes of the PDF.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Use standard fonts for simplicity
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, txt=entry.title, ln=True, align='L')
    
    pdf.set_font("Arial", 'I', 10)
    date_str = entry.created_at.strftime("%B %d, %Y at %I:%M %p")
    pdf.cell(0, 6, txt=f"Date: {date_str}", ln=True, align='L')
    
    if entry.emotion:
        conf = int((entry.confidence or 0) * 100)
        pdf.cell(0, 6, txt=f"Emotion: {entry.emotion.capitalize()} ({conf}%)", ln=True, align='L')
        
    if entry.tags:
        pdf.cell(0, 6, txt=f"Tags: {entry.tags}", ln=True, align='L')
        
    pdf.ln(5) # Add a little space
    pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Draw a horizontal line
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    # MultiCell is used for text that might wrap to multiple lines
    pdf.multi_cell(0, 8, txt=entry.content)
    
    # fpdf2 allows outputting as bytearray
    return bytes(pdf.output())
