"""
StudyMate AI - Settings & AI Provider API Endpoints
"""
from fastapi import APIRouter
from app.models import SettingsUpdate
from app.services.ai_generator import get_ai_setting, save_ai_setting

router = APIRouter(prefix="/api/settings", tags=["Settings"])

@router.get("")
def get_settings():
    """Gets current AI provider configuration status."""
    provider = get_ai_setting("ai_provider", "local")
    api_key = get_ai_setting("api_key", "")
    masked_key = f"{api_key[:4]}...{api_key[-4:]}" if len(api_key) > 8 else ("Configured" if api_key else "")
    return {
        "ai_provider": provider,
        "api_key_configured": bool(api_key),
        "api_key_masked": masked_key
    }

@router.post("")
def update_settings(req: SettingsUpdate):
    """Updates AI provider configuration."""
    save_ai_setting("ai_provider", req.ai_provider)
    if req.api_key is not None:
        save_ai_setting("api_key", req.api_key.strip())
    return {
        "success": True,
        "ai_provider": req.ai_provider,
        "message": "Settings updated successfully."
    }
