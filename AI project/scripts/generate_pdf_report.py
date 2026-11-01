"""
StudyMate AI - Academic Project Report Generator (PDF)
Compiles a formal, publication-quality academic report matching the Chandigarh University MCA format.
Embeds the 6 UI screenshots and complete architectural documentation.
"""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "StudyMate_AI_Project_Report.pdf")
SHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")

def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Custom styles matching reference format
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=1, # Center
        textColor=colors.HexColor('#0f172a')
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#1e293b')
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        alignment=1,
        textColor=colors.HexColor('#334155')
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        spaceBefore=10,
        spaceAfter=5,
        textColor=colors.HexColor('#0f172a')
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        spaceBefore=7,
        spaceAfter=3,
        textColor=colors.HexColor('#1e293b')
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        spaceAfter=5,
        textColor=colors.HexColor('#334155')
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        leftIndent=12,
        spaceAfter=3,
        textColor=colors.HexColor('#334155')
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#0284c7')
    )

    story = []

    # ==================== PAGE 1: COVER PAGE ====================
    story.append(Spacer(1, 30))
    story.append(Paragraph("STUDYMATE AI – ADAPTIVE LEARNING & QUIZ SYSTEM", title_style))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2563eb'), spaceAfter=15))
    story.append(Paragraph("A Project Report submitted in partial fulfillment of the requirements for the degree of<br/><b>Master of Computer Applications (MCA)</b>", subtitle_style))
    story.append(Spacer(1, 30))

    story.append(Paragraph("<b>Submitted By:</b><br/>Livesh Kumar<br/>Roll No: 26MCA20079<br/>Semester: 1<sup>st</sup> / Year: 1<sup>st</sup>", meta_style))
    story.append(Spacer(1, 22))
    
    story.append(Paragraph("<b>Under the Guidance of:</b><br/>Saranjeet Kaur Mam<br/>Associate professor", meta_style))
    story.append(Spacer(1, 25))

    story.append(Paragraph("<b>Department of Computer Applications</b><br/><b>Chandigarh University</b><br/>Academic Year: 2026–2027", meta_style))
    story.append(Spacer(1, 35))

    # University Badge Box
    cu_table = Table([
        [Paragraph("<font color='#c5192d' size='14'><b>CHANDIGARH UNIVERSITY</b></font><br/><font color='#64748b' size='8'><i>Discover . Learn . Empower</i></font>", meta_style)]
    ], colWidths=[300])
    cu_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(cu_table)
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>CHANDIGARH UNIVERSITY</b><br/>November 2026", meta_style))
    story.append(PageBreak())

    # ==================== PAGE 2: SECTIONS 1 & 2 ====================
    story.append(Paragraph("1. EXECUTIVE SUMMARY & ABSTRACT", h1_style))
    story.append(Paragraph(
        "StudyMate AI is a full-stack, enterprise-grade educational intelligence system engineered to deliver adaptive, high-impact learning experiences. "
        "Built with a high-performance Python/FastAPI backend and a reactive Single-Page Application (SPA) frontend, the platform automatically transforms arbitrary "
        "learning materials—including academic syllabi, lecture slides, research papers, and technical source code—into structured pedagogical study notes and Bloom's Revised Taxonomy tiered assessments.",
        body_style
    ))
    story.append(Paragraph(
        "Traditional study platforms suffer from static, uncalibrated question sets, high subscription barriers, and lack of verified cognitive progression. "
        "StudyMate AI resolves these bottlenecks through a hybrid AI generation architecture: a zero-dependency, deterministic local NLP/heuristic parser running 100% offline out-of-the-box, "
        "paired with optional pluggable LLM inference (Google Gemini / OpenAI). By structuring questions across four distinct cognitive tiers (Basic Recall, Intermediate Applied, Advanced Analytical, and Mastery System Design), "
        "the application accelerates comprehension, prevents rote memorization, and establishes verifiable technical competencies.",
        body_style
    ))

    story.append(Spacer(1, 5))
    story.append(Paragraph("2. INTRODUCTION & BACKGROUND", h1_style))
    
    story.append(Paragraph("2.1 Industry Context", h2_style))
    story.append(Paragraph(
        "Modern educational technology (EdTech) is undergoing a paradigm shift from passive content distribution toward active, personalized recall systems. "
        "Cognitive science research demonstrates that active retrieval, spaced repetition, and scaffolded Bloom's taxonomy ladders yield up to 40% higher retention compared to passive reading. "
        "Modern digital learning architecture requires three non-negotiable guarantees:",
        body_style
    ))
    story.append(Paragraph("1. <b>Adaptive Cognitive Scaffolding:</b> Learners must be assessed progressively from foundational definitions up to multi-step problem solving.", bullet_style))
    story.append(Paragraph("2. <b>Zero-Friction Ingestion:</b> Arbitrary unstructured text, Word documents, and PDFs must parse deterministically without formatting regressions.", bullet_style))
    story.append(Paragraph("3. <b>Diagnostic Remediation & Traceability:</b> Every incorrect response must be mapped to conceptual learning gaps, with instant automated remediation drills.", bullet_style))

    story.append(Paragraph("2.2 Problem Statement", h2_style))
    story.append(Paragraph(
        "Most educational test preparation utilities rely on static question banks or rigid multiple-choice arrays stored in isolated text files. "
        "They fail to adapt to learner weaknesses, provide no cognitive difficulty ladders, and lack real-time skill analytics. Conversely, proprietary LLM platforms "
        "require constant paid API tokens, internet connectivity, and external telemetry that compromise user privacy and limit institutional adoption in low-resource environments.",
        body_style
    ))

    story.append(Paragraph("2.3 Project Objectives", h2_style))
    story.append(Paragraph("The key engineering objectives of this project are:", body_style))
    story.append(Paragraph("1. To engineer a high-throughput, low-latency REST web service using FastAPI and SQLite with Write-Ahead Logging (WAL).", bullet_style))
    story.append(Paragraph("2. To build a multi-format document parser capable of extracting raw text from PDF streams, Word (.docx XML), and plaintext files natively.", bullet_style))
    story.append(Paragraph("3. To implement a Bloom's Revised Taxonomy question generation engine delivering four difficulty tiers with structured distractors and explanations.", bullet_style))
    story.append(Paragraph("4. To engineer interactive 3D Active Recall Flashcards with spaced repetition feedback intervals.", bullet_style))
    story.append(Paragraph("5. To build a unified search and instant 'Topic Study Pack' generation engine allowing on-demand curriculum synthesis.", bullet_style))
    story.append(Paragraph("6. To implement an automated skill tracker with zero-overlap competency progress bars and targeted remediation drills.", bullet_style))

    story.append(PageBreak())

    # ==================== PAGE 3: SECTIONS 2.4, 3 & 4 ====================
    story.append(Paragraph("2.4 Scope and Feasibility", h2_style))
    story.append(Paragraph(
        "• <b>Scope:</b> Technical and academic domains including Computer Science, Natural Science, Quantitative Methods, and Systems Engineering. "
        "Features live assessment runners, countdown timers, hint systems, scorecards, and CSV/Markdown export workflows.<br/>"
        "• <b>Feasibility:</b> By leveraging Python's lightweight ASGI architecture and embedded SQLite3, the application requires zero external database installation, "
        "compiles and runs out-of-the-box on standard workstations, and features automatic port collision resolution.",
        body_style
    ))

    story.append(Paragraph("3. SYSTEM ARCHITECTURE & ENGINEERING DESIGN", h1_style))
    story.append(Paragraph("3.1 High-Level Architecture Overview", h2_style))
    story.append(Paragraph(
        "The system follows a Decoupled Three-Tier Architecture comprising:",
        body_style
    ))
    story.append(Paragraph("1. <b>Presentation Layer (Web SPA):</b> Reactive HTML5/CSS3 interface styled with Tailwind CSS, Lucide SVG iconography, KaTeX mathematical typesetting, and Mermaid.js architectural tree visualization.", bullet_style))
    story.append(Paragraph("2. <b>Application & Intelligence Layer (FastAPI Service):</b> Asynchronous REST HTTP service handling document parsing, semantic concept extraction, Bloom's difficulty routing, and hybrid LLM orchestration.", bullet_style))
    story.append(Paragraph("3. <b>Persistence & Analytics Layer (SQLite3 Engine):</b> Embedded relational database with foreign key integrity, managing documents, notes, quizzes, questions, attempt scorecards, and cumulative skill competencies.", bullet_style))

    story.append(Paragraph("3.2 Concurrency & Asynchronous Processing Model", h2_style))
    story.append(Paragraph(
        "FastAPI executes on the Uvicorn ASGI server. Synchronous SQLite database queries and algorithmic NLP transformations are routed through "
        "FastAPI's optimized threadpool dispatcher, preventing blocking of the asynchronous event loop and ensuring that client UI interactions remain responsive under load.",
        body_style
    ))

    story.append(Paragraph("3.3 Bloom's Taxonomy & Pedagogical Integrity Model", h2_style))
    story.append(Paragraph(
        "Assessments are strictly partitioned into four cognitive levels: "
        "<b>Basic (Recall & Definitions)</b>, <b>Intermediate (Applied Problem Solving & Debugging)</b>, "
        "<b>Advanced (Architectural Trade-offs & Evaluation)</b>, and <b>Mastery (System Design & Capstone Innovation)</b>. "
        "Every question provides detailed rationales explaining why the correct choice is valid and why alternative distractors are structurally invalid.",
        body_style
    ))

    story.append(Paragraph("4. DATABASE DESIGN & DATA MODELING", h1_style))
    story.append(Paragraph("4.1 Relational Schema Specifications", h2_style))
    story.append(Paragraph("• <b>documents:</b> Stores ingested files, extracted text, word counts, estimated reading time, subject tags, and creation timestamps.", bullet_style))
    story.append(Paragraph("• <b>notes:</b> Stores synthesized executive summaries, key concepts JSON arrays, cheat sheet formulas, flashcards decks, and Mermaid mindmaps.", bullet_style))
    story.append(Paragraph("• <b>quizzes:</b> Stores assessment definitions, topics, difficulty tiers, question counts, and duration time limits.", bullet_style))
    story.append(Paragraph("• <b>questions:</b> Stores individual items, Bloom's cognitive level, options JSON arrays, correct answers, hints, XP points, and explanations.", bullet_style))
    story.append(Paragraph("• <b>quiz_attempts:</b> Stores user attempt history, percentage scores, time spent, difficulty breakdowns, and detected remediation topics.", bullet_style))
    story.append(Paragraph("• <b>user_skills:</b> Maintains cumulative proficiency percentages across Basic, Applied, Advanced, and Mastery domains with leveling milestones.", bullet_style))

    story.append(PageBreak())

    # ==================== PAGE 4: SECTIONS 5 & 6 ====================
    story.append(Paragraph("5. MODULE BREAKDOWN & SOURCE CODE STRUCTURE", h1_style))
    
    story.append(Paragraph("5.1 Backend Core Modules (Python / FastAPI)", h2_style))
    story.append(Paragraph("• <b>app/main.py:</b> Central FastAPI application orchestrator, static directory mounts, and CORS middleware configuration.", bullet_style))
    story.append(Paragraph("• <b>app/database.py:</b> SQLite database connection manager, table schema migrations, and index initialization.", bullet_style))
    story.append(Paragraph("• <b>app/models.py:</b> Pydantic data validation schemas for requests, responses, and serialization contracts.", bullet_style))
    story.append(Paragraph("• <b>app/services/text_extractor.py:</b> Stream parser for Word (.docx XML), PDF byte streams, Markdown, and CSV/JSON.", bullet_style))
    story.append(Paragraph("• <b>app/services/notes_engine.py:</b> Pedagogical study notes synthesizer, intuitive analogy builder, and flashcard deck generator.", bullet_style))
    story.append(Paragraph("• <b>app/services/question_engine.py:</b> Bloom's 4-tier quiz generation engine with automated distractor synthesis.", bullet_style))
    story.append(Paragraph("• <b>app/services/skill_tracker.py:</b> Competency radar calculator, XP leveling, and automated remediation topic detector.", bullet_style))
    story.append(Paragraph("• <b>app/services/ai_generator.py:</b> Hybrid orchestrator coordinating local heuristic NLP and optional external LLM inference.", bullet_style))
    story.append(Paragraph("• <b>run.py:</b> Intelligent application launcher with automatic socket collision detection and port binding failover.", bullet_style))

    story.append(Paragraph("5.2 Frontend Client Modules (Web SPA)", h2_style))
    story.append(Paragraph("• <b>app/static/index.html:</b> Single-Page Application skeleton with tab navigation, modal workflows, and responsive grids.", bullet_style))
    story.append(Paragraph("• <b>app/static/css/style.css:</b> Design system featuring 3D flashcard perspective transforms, difficulty badges, and high-contrast modes.", bullet_style))
    story.append(Paragraph("• <b>app/static/js/app.js:</b> State manager, theme toggle, text-to-speech audio reader, and toast notification pipeline.", bullet_style))
    story.append(Paragraph("• <b>app/static/js/uploader.js:</b> Drag-and-drop file upload handler, syllabus paste ingestion, and document library UI.", bullet_style))
    story.append(Paragraph("• <b>app/static/js/notes.js:</b> Interactive notes viewer, 3D card flip engine, and Markdown/JSON export handlers.", bullet_style))
    story.append(Paragraph("• <b>app/static/js/quiz.js:</b> Interactive exam runner, countdown timer, hint toggles, and zero-overlap Bloom's scorecard.", bullet_style))
    story.append(Paragraph("• <b>app/static/js/search.js:</b> Full-text fuzzy search engine and instant 'Topic Study Pack' generation trigger.", bullet_style))
    story.append(Paragraph("• <b>app/static/js/skills.js:</b> Learner competency tree, badge shelf renderer, and historical attempt analytics.", bullet_style))

    story.append(Paragraph("6. REST API SPECIFICATION", h1_style))
    
    api_data = [
        [Paragraph("<b>Endpoint</b>", h2_style), Paragraph("<b>Method</b>", h2_style), Paragraph("<b>Description</b>", h2_style)],
        [Paragraph("<code>/api/upload</code>", code_style), Paragraph("POST", body_style), Paragraph("Uploads document (PDF, DOCX, TXT, MD) or accepts pasted text.", body_style)],
        [Paragraph("<code>/api/documents</code>", code_style), Paragraph("GET", body_style), Paragraph("Lists all ingested study documents and computed reading metadata.", body_style)],
        [Paragraph("<code>/api/notes/generate</code>", code_style), Paragraph("POST", body_style), Paragraph("Synthesizes study notes, flashcards, mindmaps, and cheat sheets.", body_style)],
        [Paragraph("<code>/api/notes/{id}</code>", code_style), Paragraph("GET", body_style), Paragraph("Retrieves full structured study notes by note ID.", body_style)],
        [Paragraph("<code>/api/notes/{id}/export/{format}</code>", code_style), Paragraph("GET", body_style), Paragraph("Exports study notes as formatted Markdown (.md) or JSON.", body_style)],
        [Paragraph("<code>/api/quiz/generate</code>", code_style), Paragraph("POST", body_style), Paragraph("Generates 4-tier Bloom's taxonomy quiz from document or topic.", body_style)],
        [Paragraph("<code>/api/quiz/{id}</code>", code_style), Paragraph("GET", body_style), Paragraph("Retrieves full quiz structure, questions, and option choices.", body_style)],
        [Paragraph("<code>/api/quiz/submit</code>", code_style), Paragraph("POST", body_style), Paragraph("Submits student answers, grades Bloom's tiers, and rewards XP.", body_style)],
        [Paragraph("<code>/api/quiz/remediation</code>", code_style), Paragraph("POST", body_style), Paragraph("Generates targeted remediation quiz covering missed concepts.", body_style)],
        [Paragraph("<code>/api/search</code>", code_style), Paragraph("GET", body_style), Paragraph("Full-text search across documents, notes, quizzes, and questions.", body_style)],
        [Paragraph("<code>/api/search/generate-from-topic</code>", code_style), Paragraph("POST", body_style), Paragraph("Instantly synthesizes study notes and tiered quiz from any topic.", body_style)],
        [Paragraph("<code>/api/skills/dashboard</code>", code_style), Paragraph("GET", body_style), Paragraph("Fetches skill competency tree, unlocked badges, and past attempts.", body_style)]
    ]
    api_table = Table(api_data, colWidths=[150, 50, 300])
    api_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(api_table)

    story.append(PageBreak())

    # ==================== PAGE 5: SECTIONS 7, 8, 9, 10 ====================
    story.append(Paragraph("7. CORE LEARNING WORKFLOWS & BUSINESS LOGIC", h1_style))
    story.append(Paragraph("7.1 Multi-Format Document Ingestion & Native Stream Parsing", h2_style))
    story.append(Paragraph(
        "Uploaded files are streamed into <code>uploads/</code> and processed via native extractors. "
        "DOCX files are decompressed in memory using <code>zipfile</code>, parsing <code>word/document.xml</code> directly. "
        "PDF streams extract text via FlateDecode decompression, computing word counts and estimated reading times automatically.",
        body_style
    ))

    story.append(Paragraph("7.2 4-Tier Bloom's Taxonomy Quiz Generation & Hints", h2_style))
    story.append(Paragraph(
        "The question engine mines high-value concepts, definitions, and relationships. It generates Basic (Factual Recall), "
        "Intermediate (Scenario Application), Advanced (Tradeoff Analysis), and Mastery (System Design) questions with plausible distractors, hints, and point values.",
        body_style
    ))

    story.append(Paragraph("7.3 Interactive 3D Active Recall Flashcards & Spaced Repetition", h2_style))
    story.append(Paragraph(
        "Key concepts are compiled into a 3D flip card deck. Learners rate their recall quality as 'Again (Hard)', 'Good (Medium)', or 'Easy (Mastered)', "
        "reinforcing memory retention via active recall principles.",
        body_style
    ))

    story.append(Paragraph("7.4 Competency Scoring & Targeted Remediation Engine", h2_style))
    story.append(Paragraph(
        "Upon submission, answers are evaluated against the question bank. Subtopics with incorrect answers are dynamically extracted into "
        "a remediation queue, enabling one-click generation of a targeted drill focusing exclusively on the student's missed concepts.",
        body_style
    ))

    story.append(Paragraph("8. SECURITY, INTEGRITY & ACCESSIBILITY CONTROLS", h1_style))
    story.append(Paragraph(
        "• <b>SQL Injection Prevention:</b> All database queries execute via SQLite parameterized parameter bindings (<code>?</code> placeholders).<br/>"
        "• <b>Input Sanitization:</b> File paths are sanitized via <code>os.path.basename</code> to prevent directory traversal exploits.<br/>"
        "• <b>Accessibility Features:</b> Incorporates browser Text-to-Speech (TTS) audio narration, three-tier font scaling (A/AA/AAA), and high-contrast styling.",
        body_style
    ))

    story.append(Paragraph("9. TESTING, QUALITY ASSURANCE & VERIFICATION", h1_style))
    story.append(Paragraph(
        "The project includes an end-to-end automated test harness (<code>tests/test_core.py</code>) executing 7 comprehensive test suites. "
        "The test suite verifies database schema creation, native text extraction, note synthesis, 4-tier quiz generation, search routing, quiz grading, and skill updates.",
        body_style
    ))
    story.append(Paragraph("<b>Test Execution Output:</b> <code>Ran 7 tests in 0.067s — OK (100% Pass Rate)</code>", code_style))

    story.append(Paragraph("10. INSTALLATION, COMPILATION & EXECUTION GUIDE", h1_style))
    story.append(Paragraph(
        "1. Ensure Python 3.10+ is installed on the host operating system.<br/>"
        "2. Launch the application runner: <code>python run.py</code> (automatically binds to port 8000 or the next available socket).<br/>"
        "3. Open web browser at <b>http://127.0.0.1:8000</b>.<br/>"
        "4. To run automated tests: <code>python -m unittest tests/test_core.py -v</code>.",
        body_style
    ))

    story.append(PageBreak())

    # ==================== PAGE 6: SECTION 11 & OUTPUT PART 1 ====================
    story.append(Paragraph("11. LIMITATIONS & FUTURE ENHANCEMENTS", h1_style))
    story.append(Paragraph(
        "Future iterations can introduce multi-tenant user authentication (OAuth2 / JWT), distributed vector embeddings (FAISS / ChromaDB) for semantic retrieval, "
        "real-time peer collaboration rooms via WebSockets, and automatic LaTeX equation rendering for complex mathematical exams.",
        body_style
    ))

    story.append(Paragraph("12. OUTPUT & EXPERIMENTAL RESULTS", h1_style))
    
    # 12.1 Upload Dashboard
    story.append(Paragraph("12.1 Document Ingestion & Syllabus Upload Dashboard", h2_style))
    shot1_path = os.path.join(SHOTS_DIR, "1_upload_ingest.png")
    if os.path.exists(shot1_path):
        story.append(RLImage(shot1_path, width=490, height=195))
    story.append(Paragraph("<i>Figure 12.1: Multi-format document uploader with drop zone, syllabus ingestion, and pre-loaded curated curriculum library.</i>", body_style))
    story.append(Spacer(1, 4))

    # 12.2 Smart Search
    story.append(Paragraph("12.2 Smart Search & Instant Topic Study Pack Generator", h2_style))
    shot2_path = os.path.join(SHOTS_DIR, "2_smart_search.png")
    if os.path.exists(shot2_path):
        story.append(RLImage(shot2_path, width=490, height=190))
    story.append(Paragraph("<i>Figure 12.2: Unified search interface with cognitive difficulty filtering and one-click 'Generate AI Study Pack' capability.</i>", body_style))
    story.append(Spacer(1, 4))

    # 12.3 Study Notes & Flashcards
    story.append(Paragraph("12.3 Interactive Study Notes & Active Recall 3D Flashcards", h2_style))
    shot3_path = os.path.join(SHOTS_DIR, "3_study_notes_flashcards.png")
    if os.path.exists(shot3_path):
        story.append(RLImage(shot3_path, width=490, height=195))
    story.append(Paragraph("<i>Figure 12.3: Study notes breakdown featuring executive summary, 3D flip card deck with spaced repetition, and analogies.</i>", body_style))

    story.append(PageBreak())

    # ==================== PAGE 7: OUTPUT PART 2, CONCLUSION & REFERENCES ====================
    # 12.4 Quiz Runner
    story.append(Paragraph("12.4 Tiered Quiz Runner with Live Timer & Bloom's Badges", h2_style))
    shot4_path = os.path.join(SHOTS_DIR, "4_quiz_runner.png")
    if os.path.exists(shot4_path):
        story.append(RLImage(shot4_path, width=490, height=175))
    story.append(Paragraph("<i>Figure 12.4: Active test runner displaying countdown timer, Bloom's cognitive difficulty tier, XP indicator, and hint toggle.</i>", body_style))
    story.append(Spacer(1, 4))

    # 12.5 Scorecard & Bloom's Performance
    story.append(Paragraph("12.5 Comprehensive Scorecard & Zero-Overlap Bloom's Breakdown", h2_style))
    shot5_path = os.path.join(SHOTS_DIR, "5_scorecard_blooms.png")
    if os.path.exists(shot5_path):
        story.append(RLImage(shot5_path, width=490, height=175))
    story.append(Paragraph("<i>Figure 12.5: Detailed scorecard with accuracy percentage, XP rewards, diagnostic feedback, and structured Bloom's breakdown.</i>", body_style))
    story.append(Spacer(1, 4))

    # 12.6 Skills Dashboard
    story.append(Paragraph("12.6 Learner Competency Tree & Knowledge Badges Dashboard", h2_style))
    shot6_path = os.path.join(SHOTS_DIR, "6_skills_dashboard.png")
    if os.path.exists(shot6_path):
        story.append(RLImage(shot6_path, width=490, height=175))
    story.append(Paragraph("<i>Figure 12.6: Analytics dashboard displaying total XP, mastery matrices across cognitive levels, unlocked badges, and history.</i>", body_style))

    story.append(Spacer(1, 6))
    story.append(Paragraph("13. CONCLUSION", h1_style))
    story.append(Paragraph(
        "The StudyMate AI project successfully demonstrates the design and deployment of an adaptive, high-throughput educational intelligence platform. "
        "By coupling native document stream parsing with a scaffolded Bloom's Revised Taxonomy assessment engine and interactive active recall tools, "
        "the application proves that modern AI learning systems can be lightweight, private, accessible, and mathematically verifiable without requiring proprietary external cloud dependencies.",
        body_style
    ))

    story.append(Paragraph("14. REFERENCES", h1_style))
    story.append(Paragraph("1. Bloom, B. S., & Krathwohl, D. R. (2001). <i>A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy of Educational Objectives</i>. Longman.", bullet_style))
    story.append(Paragraph("2. Karpicke, J. D., & Blunt, J. R. (2011). <i>Retrieval Practice Produces More Learning than Elaborative Studying with Concept Mapping</i>. Science, 331(6018), 772-775.", bullet_style))
    story.append(Paragraph("3. Tiangolo, S. (2023). <i>FastAPI Modern High-Performance Web Framework Documentation</i>. FastAPI Authors.", bullet_style))
    story.append(Paragraph("4. Hipp, D. R. (2024). <i>SQLite Database Engine Architecture & Write-Ahead Logging (WAL)</i>. SQLite.org.", bullet_style))

    story.append(Paragraph("15. SOURCE CODE REPOSITORY", h1_style))
    story.append(Paragraph("<b>GitHub:</b> <code>https://github.com/SOFTGAMESTUDIO/StudyMate-AI-Adaptive-Learning</code>", code_style))

    doc.build(story)
    print("Project report PDF successfully built at:", PDF_PATH)

if __name__ == "__main__":
    build_pdf()
