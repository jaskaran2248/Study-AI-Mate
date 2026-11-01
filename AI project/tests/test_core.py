"""
StudyMate AI - Automated Test Suite
Verifies extraction, note generation, tiered quiz generation, skill scoring, and API route handlers.
"""
import unittest
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_db, get_connection
from app.services.sample_data import seed_sample_data
from app.services.text_extractor import extract_plain_text, compute_document_metadata
from app.services.notes_engine import generate_study_notes
from app.services.question_engine import generate_tiered_quiz
from app.services.skill_tracker import record_quiz_attempt, get_learner_dashboard_data
from app.api.upload import list_documents
from app.api.search import search_all, generate_from_topic
from app.api.quiz import list_quizzes, get_quiz, submit_quiz
from app.models import SubmitQuizRequest

class TestStudyMateAI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        seed_sample_data()

    def test_01_database_tables_exist(self):
        """Verifies all required SQLite tables exist."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row['name'] for row in cursor.fetchall()]
        conn.close()

        required = ['documents', 'notes', 'quizzes', 'questions', 'quiz_attempts', 'user_skills', 'settings']
        for r in required:
            self.assertIn(r, tables, f"Table {r} should exist in database")

    def test_02_text_extractor_and_metadata(self):
        """Tests metadata computation and domain classification."""
        sample_text = (
            "Algorithms and data structures are foundational to computer science. "
            "Python enables rapid development and computational literacy. "
            "Binary search achieves logarithmic time complexity O(log n)."
        )
        meta = compute_document_metadata(sample_text)
        self.assertGreater(meta['word_count'], 10)
        self.assertIn("Computer Science", meta['sdg_target'])

    def test_03_notes_generation(self):
        """Tests comprehensive notes synthesis (analogy, cheat sheet, flashcards, mindmap)."""
        content = """# Artificial Intelligence in Modern Education
Machine Learning: Algorithms that learn from observational data without explicit programming.
Supervised Learning: Training models using labeled input-output pairs.
Neural Networks: Layered computational architectures inspired by biological synapses.
Practical Significance: Enhances adaptive personalized tutoring and automated feedback globally."""
        notes = generate_study_notes(content, "AI in Education", "Computer Science")
        self.assertTrue(len(notes['summary']) > 10)
        self.assertTrue(len(notes['key_concepts']) > 0)
        self.assertTrue(len(notes['flashcards']) > 0)
        self.assertTrue(len(notes['cheat_sheet']) > 0)
        self.assertIn("graph TD", notes['mindmap'])

    def test_04_tiered_quiz_generation(self):
        """Verifies 4-tier Bloom's taxonomy quiz generation."""
        content = """Photosynthesis is the biological process by which plants convert light energy into chemical energy.
Chloroplasts: The cellular organelle where photosynthesis occurs.
Light Reactions: Solar energy hydrolyzes water, generating ATP and NADPH while releasing oxygen.
Calvin Cycle: Carbon fixation pathways that synthesize glucose using ATP and NADPH."""
        quiz = generate_tiered_quiz(
            text=content,
            title="Photosynthesis Fundamentals",
            difficulty_tier="Adaptive Mix",
            question_count=6,
            time_limit_min=10
        )
        self.assertEqual(len(quiz['questions']), 6)
        
        tiers_present = set(q['difficulty'] for q in quiz['questions'])
        self.assertTrue(len(tiers_present) >= 2, "Quiz should contain multiple difficulty tiers")
        for q in quiz['questions']:
            self.assertTrue(len(q['options']) >= 2)
            self.assertTrue(len(q['explanation']) > 10)
            self.assertIn(q['correct_answer'], q['options'])

    def test_05_api_list_documents(self):
        """Tests document listing endpoint."""
        res = list_documents()
        self.assertIn("documents", res)
        self.assertGreater(len(res["documents"]), 0)

    def test_06_instant_search_and_generate_topic(self):
        """Tests generating a study pack and tiered quiz from any user search query."""
        search_res = search_all(q="Python", difficulty="all", category="all")
        self.assertIn("results", search_res)
        self.assertGreater(search_res["total_matches"], 0)

        payload = {
            "topic": "Quantum Computing Basics",
            "difficulty_tier": "Adaptive Mix",
            "subject": "Physics & Computing"
        }
        gen_res = generate_from_topic(payload)
        self.assertTrue(gen_res['success'])
        self.assertIn('notes', gen_res)
        self.assertIn('quiz', gen_res)
        self.assertTrue(len(gen_res['quiz']['questions']) > 0)

    def test_07_quiz_submission_and_skill_scoring(self):
        """Tests quiz submission, XP calculation, Bloom's scoring, and remediation detection."""
        quizzes_res = list_quizzes()
        quizzes = quizzes_res.get('quizzes', [])
        self.assertTrue(len(quizzes) > 0, "There should be at least one quiz")
        quiz_id = quizzes[0]['id']

        quiz_detail = get_quiz(quiz_id)
        questions = quiz_detail['questions']
        self.assertTrue(len(questions) > 0)

        answers = {
            str(questions[0]['id']): questions[0]['correct_answer'],
        }
        if len(questions) > 1:
            answers[str(questions[1]['id'])] = "Deliberately wrong answer for remediation test"

        sub_req = SubmitQuizRequest(
            quiz_id=quiz_id,
            time_spent_sec=45,
            answers=answers
        )
        attempt = submit_quiz(sub_req)
        self.assertGreaterEqual(attempt['score'], 0)
        self.assertGreater(attempt['xp_earned'], 0)
        self.assertIn('difficulty_breakdown', attempt)
        self.assertIn('ai_feedback', attempt)

        dash = get_learner_dashboard_data()
        self.assertGreater(dash['total_xp'], 0)
        self.assertGreater(dash['quizzes_completed'], 0)

if __name__ == '__main__':
    unittest.main()
