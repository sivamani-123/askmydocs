from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import config, models
from .database import Base, engine
from .routers import auth, documents, chat

Base.metadata.create_all(bind=engine)  # no-op if schema.sql already ran

app = FastAPI(title="AskMyDocs AI", version="1.0.0", description="RAG document assistant with ML classification")
app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router)
app.include_router(documents.router)
app.include_router(chat.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
