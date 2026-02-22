# RAG Note Vault

Local-first "note vault" MVP. The long-term goal is to drop in messy documents and later layer on Retrieval-Augmented Generation (RAG) chat, AI suggestions, and note-cleanup workflows.

> **Status -- January 27, 2026:** Phase 1 foundation is in place (FastAPI health endpoint, Streamlit UI, Postgres + pgvector via Docker, uv-managed environment). Next milestone: ingestion, embeddings, and chat workflows.

---

## What ships today (Phase 1)

- FastAPI backend exposing `/health`
- Streamlit UI that pings the API and echoes the health payload
- Postgres + pgvector via `docker compose`
- Deterministic environment managed by `uv` + `pyproject.toml`
- `.env`-driven configuration and `data/` directories for local storage

## Not built yet (Phase 2+ backlog)

- File uploads or inbox processing
- Database schema migrations
- Embeddings/index building
- RAG chat or suggestion workflows

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
|   |-- api/          # FastAPI backend (apps/api/main.py)
|   |-- ui/           # Streamlit UI (apps/ui/app.py)
|-- packages/
|   |-- core/         # placeholder for shared logic
|-- data/
|   |-- inbox/        # future raw uploads
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

---

## Run the stack

### FastAPI backend
```bash
uv run uvicorn apps.api.main:app --reload --port 8000
```
Verify:
- http://127.0.0.1:8000/health -> `{"status":"ok"}`
- http://127.0.0.1:8000/docs (interactive Swagger UI)

### Streamlit UI
```bash
uv run streamlit run apps/ui/app.py
```
The page should render the JSON returned by `/health`. If you change the API port, update `API_BASE_URL` and restart Streamlit.

---

## Troubleshooting

- **`/health` returns 404**  
  Double-check you requested `/health` (not `/`). Confirm the server logs show FastAPI running with the `apps.api.main:app` target.

- **Wrong module path**  
  Always start the server with `uv run uvicorn apps.api.main:app --reload --port 8000`.

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
