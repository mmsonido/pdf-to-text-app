from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os, uuid, pathlib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # en prod restringe dominios
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
    fname = UPLOAD_DIR / f"{uuid.uuid4()}_{file.filename}"
    with open(fname, "wb") as out:
        out.write(await file.read())
    return {"saved_as": fname.name}