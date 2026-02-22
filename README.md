# RAG Note Vault

Local-first "note vault" MVP. The long-term goal is to drop in messy documents and later layer on Retrieval-Augmented Generation (RAG) chat, AI suggestions, and note-cleanup workflows.

> **Status -- February 22, 2026:** Foundation + ingestion MVP is in place (FastAPI upload/list endpoints, Streamlit upload UI, Postgres + pgvector, Alembic migration flow, uv-managed environment).

---

## What ships today

- FastAPI backend exposing `/health`
- FastAPI upload endpoint: `POST /documents/upload` (stores file to disk + metadata to DB)
- FastAPI listing endpoint: `GET /documents` (returns uploaded documents newest first)
- Streamlit UI with:
  - API health check sidebar
  - file upload action
  - document list view
- Postgres + pgvector via `docker compose`
- Alembic migration setup and initial migration for `documents` table
- Deterministic environment managed by `uv` + `pyproject.toml`
- `.env`-driven configuration and `data/` directories for local storage

## Not built yet 

- Embeddings/index building
- RAG chat or suggestion workflows
- Chunking/ingestion pipeline beyond raw file storage
- Automated tests and CI checks for API/UI behavior

---

## Requirements

- Python 3.12
- `uv` for dependency management
- Docker + Docker Compose
- Git

---

## Project structure

```text
rag-note-vault/
|-- apps/
|   |-- api/
|   |   |-- main.py      # FastAPI routes
|   |   |-- db.py        # SQLAlchemy engine/session/base
|   |   |-- models.py    # Document ORM model
|   |   |-- settings.py  # Pydantic settings (.env)
|   |-- ui/
|   |   |-- app.py       # Streamlit UI
|-- alembic/
|   |-- env.py
|   |-- versions/        # migration files
|-- alembic.ini
|-- packages/
|   |-- core/         # placeholder for shared logic
|-- data/
|   |-- inbox/        # uploaded raw files
|   |-- derived/      # future generated artifacts
|-- docker-compose.yml
|-- pyproject.toml
|-- .env              # local config (not committed)
|-- uv.lock
```

---

## Setup

1. **Clone & enter**
   ```bash
   git clone <YOUR_REPO_URL>
   cd rag-note-vault
   ```
2. **Start Postgres + pgvector**
   ```bash
   docker compose up -d
   docker compose ps   # confirm containers are healthy
   ```
3. **Install Python dependencies**
   ```bash
   uv sync
   ```
   _Need `uv`?_ Follow the official install instructions once, then re-run `uv sync`.
4. **Create `.env`**
   ```env
   DATABASE_URL=postgresql+psycopg://rag:rag@localhost:5432/ragdb
   DATA_DIR=./data
   API_BASE_URL=http://127.0.0.1:8000
   ```
5. **Run DB migrations**
   ```bash
   uv run alembic upgrade head
   ```

---

## Run the stack

### FastAPI backend
```bash
uv run uvicorn apps.api.main:app --reload --port 8000
```
Verify:
- http://127.0.0.1:8000/health -> `{"status":"ok"}`
- `POST /documents/upload` via Swagger at http://127.0.0.1:8000/docs
- `GET /documents` should return an array
- http://127.0.0.1:8000/docs (interactive Swagger UI)

### Streamlit UI
```bash
uv run streamlit run apps/ui/app.py
```
The page should show API health, let you upload a file, and list saved documents. If you change the API port, update `API_BASE_URL` and restart Streamlit.

---

## Troubleshooting

- **`/health` returns 404**  
  Double-check you requested `/health` (not `/`). Confirm the server logs show FastAPI running with the `apps.api.main:app` target.

- **Wrong module path**  
  Always start the server with `uv run uvicorn apps.api.main:app --reload --port 8000`.

- **`alembic` reports missing table/column**  
  Ensure migrations are applied:
  ```bash
  uv run alembic upgrade head
  ```

- **Port already in use**  
  Pick another port: `uv run uvicorn apps.api.main:app --reload --port 8001`, then update `API_BASE_URL` everywhere it is consumed.

- **Database container down**  
  ```bash
  docker compose ps
  docker compose down && docker compose up -d
  ```

---

## License

License not chosen yet. Treat this code as private/internal until a license is added.
