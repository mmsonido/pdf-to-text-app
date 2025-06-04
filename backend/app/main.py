from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid, pathlib, pdfplumber

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
    file_id = f"{uuid.uuid4()}_{file.filename}"
    dest = UPLOAD_DIR / file_id
    with open(dest, "wb") as out:
        out.write(await file.read())

    try:
        content = ""
        with pdfplumber.open(dest) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF error: {e}")

    return {"saved_as": file_id, "text": content}