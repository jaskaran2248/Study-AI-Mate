"""
StudyMate AI - Skill Tracker & Competency Engine
Calculates Bloom's taxonomy mastery, XP, learner progression, and identifies learning gaps.
Generates personalized remediation roadmaps for target concept reinforcement.
"""
import json
import sqlite3
from typing import Dict, Any, List, Tuple
from app.database import get_connection

XP_TABLE = {
    "basic": 10,
    "intermediate": 15,
    "advanced": 25,
    "mastery": 40
}

MASTERY_LEVELS = [
    (0, "Novice Learner", "🌱"),
    (25, "Apprentice Scholar", "🌿"),
    (50, "Proficient Practitioner", "⚡"),
    (75, "Advanced Specialist", "⭐"),
    (90, "Master Strategist & Grandmaster", "🏆")
]

def record_quiz_attempt(
    quiz_id: int,
    time_spent_sec: int,
    user_answers: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Evaluates quiz answers, updates skill competencies, calculates XP, and flags remediation topics.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM quizzes WHERE id = ?", (quiz_id,))
    quiz = cursor.fetchone()
    if not quiz:
        conn.close()
        raise ValueError("Quiz not found")

    cursor.execute("SELECT * FROM questions WHERE quiz_id = ?", (quiz_id,))
    questions = cursor.fetchall()

    total_score = 0.0
    max_score = 0.0
    tier_stats = {
        "basic": {"correct": 0, "total": 0, "points_earned": 0, "points_max": 0},
        "intermediate": {"correct": 0, "total": 0, "points_earned": 0, "points_max": 0},
        "advanced": {"correct": 0, "total": 0, "points_earned": 0, "points_max": 0},
        "mastery": {"correct": 0, "total": 0, "points_earned": 0, "points_max": 0}
    }

    remediation_topics = []
    review_items = []
    xp_earned = 0

    for q in questions:
        q_id = str(q['id'])
        q_diff = q['difficulty'].lower()
        if q_diff not in tier_stats:
            q_diff = "intermediate"
            
        q_points = q['points'] or 10
        max_score += q_points
        tier_stats[q_diff]["total"] += 1
        tier_stats[q_diff]["points_max"] += q_points

        user_ans = user_answers.get(q_id, "").strip()
        correct_ans = q['correct_answer'].strip()

        is_correct = False
        if q['question_type'] == 'tf':
            is_correct = user_ans.lower() == correct_ans.lower()
        elif q['question_type'] == 'mcq':
            is_correct = (user_ans.lower() == correct_ans.lower()) or (user_ans == correct_ans)
        else:
            clean_u = user_ans.lower()
            clean_c = correct_ans.lower()
            is_correct = (clean_c in clean_u) or (clean_u in clean_c and len(clean_u) > 3)

        if is_correct:
            total_score += q_points
            tier_stats[q_diff]["correct"] += 1
            tier_stats[q_diff]["points_earned"] += q_points
            xp_earned += XP_TABLE.get(q_diff, 10)
        else:
            subtopic = q['subtopic'] or quiz['topic']
            if subtopic and subtopic not in remediation_topics:
                remediation_topics.append(subtopic)

        review_items.append({
            "question_id": q['id'],
            "question_text": q['question_text'],
            "difficulty": q['difficulty'],
            "bloom_level": q['bloom_level'],
            "user_answer": user_ans,
            "correct_answer": correct_ans,
            "is_correct": is_correct,
            "explanation": q['explanation'],
            "hint": q['hint'],
            "subtopic": q['subtopic']
        })

    percentage = round((total_score / max_score * 100), 1) if max_score > 0 else 0.0

    feedback = generate_performance_feedback(percentage, tier_stats, quiz['topic'])

    cursor.execute("""
    INSERT INTO quiz_attempts (
        quiz_id, score, max_score, percentage, time_spent_sec,
        difficulty_breakdown, answers, ai_feedback, remediation_topics
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        quiz_id, total_score, max_score, percentage, time_spent_sec,
        json.dumps(tier_stats), json.dumps(user_answers), feedback, json.dumps(remediation_topics)
    ))
    attempt_id = cursor.lastrowid

    skill_name = quiz['topic'] or "General Competency"
    update_skill_stats(cursor, skill_name, tier_stats, xp_earned)

    conn.commit()

    cursor.execute("SELECT mastery_level FROM user_skills WHERE skill_name = ?", (skill_name,))
    row = cursor.fetchone()
    current_mastery = row['mastery_level'] if row else "Apprentice Scholar"

    conn.close()

    return {
        "attempt_id": attempt_id,
        "quiz_id": quiz_id,
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "time_spent_sec": time_spent_sec,
        "difficulty_breakdown": tier_stats,
        "ai_feedback": feedback,
        "remediation_topics": remediation_topics,
        "xp_earned": xp_earned,
        "new_mastery_level": current_mastery,
        "review": review_items
    }

def update_skill_stats(cursor, skill_name: str, tier_stats: Dict[str, Any], xp_earned: int):
    """Updates user_skills table with cumulative mastery scores."""
    cursor.execute("SELECT * FROM user_skills WHERE skill_name = ?", (skill_name,))
    existing = cursor.fetchone()

    total_attempted = sum(t["total"] for t in tier_stats.values())
    total_correct = sum(t["correct"] for t in tier_stats.values())

    if existing:
        new_xp = existing['xp'] + xp_earned
        new_attempted = existing['total_attempted'] + total_attempted
        new_correct = existing['total_correct'] + total_correct
        
        b_pct = (tier_stats['basic']['correct'] / max(1, tier_stats['basic']['total'])) * 100 if tier_stats['basic']['total'] > 0 else existing['basic_score']
        i_pct = (tier_stats['intermediate']['correct'] / max(1, tier_stats['intermediate']['total'])) * 100 if tier_stats['intermediate']['total'] > 0 else existing['intermediate_score']
        a_pct = (tier_stats['advanced']['correct'] / max(1, tier_stats['advanced']['total'])) * 100 if tier_stats['advanced']['total'] > 0 else existing['advanced_score']
        m_pct = (tier_stats['mastery']['correct'] / max(1, tier_stats['mastery']['total'])) * 100 if tier_stats['mastery']['total'] > 0 else existing['mastery_score']

        overall_pct = round((b_pct * 0.20) + (i_pct * 0.30) + (a_pct * 0.30) + (m_pct * 0.20), 1)

        level_title = "Novice Learner"
        for thresh, title, icon in MASTERY_LEVELS:
            if overall_pct >= thresh:
                level_title = f"{icon} {title}"

        cursor.execute("""
        UPDATE user_skills SET
            mastery_level = ?,
            mastery_percent = ?,
            xp = ?,
            total_attempted = ?,
            total_correct = ?,
            basic_score = ?,
            intermediate_score = ?,
            advanced_score = ?,
            mastery_score = ?,
            last_practiced = CURRENT_TIMESTAMP
        WHERE skill_name = ?
        """, (
            level_title, overall_pct, new_xp, new_attempted, new_correct,
            b_pct, i_pct, a_pct, m_pct, skill_name
        ))
    else:
        b_pct = (tier_stats['basic']['correct'] / max(1, tier_stats['basic']['total'])) * 100 if tier_stats['basic']['total'] > 0 else 0
        i_pct = (tier_stats['intermediate']['correct'] / max(1, tier_stats['intermediate']['total'])) * 100 if tier_stats['intermediate']['total'] > 0 else 0
        a_pct = (tier_stats['advanced']['correct'] / max(1, tier_stats['advanced']['total'])) * 100 if tier_stats['advanced']['total'] > 0 else 0
        m_pct = (tier_stats['mastery']['correct'] / max(1, tier_stats['mastery']['total'])) * 100 if tier_stats['mastery']['total'] > 0 else 0
        
        overall_pct = round((b_pct * 0.20) + (i_pct * 0.30) + (a_pct * 0.30) + (m_pct * 0.20), 1)
        
        level_title = "Novice Learner"
        for thresh, title, icon in MASTERY_LEVELS:
            if overall_pct >= thresh:
                level_title = f"{icon} {title}"

        cursor.execute("""
        INSERT INTO user_skills (
            skill_name, category, mastery_level, mastery_percent, xp,
            total_attempted, total_correct, basic_score, intermediate_score,
            advanced_score, mastery_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            skill_name, "Core Sciences & Technical Domains", level_title, overall_pct, xp_earned,
            total_attempted, total_correct, b_pct, i_pct, a_pct, m_pct
        ))

def generate_performance_feedback(score_pct: float, tier_stats: Dict[str, Any], topic: str) -> str:
    """Generates personalized pedagogical feedback."""
    if score_pct >= 90:
        return f"Outstanding mastery in {topic}! You demonstrated flawless recall and superior problem synthesis. You are fully prepared to tackle advanced capstone architectures."
    elif score_pct >= 75:
        return f"Great performance in {topic}! Your foundational and applied skills are solid. Focus on refining edge-case analysis in advanced scenarios to reach top-tier mastery."
    elif score_pct >= 50:
        return f"Good foundational progress in {topic}. While your basic recall is solid, scenario-based applications and trade-off evaluations require additional active revision. Review the auto-generated flashcards."
    else:
        return f"Valuable learning benchmark in {topic}. Review the study notes and take the targeted remediation quiz to cement core foundational concepts."

def get_learner_dashboard_data() -> Dict[str, Any]:
    """Retrieves all skill data, badges, total XP, and activity history."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM user_skills ORDER BY xp DESC")
    skills = [dict(row) for row in cursor.fetchall()]

    cursor.execute("""
    SELECT qa.*, q.title as quiz_title, q.topic as quiz_topic 
    FROM quiz_attempts qa
    JOIN quizzes q ON qa.quiz_id = q.id
    ORDER BY qa.created_at DESC LIMIT 10
    """)
    attempts = []
    for row in cursor.fetchall():
        d = dict(row)
        try:
            d['difficulty_breakdown'] = json.loads(d['difficulty_breakdown'])
            d['remediation_topics'] = json.loads(d['remediation_topics'])
        except Exception:
            pass
        attempts.append(d)

    total_xp = sum(s['xp'] for s in skills)
    total_quizzes_taken = len(attempts)
    avg_accuracy = round(sum(a['percentage'] for a in attempts) / max(1, len(attempts)), 1) if attempts else 0.0

    badges = [
        {
            "id": "starter",
            "name": "Dedicated Learner",
            "desc": "Began the skill building journey with StudyMate AI",
            "icon": "🎓",
            "unlocked": total_quizzes_taken >= 1
        },
        {
            "id": "foundation",
            "name": "Foundations Master",
            "desc": "Achieved 80%+ on Basic tier recall questions",
            "icon": "🧱",
            "unlocked": any(s.get('basic_score', 0) >= 80 for s in skills)
        },
        {
            "id": "applied",
            "name": "Applied Problem Solver",
            "desc": "Conquered Intermediate scenario challenges",
            "icon": "⚙️",
            "unlocked": any(s.get('intermediate_score', 0) >= 70 for s in skills)
        },
        {
            "id": "architect",
            "name": "Advanced Synthesizer",
            "desc": "Mastered complex edge cases and architectural evaluation",
            "icon": "🧠",
            "unlocked": any(s.get('advanced_score', 0) >= 60 for s in skills)
        },
        {
            "id": "champion",
            "name": "Mastery Scholar",
            "desc": "Earned over 300 XP across multiple competencies",
            "icon": "🏆",
            "unlocked": total_xp >= 300
        }
    ]

    conn.close()

    return {
        "skills": skills,
        "recent_attempts": attempts,
        "total_xp": total_xp,
        "quizzes_completed": total_quizzes_taken,
        "average_accuracy": avg_accuracy,
        "badges": badges
    }
