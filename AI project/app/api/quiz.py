"""
StudyMate AI - Quiz API Endpoints
"""
import json
from fastapi import APIRouter, HTTPException
from typing import Optional, List
from app.database import get_connection
from app.models import GenerateQuizRequest, SubmitQuizRequest
from app.services.ai_generator import generate_quiz_hybrid
from app.services.skill_tracker import record_quiz_attempt

router = APIRouter(prefix="/api/quiz", tags=["Quiz"])

@router.post("/generate")
def generate_quiz_endpoint(req: GenerateQuizRequest):
    """
    Generates a Basic to Advanced tiered quiz from a document ID, topic, or custom text.
    """
    conn = get_connection()
    cursor = conn.cursor()

    text_to_process = ""
    title = req.topic or "Subject Mastery Quiz"
    custom_topic = req.topic or ""
    doc_id = req.document_id

    if doc_id:
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        doc = cursor.fetchone()
        if not doc:
            conn.close()
            raise HTTPException(status_code=404, detail="Document not found")
        text_to_process = doc['content']
        title = doc['title']
        custom_topic = doc['title']
    elif req.custom_text and req.custom_text.strip():
        text_to_process = req.custom_text.strip()
    elif req.topic and req.topic.strip():
        # Synthesize from topic query
        text_to_process = f"Comprehensive curriculum on {req.topic}. Key concepts, design principles, practical scenarios, and evaluation criteria for {req.topic}."
        title = req.topic
        custom_topic = req.topic
    else:
        conn.close()
        raise HTTPException(status_code=400, detail="Provide document_id, topic, or custom_text.")

    # Call AI generation
    quiz_data = generate_quiz_hybrid(
        text=text_to_process,
        title=title,
        difficulty_tier=req.difficulty_tier,
        question_count=req.question_count,
        time_limit_min=req.time_limit_min,
        custom_topic=custom_topic
    )

    # Save Quiz to Database
    cursor.execute("""
    INSERT INTO quizzes (
        document_id, title, topic, description,
        difficulty_tier, question_count, time_limit_min, tags
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        doc_id, quiz_data['title'], quiz_data['topic'],
        quiz_data['description'], quiz_data['difficulty_tier'],
        len(quiz_data['questions']), quiz_data['time_limit_min'],
        quiz_data['tags']
    ))
    quiz_id = cursor.lastrowid

    # Insert Questions
    saved_questions = []
    for q in quiz_data['questions']:
        cursor.execute("""
        INSERT INTO questions (
            quiz_id, question_text, question_type, difficulty,
            bloom_level, options, correct_answer, explanation,
            hint, points, subtopic
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            quiz_id, q['question_text'], q['question_type'],
            q['difficulty'], q['bloom_level'],
            json.dumps(q['options']), q['correct_answer'],
            q['explanation'], q.get('hint', ''),
            q.get('points', 10), q.get('subtopic', '')
        ))
        q_id = cursor.lastrowid
        q_copy = dict(q)
        q_copy['id'] = q_id
        saved_questions.append(q_copy)

    conn.commit()
    conn.close()

    quiz_data['id'] = quiz_id
    quiz_data['document_id'] = doc_id
    quiz_data['questions'] = saved_questions
    return quiz_data

@router.get("")
def list_quizzes():
    """Returns all available quizzes."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT q.*, d.subject, 
           (SELECT COUNT(*) FROM questions WHERE quiz_id = q.id) as actual_question_count,
           (SELECT MAX(percentage) FROM quiz_attempts WHERE quiz_id = q.id) as best_score
    FROM quizzes q
    LEFT JOIN documents d ON q.document_id = d.id
    ORDER BY q.created_at DESC
    """)
    quizzes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return {"quizzes": quizzes}

@router.get("/{quiz_id}")
def get_quiz(quiz_id: int):
    """Retrieves full quiz including questions with parsed options."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
    quiz = cursor.fetchone()
    if not quiz:
        conn.close()
        raise HTTPException(status_code=404, detail="Quiz not found")

    cursor.execute("SELECT * FROM questions WHERE quiz_id = ? ORDER BY id ASC", (quiz_id,))
    rows = cursor.fetchall()
    conn.close()

    questions = []
    for r in rows:
        qd = dict(r)
        try:
            qd['options'] = json.loads(qd['options'])
        except Exception:
            qd['options'] = []
        questions.append(qd)

    result = dict(quiz)
    result['questions'] = questions
    return result

@router.post("/submit")
def submit_quiz(req: SubmitQuizRequest):
    """
    Submits a completed quiz attempt, calculates scores, updates skills, and generates feedback.
    """
    try:
        result = record_quiz_attempt(
            quiz_id=req.quiz_id,
            time_spent_sec=req.time_spent_sec,
            user_answers=req.answers
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/remediation")
def create_remediation_quiz(topics: List[str], base_quiz_id: Optional[int] = None):
    """
    Generates a targeted remediation quiz focused specifically on the student's missed concepts.
    """
    if not topics:
        raise HTTPException(status_code=400, detail="No remediation topics provided.")

    combined_topic = ", ".join(topics[:3])
    text_content = f"Targeted remediation drill focusing on learning gaps in: {combined_topic}. Clear foundational definitions, intermediate applications, and common pitfalls."

    req = GenerateQuizRequest(
        topic=f"Remediation: {combined_topic}",
        custom_text=text_content,
        difficulty_tier="Adaptive Mix",
        question_count=min(6, max(4, len(topics) * 2)),
        time_limit_min=10
    )
    return generate_quiz_endpoint(req)
