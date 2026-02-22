import os
import uuid
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from apps.api.settings import settings
from apps.api.db import get_db
from apps.api.models import Document

# Initialize FastAPI app
app = FastAPI(title="RAG Note Vault")

# Health check endpoint to verify the API is running
@app.get("/health")
def health():
    return {"status": "ok"}

# Document upload endpoint 
# Handles file uploads, saves them to dicsk and records metadata in the database 
@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Ensure the uploaded file has a name
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    # Generate a unique ID and create dedicated directory for the uploaded file 
    doc_id = uuid.uuid4()
    inbox_dir = Path(settings.data_dir) / "inbox" / str(doc_id)
    inbox_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize the filename and define the local storage path 
    safe_name = os.path.basename(file.filename)
    file_path = inbox_dir / safe_name

    # Save the file content from memory to the local file system
    contents = await file.read()
    file_path.write_bytes(contents)

    # Creatwe an ORM instance and save the file metadata to the database
    doc = Document(
        id=doc_id,
        filename=safe_name,
        mime_type=file.content_type or "application/octet-stream",
        file_path=str(file_path),
    )
    db.add(doc)
    db.commit()

    return {"id": str(doc_id), "filename": safe_name}

# Document listing endpoint 
# Fetches all document records from the database, sorted by newest first. 
@app.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    # Execute a query to select all documents ordered by creation date
    # .scalars().all() converts the results rows into a list of Documents objects
    rows = db.execute(select(Document).order_by(Document.created_at.desc())).scalars().all()

    # Return a list of dictionaries (which FastAPI converts to JSON Array)
    return [
        {
            "id": str(d.id),
            "filename": d.filename,
            "mime_type": d.mime_type,
            "file_path": d.file_path,
            "created_at": d.created_at.isoformat(),
        }
        for d in rows
    ]