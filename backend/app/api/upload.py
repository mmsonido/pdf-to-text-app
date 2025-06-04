from fastapi import APIRouter, UploadFile, File, HTTPException
import uuid, pathlib, pdfplumber

router = APIRouter()

UPLOAD_DIR = pathlib.Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/api/v1/upload")
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