"""
AI SECOND BRAIN — BACKEND
FastAPI + Groq 
"""

import os
import json
import uuid
import fitz
import docx
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import uvicorn

# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DOCS_DIR = DATA_DIR / "documents"
DB_FILE  = DATA_DIR / "knowledge.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)

GROQ_MODEL = "llama-3.3-70b-versatile"

# ── DB helpers ─────────────────────────────────────────────────────────────
def load_db():
    if DB_FILE.exists():
        try:
            return json.loads(DB_FILE.read_text())
        except Exception:
            pass
    return {"documents": [], "conversations": []}

def save_db(db):
    DB_FILE.write_text(json.dumps(db, indent=2, default=str))

# ── Text extraction ────────────────────────────────────────────────────────
def extract_text(filepath: Path) -> str:
    suffix = filepath.suffix.lower()
    try:
        if suffix == ".pdf":
            doc  = fitz.open(str(filepath))
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
            return text
        elif suffix in [".docx", ".doc"]:
            d = docx.Document(str(filepath))
            return "\n".join(p.text for p in d.paragraphs if p.text.strip())
        else:
            return filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return "Error extracting: " + str(e)

# ── Groq client ────────────────────────────────────────────────────────────
def get_client():
    key = os.getenv("GROQ_API_KEY", "")
    if not key:
        raise HTTPException(400, "GROQ_API_KEY not set.")
    return Groq(api_key=key)

# ── Pydantic ───────────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    question: str
    history: Optional[List[dict]] = []

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    doc_count: int

# ── App ────────────────────────────────────────────────────────────────────
app = FastAPI(title="AI Second Brain", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"status": "running", "model": GROQ_MODEL}

@app.get("/health")
def health():
    db = load_db()
    return {"status": "healthy", "model": GROQ_MODEL,
            "documents": len(db["documents"]),
            "conversations": len(db["conversations"])}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    allowed = {".pdf", ".docx", ".doc", ".txt", ".md", ".csv"}
    suffix  = Path(file.filename).suffix.lower()
    if suffix not in allowed:
        raise HTTPException(400, "Unsupported file type: " + suffix)

    doc_id   = str(uuid.uuid4())[:8]
    filename = doc_id + "_" + file.filename
    filepath = DOCS_DIR / filename
    content  = await file.read()
    filepath.write_bytes(content)

    text       = extract_text(filepath)
    word_count = len(text.split())

    try:
        client = get_client()
        resp   = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user",
                       "content": "Summarize in 2 sentences:\n\n" + text[:3000]}],
            max_tokens=150, temperature=0.3,
        )
        summary = resp.choices[0].message.content
    except Exception as e:
        summary = "Uploaded successfully. " + str(word_count) + " words."

    db = load_db()
    db["documents"].append({
        "id":          doc_id,
        "filename":    file.filename,
        "stored_as":   filename,
        "size":        len(content),
        "word_count":  word_count,
        "summary":     summary,
        "uploaded_at": datetime.now().isoformat(),
        "text":        text[:60000],
    })
    save_db(db)

    return {"id": doc_id, "filename": file.filename,
            "word_count": word_count, "summary": summary}

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    db   = load_db()
    docs = db.get("documents", [])

    if not docs:
        return AskResponse(
            answer="No documents uploaded yet. Please upload some documents first!",
            sources=[], doc_count=0)

    context      = ""
    sources_used = []
    total        = 0
    limit        = 90000

    for doc in docs:
        text  = doc.get("text", "")
        block = "\n\n=== " + doc["filename"] + " ===\n" + text
        if total + len(block) > limit:
            left = limit - total
            if left > 500:
                context      += block[:left]
                sources_used.append(doc["filename"])
            break
        context      += block
        sources_used.append(doc["filename"])
        total        += len(block)

    system = (
        "You are the AI Second Brain — a brilliant personal knowledge assistant.\n"
        "You have the user's uploaded documents. Your job:\n"
        "1. Answer by synthesizing knowledge ACROSS all documents\n"
        "2. Connect ideas between different topics (SQL to Data Science, Stats to ML)\n"
        "3. Give structured answers with bullet points and numbered lists\n"
        "4. Mention which document information comes from\n"
        "5. Find smart non-obvious connections between topics\n"
        "Format responses clearly with sections and structure."
    )

    messages = [{"role": "system", "content": system}]
    for h in req.history[-6:]:
        messages.append({"role": h["role"], "content": h["content"]})

    user_msg = (
        "My uploaded documents:\n" + context +
        "\n\n---\nQuestion: " + req.question +
        "\n\nSynthesize knowledge from ALL relevant documents to answer."
    )
    messages.append({"role": "user", "content": user_msg})

    try:
        client = get_client()
        resp   = client.chat.completions.create(
            model=GROQ_MODEL, messages=messages,
            max_tokens=2048, temperature=0.4)
        answer = resp.choices[0].message.content
    except Exception as e:
        answer = "Groq API error: " + str(e)

    db = load_db()
    db["conversations"].append({
        "question": req.question,
        "answer":   answer[:500],
        "sources":  sources_used,
        "ts":       datetime.now().isoformat(),
    })
    if len(db["conversations"]) > 100:
        db["conversations"] = db["conversations"][-100:]
    save_db(db)

    return AskResponse(answer=answer, sources=sources_used, doc_count=len(docs))

@app.get("/documents")
def list_docs():
    db = load_db()
    return [{"id": d["id"], "filename": d["filename"],
             "word_count": d.get("word_count", 0),
             "summary": d.get("summary", ""),
             "size": d.get("size", 0),
             "uploaded_at": d.get("uploaded_at", "")}
            for d in db.get("documents", [])]

@app.delete("/documents/{doc_id}")
def delete_doc(doc_id: str):
    db  = load_db()
    doc = next((d for d in db["documents"] if d["id"] == doc_id), None)
    if not doc:
        raise HTTPException(404, "Not found.")
    try:
        (DOCS_DIR / doc["stored_as"]).unlink(missing_ok=True)
    except Exception:
        pass
    db["documents"] = [d for d in db["documents"] if d["id"] != doc_id]
    save_db(db)
    return {"message": "Deleted: " + doc["filename"]}

@app.get("/conversations")
def conversations():
    db = load_db()
    return db.get("conversations", [])[-20:]

@app.delete("/clear")
def clear_all():
    save_db({"documents": [], "conversations": []})
    for f in DOCS_DIR.glob("*"):
        try: f.unlink()
        except Exception: pass
    return {"message": "Cleared all data."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
