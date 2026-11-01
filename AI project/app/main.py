"""
StudyMate AI - Main FastAPI Application
Adaptive Learning Platform | Quizzes & Active Study Notes
"""
import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.services.sample_data import seed_sample_data
from app.api.upload import router as upload_router
from app.api.notes import router as notes_router
from app.api.quiz import router as quiz_router
from app.api.search import router as search_router
from app.api.skills import router as skills_router
from app.api.settings import router as settings_router

app = FastAPI(
    title="StudyMate AI",
    description="Adaptive Quiz & Study Notes Generation Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(notes_router)
app.include_router(quiz_router)
app.include_router(search_router)
app.include_router(skills_router)
app.include_router(settings_router)

static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.on_event("startup")
def on_startup():
    """Initializes database schema and populates curated starter modules."""
    init_db()
    seed_sample_data()

@app.get("/api/health")
def health_check():
    """Health and readiness check endpoint."""
    return {
        "status": "healthy",
        "app": "StudyMate AI",
        "version": "1.0.0"
    }

@app.get("/")
def root():
    """Serves the main single page interactive application."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "StudyMate AI API is online. Loading UI..."})
