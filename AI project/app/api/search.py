"""
StudyMate AI - Search & Discovery API Endpoints
Enables users to search across uploaded documents, notes, question banks,
and instantly generate full study packs & tiered quizzes from any search query.
"""
import json
from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any, List
from app.database import get_connection
from app.services.ai_generator import generate_notes_hybrid, generate_quiz_hybrid

router = APIRouter(prefix="/api/search", tags=["Search"])

@router.get("")
def search_all(
    q: str = Query("", description="Search keywords or concepts"),
    difficulty: str = Query("all", description="Difficulty filter"),
    category: str = Query("all", description="Category filter")
):
    """
    Unified multi-entity search across documents, notes, quizzes, and individual questions.
    """
    query = q.strip()
    conn = get_connection()
    cursor = conn.cursor()

    if not query:
        cursor.execute("SELECT id, title, subject, sdg_target, reading_time_min FROM documents ORDER BY created_at DESC LIMIT 5")
        docs = [dict(r) for r in cursor.fetchall()]
        cursor.execute("SELECT id, title, difficulty_tier, question_count FROM quizzes ORDER BY created_at DESC LIMIT 5")
        quizzes = [dict(r) for r in cursor.fetchall()]
        conn.close()
        return {
            "query": "",
            "results": {
                "documents": docs,
                "quizzes": quizzes,
                "notes": [],
                "questions": []
            },
            "total_matches": len(docs) + len(quizzes)
        }

    search_param = f"%{query}%"

    cursor.execute("""
    SELECT id, title, filename, file_type, subject, sdg_target, tags, word_count
    FROM documents
    WHERE title LIKE ? OR tags LIKE ? OR content LIKE ? OR subject LIKE ?
    LIMIT 10
    """, (search_param, search_param, search_param, search_param))
    documents = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
    SELECT id, document_id, title, summary, created_at
    FROM notes
    WHERE title LIKE ? OR summary LIKE ? OR key_concepts LIKE ?
    LIMIT 10
    """, (search_param, search_param, search_param))
    notes = [dict(r) for r in cursor.fetchall()]

    cursor.execute("""
    SELECT id, document_id, title, topic, difficulty_tier, question_count, tags
    FROM quizzes
    WHERE title LIKE ? OR topic LIKE ? OR tags LIKE ? OR description LIKE ?
    LIMIT 10
    """, (search_param, search_param, search_param, search_param))
    quizzes = [dict(r) for r in cursor.fetchall()]

    q_sql = """
    SELECT q.id, q.quiz_id, q.question_text, q.difficulty, q.bloom_level, q.subtopic,
           qz.title as quiz_title
    FROM questions q
    JOIN quizzes qz ON q.quiz_id = qz.id
    WHERE (q.question_text LIKE ? OR q.explanation LIKE ? OR q.subtopic LIKE ?)
    """
    params = [search_param, search_param, search_param]
    if difficulty.lower() != "all":
        q_sql += " AND LOWER(q.difficulty) = ?"
        params.append(difficulty.lower())
    q_sql += " LIMIT 15"

    cursor.execute(q_sql, tuple(params))
    questions = [dict(r) for r in cursor.fetchall()]

    conn.close()

    total = len(documents) + len(notes) + len(quizzes) + len(questions)

    return {
        "query": query,
        "results": {
            "documents": documents,
            "notes": notes,
            "quizzes": quizzes,
            "questions": questions
        },
        "total_matches": total
    }

@router.post("/generate-from-topic")
def generate_from_topic(payload: Dict[str, Any]):
    """
    Instantly generates both study notes and a tiered quiz from any user-searched topic!
    """
    topic = payload.get("topic", "").strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Please enter a topic.")

    difficulty = payload.get("difficulty_tier", "Adaptive Mix")
    subject = payload.get("subject", "STEM & Core Studies")

    text_content = f"""# {topic}

Comprehensive Curriculum & Skill Study Guide on {topic}.

Core Concept: {topic} represents a foundational domain within {subject}. Mastery of this subject requires understanding underlying principles, architectural mechanics, and practical applications.
Key Mechanism: The internal behavior of {topic} is governed by structured operational rules, state transformations, and input/output parameters.
System Design & Optimization: Engineers and practitioners optimize {topic} by analyzing efficiency bottlenecks, ensuring high fault tolerance, and maintaining deterministic execution.
Practical Applications: Applied extensively in real-world scenarios to deliver resilient, scalable, and verifiable technical solutions.
Skill Impact: Mastering {topic} develops technical literacy, critical problem-solving skills, and workforce readiness.
"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO documents (
        title, filename, file_type, content, word_count,
        reading_time_min, subject, sdg_target, tags
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"Guide: {topic}", f"{topic.lower().replace(' ', '_')}.md", "md",
        text_content, 120, 1.0, subject, "Core Curriculum", f"{topic}, Education, Skills"
    ))
    doc_id = cursor.lastrowid

    notes_data = generate_notes_hybrid(text_content, topic, subject)
    cursor.execute("""
    INSERT INTO notes (
        document_id, title, summary, key_concepts,
        cheat_sheet, flashcards, mindmap, glossary
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        doc_id, notes_data['title'], notes_data['summary'],
        json.dumps(notes_data['key_concepts']),
        json.dumps(notes_data['cheat_sheet']),
        json.dumps(notes_data['flashcards']),
        notes_data['mindmap'],
        json.dumps(notes_data['glossary'])
    ))
    notes_id = cursor.lastrowid
    notes_data['id'] = notes_id

    quiz_data = generate_quiz_hybrid(
        text=text_content,
        title=topic,
        difficulty_tier=difficulty,
        question_count=8,
        time_limit_min=10,
        custom_topic=topic
    )
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
    quiz_data['id'] = quiz_id

    saved_qs = []
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
        q_copy = dict(q)
        q_copy['id'] = cursor.lastrowid
        saved_qs.append(q_copy)

    conn.commit()
    conn.close()

    quiz_data['questions'] = saved_qs

    return {
        "success": True,
        "topic": topic,
        "document_id": doc_id,
        "notes": notes_data,
        "quiz": quiz_data
    }
