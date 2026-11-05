from datetime import datetime, timedelta
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from . import config, models
from .database import get_db

bearer = HTTPBearer()


def hash_password(pw: str) -> str:
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()


def verify_password(pw: str, hashed: str) -> bool:
    return bcrypt.checkpw(pw.encode(), hashed.encode())


def create_token(user_id: int) -> str:
    exp = datetime.utcnow() + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": exp}, config.JWT_SECRET, algorithm="HS256")


def current_user(creds: HTTPAuthorizationCredentials = Depends(bearer), db: Session = Depends(get_db)) -> models.User:
    try:
        payload = jwt.decode(creds.credentials, config.JWT_SECRET, algorithms=["HS256"])
        user = db.get(models.User, int(payload["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError):
        user = None
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid or expired token")
    return user
