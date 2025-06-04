from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "API running"}

@router.get("/api/v1/health")
async def health():
    return {"status": "ok"} 