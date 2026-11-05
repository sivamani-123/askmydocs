from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, security
from ..database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=schemas.TokenOut, status_code=201)
def register(body: schemas.RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=body.email.lower()).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "Email already registered")
    user = models.User(email=body.email.lower(), full_name=body.full_name, password_hash=security.hash_password(body.password))
    db.add(user)
    db.commit()
    return schemas.TokenOut(access_token=security.create_token(user.id), full_name=user.full_name)


@router.post("/login", response_model=schemas.TokenOut)
def login(body: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=body.email.lower()).first()
    if not user or not security.verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong email or password")
    return schemas.TokenOut(access_token=security.create_token(user.id), full_name=user.full_name)
