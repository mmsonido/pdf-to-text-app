from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import root, upload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(root.router)
app.include_router(upload.router)