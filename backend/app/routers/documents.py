from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..security import current_user
from ..services import rag, classifier

router = APIRouter(prefix="/api/documents", tags=["documents"])
MAX_BYTES = 5 * 1024 * 1024


@router.get("", response_model=List[schemas.DocumentOut])
def list_documents(user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(models.Document).filter_by(user_id=user.id).order_by(models.Document.id.desc()).all()


@router.post("", response_model=schemas.DocumentOut, status_code=201)
async def upload(file: UploadFile = File(...), user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith((".pdf", ".txt", ".md")):
        raise HTTPException(415, "Only PDF, TXT or MD files are supported")
    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(413, "File larger than 5 MB")
    text = rag.extract_text(file.filename, data)
    if not text.strip():
        raise HTTPException(422, "No readable text found in file")
    doc = models.Document(user_id=user.id, filename=file.filename, category=classifier.classify(text))
    db.add(doc)
    db.flush()
    doc.num_chunks = rag.ingest(db, user.id, doc, text)
    db.commit()
    db.refresh(doc)
    return doc


@router.delete("/{doc_id}", status_code=204)
def delete(doc_id: int, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter_by(id=doc_id, user_id=user.id).first()
    if not doc:
        raise HTTPException(404, "Document not found")
    db.delete(doc)
    db.commit()
