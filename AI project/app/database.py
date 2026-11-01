"""
StudyMate AI - Database Layer
SQLite storage for documents, notes, quizzes, questions, attempts, skills, and configuration.
"""
import sqlite3
import json
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "studymate.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        content TEXT NOT NULL,
        word_count INTEGER DEFAULT 0,
        reading_time_min REAL DEFAULT 0.0,
        subject TEXT DEFAULT 'General',
        sdg_target TEXT DEFAULT 'SDG 4.4 - Skill Building',
        tags TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Notes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        key_concepts TEXT NOT NULL,     -- JSON array
        cheat_sheet TEXT NOT NULL,      -- JSON array
        flashcards TEXT NOT NULL,       -- JSON array
        mindmap TEXT NOT NULL,          -- Markdown / Mermaid
        glossary TEXT NOT NULL,         -- JSON array
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE CASCADE
    )
    """)

    # Quizzes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        document_id INTEGER,
        title TEXT NOT NULL,
        topic TEXT NOT NULL,
        description TEXT DEFAULT '',
        difficulty_tier TEXT DEFAULT 'Adaptive Mix',
        question_count INTEGER DEFAULT 10,
        time_limit_min INTEGER DEFAULT 15,
        tags TEXT DEFAULT '',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE SET NULL
    )
    """)

    # Questions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        question_text TEXT NOT NULL,
        question_type TEXT DEFAULT 'mcq',  -- mcq, tf, fill, open
        difficulty TEXT NOT NULL,          -- basic, intermediate, advanced, mastery
        bloom_level TEXT NOT NULL,         -- Remember, Understand, Apply, Analyze, Evaluate, Create
        options TEXT NOT NULL,             -- JSON array of strings
        correct_answer TEXT NOT NULL,      -- string or JSON
        explanation TEXT NOT NULL,
        hint TEXT DEFAULT '',
        points INTEGER DEFAULT 10,
        subtopic TEXT DEFAULT '',
        FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
    )
    """)

    # Quiz Attempts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_id INTEGER NOT NULL,
        score REAL DEFAULT 0.0,
        max_score REAL DEFAULT 0.0,
        percentage REAL DEFAULT 0.0,
        time_spent_sec INTEGER DEFAULT 0,
        difficulty_breakdown TEXT DEFAULT '{}',  -- JSON
        answers TEXT DEFAULT '{}',               -- JSON
        ai_feedback TEXT DEFAULT '',
        remediation_topics TEXT DEFAULT '[]',    -- JSON
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(quiz_id) REFERENCES quizzes(id) ON DELETE CASCADE
    )
    """)

    # User Skills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skill_name TEXT UNIQUE NOT NULL,
        category TEXT DEFAULT 'General',
        mastery_level TEXT DEFAULT 'Novice',  -- Novice, Apprentice, Practitioner, Expert, Master
        mastery_percent REAL DEFAULT 0.0,
        xp INTEGER DEFAULT 0,
        total_attempted INTEGER DEFAULT 0,
        total_correct INTEGER DEFAULT 0,
        basic_score REAL DEFAULT 0.0,
        intermediate_score REAL DEFAULT 0.0,
        advanced_score REAL DEFAULT 0.0,
        mastery_score REAL DEFAULT 0.0,
        last_practiced TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DB_PATH)
