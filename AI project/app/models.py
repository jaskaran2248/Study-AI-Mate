"""
StudyMate AI - Pydantic Data Models & Schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DocumentCreate(BaseModel):
    title: str
    content: str
    subject: Optional[str] = "General"
    sdg_target: Optional[str] = "Core Curriculum"
    tags: Optional[str] = ""

class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    file_type: str
    word_count: int
    reading_time_min: float
    subject: str
    sdg_target: str
    tags: str
    created_at: str

class GenerateNotesRequest(BaseModel):
    document_id: Optional[int] = None
    custom_text: Optional[str] = None
    title: Optional[str] = None
    subject: Optional[str] = "General"

class FlashcardItem(BaseModel):
    front: str
    back: str
    tag: Optional[str] = "Key Term"
    difficulty: Optional[str] = "Basic"

class ConceptItem(BaseModel):
    concept: str
    definition: str
    analogy: str
    real_world_application: str
    practical_insight: Optional[str] = "Applied Core Competency"

class CheatSheetItem(BaseModel):
    topic: str
    rules_or_formula: str
    quick_tip: str

class GlossaryItem(BaseModel):
    term: str
    definition: str

class NotesResponse(BaseModel):
    id: int
    document_id: Optional[int]
    title: str
    summary: str
    key_concepts: List[ConceptItem]
    cheat_sheet: List[CheatSheetItem]
    flashcards: List[FlashcardItem]
    mindmap: str
    glossary: List[GlossaryItem]
    created_at: str

class GenerateQuizRequest(BaseModel):
    document_id: Optional[int] = None
    custom_text: Optional[str] = None
    topic: Optional[str] = None
    difficulty_tier: str = "Adaptive Mix" # "Basic", "Intermediate", "Advanced", "Mastery", "Adaptive Mix"
    question_count: int = 10
    time_limit_min: int = 15
    question_types: Optional[List[str]] = ["mcq", "tf", "fill", "open"]

class QuestionItem(BaseModel):
    id: Optional[int] = None
    question_text: str
    question_type: str  # mcq, tf, fill, open
    difficulty: str     # basic, intermediate, advanced, mastery
    bloom_level: str    # Remember, Understand, Apply, Analyze, Evaluate, Create
    options: List[str]
    correct_answer: str
    explanation: str
    hint: Optional[str] = ""
    points: int = 10
    subtopic: Optional[str] = ""

class QuizResponse(BaseModel):
    id: int
    document_id: Optional[int]
    title: str
    topic: str
    description: str
    difficulty_tier: str
    question_count: int
    time_limit_min: int
    tags: str
    questions: List[QuestionItem]
    created_at: str

class SubmitQuizRequest(BaseModel):
    quiz_id: int
    time_spent_sec: int
    answers: Dict[str, Any] # question_id (str) -> selected answer (str)

class QuizAttemptResult(BaseModel):
    attempt_id: int
    quiz_id: int
    score: float
    max_score: float
    percentage: float
    time_spent_sec: int
    difficulty_breakdown: Dict[str, Dict[str, Any]]
    ai_feedback: str
    remediation_topics: List[str]
    xp_earned: int
    new_mastery_level: str
    review: List[Dict[str, Any]]

class SearchRequest(BaseModel):
    query: str
    difficulty: Optional[str] = "all"
    category: Optional[str] = "all"
    limit: Optional[int] = 20

class SettingsUpdate(BaseModel):
    ai_provider: str = "local" # "local", "gemini", "openai"
    api_key: Optional[str] = ""
    model_name: Optional[str] = ""
