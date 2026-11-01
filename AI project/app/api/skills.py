"""
StudyMate AI - Skills & Learner Analytics API Endpoints
"""
from fastapi import APIRouter
from app.services.skill_tracker import get_learner_dashboard_data

router = APIRouter(prefix="/api/skills", tags=["Skills & Analytics"])

@router.get("/dashboard")
def get_dashboard():
    """Returns user skill mastery tree, badges, total XP, and past attempts."""
    return get_learner_dashboard_data()
