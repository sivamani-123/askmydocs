# AskMyDocs AI – RAG Document Assistant

Full-stack AI project: upload documents, auto-categorise them with an ML model, and ask questions answered by an LLM grounded in retrieved passages (RAG) with source citations.

## Architecture
```
React (Vite, HTML/CSS)  --REST/JWT-->  FastAPI backend  --SQLAlchemy-->  MySQL 8
                                         |-- Auth (bcrypt + JWT)
                                         |-- Business logic (routers: auth, documents, chat)
                                         |-- AI/ML: sentence-transformers embeddings (deep learning),
                                         |          cosine retrieval (RAG), TF-IDF + LogisticRegression
                                         |          classifier (ML), Claude LLM for answer generation
```
| Skill | Where |
|---|---|
| Python / FastAPI / REST | `backend/app` |
| RAG | `backend/app/services/rag.py`, `llm.py` |
| Deep learning | transformer embeddings (MiniLM) in `rag.py` |
| Machine learning | `backend/ml/train_classifier.py`, `services/classifier.py` |
| Auth | `security.py`, `routers/auth.py` |
| MySQL 8 | `database/schema.sql`, `models.py` |

## Setup
1. **MySQL**: open MySQL Workbench 8, run `database/schema.sql`.
2. **Backend** (Python 3.10+):
   ```
   cd backend
   python -m venv .venv && .venv\Scripts\activate     (Linux/Mac: source .venv/bin/activate)
   pip install -r requirements.txt
   copy .env.example .env      (set DATABASE_URL password, JWT_SECRET, ANTHROPIC_API_KEY)
   python ml/train_classifier.py
   uvicorn app.main:app --reload --port 8000
   ```
   API docs: http://localhost:8000/docs
3. **Frontend** (Node 18+): `cd frontend && npm install && npm run dev` → http://localhost:5173

Without `ANTHROPIC_API_KEY` the app still works in extractive mode (returns the best passage).

## Using VS Code
Prerequisites: VS Code, **Python 3.10-3.12**, **Node.js 18+**, MySQL 8 (Workbench optional).
1. Create the database: run `database/schema.sql` in Workbench, or `mysql -u root -p < database/schema.sql`.
2. Run `setup.bat` (Windows) or `./setup.sh` (macOS/Linux) once. It creates the virtual env, installs packages, creates `backend/.env` and trains the classifier.
3. Edit `backend/.env`: MySQL password in `DATABASE_URL`, a `JWT_SECRET`, optional `ANTHROPIC_API_KEY`.
4. Open the folder in VS Code, install the recommended extensions, and press **F5** (Backend: FastAPI).
5. Run **Terminal > Run Task > Frontend: dev server**, then open http://localhost:5173.

## Tests
`cd backend && pytest`

## Ideas to extend
Streaming answers, hybrid BM25 + vector search, re-ranking, Docker Compose, evaluation set with retrieval hit-rate.
