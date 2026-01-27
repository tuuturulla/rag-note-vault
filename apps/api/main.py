from fastapi import FastAPI

app = FastAPI(title="RAG Note Vault")

@app.get("/health")
def health():
    return {"status": "ok"}
