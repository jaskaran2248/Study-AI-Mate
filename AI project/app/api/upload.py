"""
StudyMate AI - Document Upload & Management Endpoints
"""
import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional, List
from app.database import get_connection
from app.services.text_extractor import extract_text_from_file, compute_document_metadata
from app.models import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/api", tags=["Documents"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
def upload_file_or_text(
    file: Optional[UploadFile] = File(None),
    title: Optional[str] = Form(None),
    custom_text: Optional[str] = Form(None),
    subject: Optional[str] = Form("General"),
    sdg_target: Optional[str] = Form("SDG 4.4 - Quality Education & Skills")
):
    """
    Uploads a document (PDF, DOCX, TXT, MD, CSV, JSON) or accepts direct text/syllabus paste.
    """
    if file and file.filename:
        # Save file to uploads folder
        safe_filename = os.path.basename(file.filename)
        save_path = os.path.join(UPLOAD_DIR, safe_filename)
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        try:
            content, file_type = extract_text_from_file(save_path, safe_filename)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract text: {str(e)}")
            
        doc_title = title.strip() if (title and title.strip()) else os.path.splitext(safe_filename)[0]
    elif custom_text and custom_text.strip():
        content = custom_text.strip()
        file_type = "text"
        safe_filename = "pasted_syllabus.txt"
        doc_title = title.strip() if (title and title.strip()) else "Uploaded Study Material"
    else:
        raise HTTPException(status_code=400, detail="Please upload a file or paste syllabus text.")

    if len(content.strip()) < 15:
        raise HTTPException(status_code=400, detail="Document content too short. Please provide meaningful study text.")

    # Compute metadata
    meta = compute_document_metadata(content)
    final_sdg = sdg_target or meta['sdg_target']

    # Insert into database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO documents (
        title, filename, file_type, content, word_count,
        reading_time_min, subject, sdg_target, tags
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        doc_title, safe_filename, file_type, content, meta['word_count'],
        meta['reading_time_min'], subject, final_sdg, meta['tags']
    ))
    doc_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "success": True,
        "document_id": doc_id,
        "title": doc_title,
        "file_type": file_type,
        "word_count": meta['word_count'],
        "reading_time_min": meta['reading_time_min'],
        "sdg_target": final_sdg,
        "tags": meta['tags'],
        "preview": content[:300] + ("..." if len(content) > 300 else "")
    }

@router.get("/documents")
def list_documents():
    """Returns all stored documents."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, filename, file_type, word_count, reading_time_min, subject, sdg_target, tags, created_at FROM documents ORDER BY created_at DESC")
    docs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"documents": docs}

@router.get("/documents/{doc_id}")
def get_document(doc_id: int):
    """Retrieves document details and full text."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    doc = cursor.fetchone()
    conn.close()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return dict(doc)

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: int):
    """Deletes document and associated notes and quizzes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()
    return {"success": True, "message": "Document deleted successfully."}
