from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os, uuid, pathlib
from PyPDF2 import PdfReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "API running"}

@app.get("/api/v1/health")
async def health():
    return {"status": "ok"}

UPLOAD_DIR = pathlib.Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/api/v1/upload")
async def upload(file: UploadFile = File(...)):
    # 1. Guarda el PDF
    file_id = f"{uuid.uuid4()}_{file.filename}"
    dest = UPLOAD_DIR / file_id
    with open(dest, "wb") as out:
        out.write(await file.read())

    # 2. Lee el PDF y extrae texto
    try:
        reader = PdfReader(str(dest))
        text_chunks = []
        for page in reader.pages:
            text_chunks.append(page.extract_text() or "")
        content = "\n".join(text_chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF error: {e}")

    # 3. Devuelve nombre de archivo + texto
    return {"saved_as": file_id, "text": content}