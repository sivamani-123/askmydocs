from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, LargeBinary
from sqlalchemy.dialects.mysql import MEDIUMTEXT, LONGBLOB
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(120), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = Column(String(255), nullable=False)
    category = Column(String(60), nullable=False, default="Uncategorized")
    num_chunks = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    chunks = relationship("Chunk", cascade="all, delete-orphan", passive_deletes=True)


class Chunk(Base):
    __tablename__ = "chunks"
    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    text = Column(MEDIUMTEXT, nullable=False)
    embedding = Column(LONGBLOB, nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(MEDIUMTEXT, nullable=False)
    sources = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
