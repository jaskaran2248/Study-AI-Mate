"""
StudyMate AI - Unified AI Generator & Orchestrator
Coordinates between local zero-dependency NLP engine and optional external LLMs (Gemini, OpenAI, Ollama).
Guarantees 100% offline functionality while offering live LLM enhancement when configured.
"""
import os
import json
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

from app.database import get_connection
from app.services.notes_engine import generate_study_notes
from app.services.question_engine import generate_tiered_quiz

def get_ai_setting(key: str, default: str = "") -> str:
    """Reads setting from SQLite settings table."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        row = cursor.fetchone()
        conn.close()
        return row['value'] if row else default
    except Exception:
        return default

def save_ai_setting(key: str, value: str):
    """Saves setting into SQLite settings table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()

def generate_notes_hybrid(text: str, title: str, subject: str = "General Studies") -> Dict[str, Any]:
    """
    Generates notes using configured provider (local or external LLM with automatic fallback).
    """
    provider = get_ai_setting("ai_provider", "local").lower()
    api_key = get_ai_setting("api_key", "").strip()

    if provider == "gemini" and api_key:
        try:
            llm_result = call_gemini_for_notes(text, title, subject, api_key)
            if llm_result:
                return llm_result
        except Exception as e:
            print(f"Gemini API fallback to local engine: {e}")

    elif provider == "openai" and api_key:
        try:
            llm_result = call_openai_for_notes(text, title, subject, api_key)
            if llm_result:
                return llm_result
        except Exception as e:
            print(f"OpenAI API fallback to local engine: {e}")

    return generate_study_notes(text, title, subject)

def generate_quiz_hybrid(
    text: str,
    title: str,
    difficulty_tier: str = "Adaptive Mix",
    question_count: int = 10,
    time_limit_min: int = 15,
    custom_topic: str = ""
) -> Dict[str, Any]:
    """
    Generates tiered quiz using configured provider with automatic local fallback.
    """
    provider = get_ai_setting("ai_provider", "local").lower()
    api_key = get_ai_setting("api_key", "").strip()

    if provider == "gemini" and api_key:
        try:
            llm_result = call_gemini_for_quiz(text, title, difficulty_tier, question_count, time_limit_min, api_key)
            if llm_result:
                return llm_result
        except Exception as e:
            print(f"Gemini Quiz fallback to local engine: {e}")

    elif provider == "openai" and api_key:
        try:
            llm_result = call_openai_for_quiz(text, title, difficulty_tier, question_count, time_limit_min, api_key)
            if llm_result:
                return llm_result
        except Exception as e:
            print(f"OpenAI Quiz fallback to local engine: {e}")

    return generate_tiered_quiz(text, title, difficulty_tier, question_count, time_limit_min, custom_topic)

# ==================== EXTERNAL LLM INTEGRATION HELPERS ====================

def call_gemini_for_notes(text: str, title: str, subject: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Calls Google Gemini API for structured note generation."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = f"""
    You are StudyMate AI, an adaptive educational AI system.
    Analyze the following text on '{title}' in subject '{subject}' and generate structured study notes in strictly valid JSON format.
    
    JSON Schema:
    {{
      "title": "{title}",
      "summary": "Crisp 2-3 sentence executive summary",
      "key_concepts": [
        {{
          "concept": "Name",
          "definition": "Clear explanation",
          "analogy": "Pedagogical real-world analogy",
          "real_world_application": "Practical usage",
          "practical_insight": "Core skill significance"
        }}
      ],
      "cheat_sheet": [
        {{
          "topic": "Rule or Theorem",
          "rules_or_formula": "Formula or syntax rule",
          "quick_tip": "High-yield memory tip"
        }}
      ],
      "flashcards": [
        {{
          "front": "Question/Prompt",
          "back": "Answer",
          "tag": "Category",
          "difficulty": "Basic or Intermediate or Advanced"
        }}
      ],
      "mindmap": "graph TD\\n  Root['{title}'] --> Node1['Concept']",
      "glossary": [
        {{"term": "Term", "definition": "Brief definition"}}
      ]
    }}
    
    Source Material:
    {text[:4000]}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=12) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))
        raw_json = res_data['candidates'][0]['content']['parts'][0]['text']
        return json.loads(raw_json)

def call_gemini_for_quiz(text: str, title: str, difficulty_tier: str, question_count: int, time_limit_min: int, api_key: str) -> Optional[Dict[str, Any]]:
    """Calls Google Gemini API for Bloom's tiered questions."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = f"""
    You are StudyMate AI. Generate {question_count} tiered questions ({difficulty_tier} progression) on '{title}' based on the source text below.
    Levels should span Basic (Recall), Intermediate (Apply), Advanced (Evaluate), Mastery (Create & Innovate).
    
    Return strictly JSON with schema:
    {{
      "title": "Quiz: {title}",
      "topic": "{title}",
      "description": "Comprehensive skill building assessment",
      "difficulty_tier": "{difficulty_tier}",
      "question_count": {question_count},
      "time_limit_min": {time_limit_min},
      "tags": "{title}, Core Skill",
      "questions": [
        {{
          "question_text": "Question stem",
          "question_type": "mcq",
          "difficulty": "basic",
          "bloom_level": "Remember",
          "options": ["Option A", "Option B", "Option C", "Option D"],
          "correct_answer": "Exact text of correct option",
          "explanation": "Detailed explanation of why right and why others are wrong",
          "hint": "Pedagogical hint",
          "points": 10,
          "subtopic": "Subtopic name"
        }}
      ]
    }}
    
    Source Material:
    {text[:4000]}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    with urllib.request.urlopen(req, timeout=12) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))
        raw_json = res_data['candidates'][0]['content']['parts'][0]['text']
        return json.loads(raw_json)

def call_openai_for_notes(text: str, title: str, subject: str, api_key: str) -> Optional[Dict[str, Any]]:
    """Calls OpenAI API for structured study notes."""
    url = "https://api.openai.com/v1/chat/completions"
    prompt = f"Analyze '{title}' in '{subject}' and output JSON study notes with summary, key_concepts, cheat_sheet, flashcards, mindmap (Mermaid graph TD), glossary. Content:\n{text[:4000]}"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are StudyMate AI, an adaptive educational intelligence system. Respond strictly in valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))
        return json.loads(res_data['choices'][0]['message']['content'])

def call_openai_for_quiz(text: str, title: str, difficulty_tier: str, question_count: int, time_limit_min: int, api_key: str) -> Optional[Dict[str, Any]]:
    """Calls OpenAI API for tiered questions."""
    url = "https://api.openai.com/v1/chat/completions"
    prompt = f"Generate a {question_count}-question quiz with tiered difficulty ({difficulty_tier}) on '{title}'. Return strictly valid JSON with questions list containing question_text, question_type, difficulty, bloom_level, options, correct_answer, explanation, hint, points, subtopic. Content:\n{text[:4000]}"
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "You are StudyMate AI. Return strictly valid JSON."},
            {"role": "user", "content": prompt}
        ],
        "response_format": {"type": "json_object"}
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        res_data = json.loads(resp.read().decode('utf-8'))
        return json.loads(res_data['choices'][0]['message']['content'])
