from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class RegisterIn(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    full_name: str


class DocumentOut(BaseModel):
    id: int
    filename: str
    category: str
    num_chunks: int
    created_at: datetime

    class Config:
        from_attributes = True


class AskIn(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    top_k: int = Field(default=4, ge=1, le=10)


class SourceOut(BaseModel):
    document_id: int
    filename: str
    score: float
    snippet: str


class AskOut(BaseModel):
    answer: str
    sources: List[SourceOut]
    mode: str  # "llm" or "extractive"


class HistoryOut(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime
    class Config:
        from_attributes = True
