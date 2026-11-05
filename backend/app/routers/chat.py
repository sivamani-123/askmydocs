from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from ..security import current_user
from ..services import rag, llm

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("/ask", response_model=schemas.AskOut)
def ask(body: schemas.AskIn, user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    hits = rag.retrieve(db, user.id, body.question, body.top_k)
    names = {d.id: d.filename for d in db.query(models.Document).filter_by(user_id=user.id)}
    answer, mode = llm.generate(body.question, [c.text for c, _ in hits])
    sources = [
        schemas.SourceOut(document_id=c.document_id, filename=names.get(c.document_id, "?"), score=round(s, 3), snippet=c.text[:220])
        for c, s in hits
    ]
    db.add(models.ChatMessage(user_id=user.id, question=body.question, answer=answer, sources=[s.model_dump() for s in sources]))
    db.commit()
    return schemas.AskOut(answer=answer, sources=sources, mode=mode)


@router.get("/history", response_model=List[schemas.HistoryOut])
def history(user: models.User = Depends(current_user), db: Session = Depends(get_db)):
    return db.query(models.ChatMessage).filter_by(user_id=user.id).order_by(models.ChatMessage.id.desc()).limit(30).all()
