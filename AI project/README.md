# 🎓 StudyMate AI – Intelligent Adaptive Learning Platform

> *Adaptive Quizzes, Active Recall Notes & Bloom's Taxonomy Skill Development*

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14%20%7C%203.15-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com)
[![Tests](https://img.shields.io/badge/Tests-Passing%20(7%2F7)-emerald.svg)](tests/test_core.py)

---

## 🌟 Overview

**StudyMate AI** is an intelligent, full-stack educational AI platform engineered to accelerate learning, active recall, and verifiable skill development. 

Whether a student uploads lecture slides, syllabi, research notes, or code—or searches for any topic on the fly—StudyMate AI instantly generates:
1. **Interactive Study Notes** complete with executive summaries, high-yield definitions, intuitive real-world analogies, cheat sheets, visual mind maps, and glossaries.
2. **Tiered Adaptive Quizzes** structured along **Bloom’s Revised Taxonomy** from **Basic Recall** up to **Mastery & System Design**.
3. **Interactive 3D Active Recall Flashcards** with spaced repetition self-assessment ratings.
4. **Competency Skill Tree & Diagnostics** tracking learner progress across Bloom's levels, rewarding XP, unlocking excellence badges, and generating **targeted remediation drills** for missed concepts.

---

## 🚀 Key Features

### 1. 📁 Multi-Format Document Ingestion
- Upload `.pdf`, `.docx`, `.txt`, `.md`, `.json`, `.csv`, or source code (`.py`, `.js`, etc.).
- Native, zero-dependency parsers: extracts clean text directly from Word (`word/document.xml`) and PDF objects without external binary bloat.
- Direct syllabus paste with auto-detected word count, reading time, and domain classification.
- Pre-packaged with curated starter modules (Python Programming, Climate Science, AI Ethics, Urban Hydrology).

### 2. 🔍 Smart Search & Topic Study Pack Generator
- Full-text search across documents, study notes, quiz banks, and individual question stems.
- Filter by difficulty tier (`Basic`, `Intermediate`, `Advanced`, `Mastery`) or category.
- **Instant AI Study Pack Generator**: Type any query into the search bar (e.g., *"Binary Search Trees"*, *"Urban Flooding"*, *"Transformer Models"*), and click **"Generate AI Study Pack"** to synthesize fresh study notes and a 4-tier quiz on the fly!

### 3. 📘 AI Study Notes & Active Recall Flashcards
- **Executive Summary**: High-yield 2-3 sentence distillation.
- **Key Concepts with Real-World Analogies**: Explains complex theorems using intuitive physical analogies.
- **Cheat Sheet & Rapid Rules**: Syntax rules, formulas, and common traps.
- **Visual Mind Map**: Rendered via Mermaid.js and clean structural diagrams.
- **Interactive 3D Flashcards**: Flip cards with spaced repetition self-rating (`Again`, `Good`, `Easy`).
- **Export Options**: 1-click export to Markdown (`.md`) or structured JSON.

### 4. 🎯 Bloom's Taxonomy 4-Tier Quiz Engine
Quizzes are systematically generated across 4 distinct cognitive tiers:
| Tier | Bloom's Level | Cognitive Focus | Point Value |
| :--- | :--- | :--- | :--- |
| **🌱 Basic** | Remember & Understand | Factual recall, definitions, syntax, True/False | 10 XP |
| **⚙️ Intermediate** | Apply & Analyze | Scenario implementation, cause & effect, debugging | 15 XP |
| **🧠 Advanced** | Evaluate & Synthesize | Edge cases, architectural tradeoffs, concurrency | 25 XP |
| **🏆 Mastery** | Create & Innovate | High-scale system design, resiliency, innovation | 40 XP |

### 5. 📊 Real-Time Skill Tree & Targeted Remediation
- Comprehensive scorecard with accuracy %, percentile, and XP gain.
- **Clean Bloom's Taxonomy Performance Chart** breaking down accuracy by difficulty tier with zero visual overlap.
- **Targeted Remediation Engine**: Detects missed subtopics and generates a 1-click **"Practice Missed Topics"** drill covering only the student's learning gaps.
- **Knowledge Badges Shelf**: Unlocks badges such as *Dedicated Learner*, *Foundations Master*, *Applied Problem Solver*, *Advanced Synthesizer*, and *Mastery Scholar*.

### 6. 🧠 Dual AI Engine Architecture
- **Built-in Local NLP Engine (Default)**: Runs 100% offline out-of-the-box with zero API keys or external dependencies.
- **External LLM Support (Optional)**: Seamless toggle in Settings to connect Google Gemini (`gemini-1.5-flash`) or OpenAI (`gpt-4o-mini`) via API key, with graceful automatic fallback.

---

## ⚡ Quickstart Guide

### 1. Start the Web Server
Run the launcher script from the project directory:

```bash
python run.py
```

*Note: If port 8000 is occupied by another process, `run.py` automatically detects it and binds to the next free port (e.g. 8001), or you can specify any port: `python run.py 8080`.*

### 2. Open in Your Browser
Visit:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)** (or the port reported by `run.py`)

### 3. Run Automated Tests
```bash
python -m unittest tests/test_core.py -v
```

Output:
```
test_01_database_tables_exist ... ok
test_02_text_extractor_and_metadata ... ok
test_03_notes_generation ... ok
test_04_tiered_quiz_generation ... ok
test_05_api_list_documents ... ok
test_06_instant_search_and_generate_topic ... ok
test_07_quiz_submission_and_skill_scoring ... ok

Ran 7 tests in 0.067s
OK
```
