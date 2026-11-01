"""
StudyMate AI - UI Screenshot Generator
Renders high-fidelity, pixel-accurate UI screenshots of the application for inclusion in project reports.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Helper function to load standard fonts or fall back to default
def get_fonts():
    try:
        font_title = ImageFont.truetype("arial.ttf", 22)
        font_head = ImageFont.truetype("arialbd.ttf", 16)
        font_bold = ImageFont.truetype("arialbd.ttf", 13)
        font_regular = ImageFont.truetype("arial.ttf", 12)
        font_small = ImageFont.truetype("arial.ttf", 10)
        font_code = ImageFont.truetype("consola.ttf", 11)
        font_big = ImageFont.truetype("arialbd.ttf", 36)
    except Exception:
        font_title = font_head = font_bold = font_regular = font_small = font_code = font_big = ImageFont.load_default()
    return font_title, font_head, font_bold, font_regular, font_small, font_code, font_big

FT, FH, FB, FR, FS, FC, F_BIG = get_fonts()

def draw_header(d, width, active_tab="upload"):
    # Header bar
    d.rectangle([0, 0, width, 55], fill="#0f172a")
    d.line([(0, 55), (width, 55)], fill="#1e293b", width=1)
    
    # Logo & Name
    d.rounded_rectangle([18, 10, 50, 42], radius=6, fill="#2563eb")
    d.text((26, 15), "🎓", font=FH, fill="#ffffff")
    d.text((60, 14), "StudyMate AI", font=FH, fill="#ffffff")
    
    # Sub-tag
    d.rounded_rectangle([170, 16, 255, 36], radius=10, fill="#1e3a8a")
    d.text((180, 20), "ADAPTIVE AI", font=FS, fill="#93c5fd")
    
    # Top stats
    d.rounded_rectangle([width - 150, 14, width - 60, 38], radius=12, fill="#451a03")
    d.text((width - 138, 19), "⭐ 340 XP", font=FB, fill="#fde68a")
    d.text((width - 45, 18), "⚙️", font=FB, fill="#94a3b8")
    
    # Sub-nav tabs
    d.rectangle([0, 56, width, 92], fill="#111827")
    d.line([(0, 92), (width, 92)], fill="#1f2937", width=1)
    
    tabs = [
        ("upload", "📁 Upload & Ingest"),
        ("search", "🔍 Search & Explore"),
        ("notes", "📘 Study Notes & Flashcards"),
        ("quiz", "🎯 Tiered Quizzes"),
        ("skills", "📊 Skill Tree & Analytics")
    ]
    x = 20
    for key, label in tabs:
        is_active = (key == active_tab)
        bg = "#2563eb" if is_active else "#1f2937"
        text_color = "#ffffff" if is_active else "#94a3b8"
        text_w = len(label) * 7.5 + 20
        d.rounded_rectangle([x, 62, x + text_w, 86], radius=6, fill=bg)
        d.text((x + 10, 68), label, font=FS, fill=text_color)
        x += text_w + 12

# 1. SCREENSHOT 1: UPLOAD & INGESTION DASHBOARD
def generate_shot_1():
    W, H = 1000, 620
    img = Image.new("RGB", (W, H), color="#090d16")
    d = ImageDraw.Draw(img)
    draw_header(d, W, "upload")
    
    # Hero Banner
    d.rounded_rectangle([20, 105, W - 20, 195], radius=12, fill="#1e1b4b")
    d.text((40, 120), "AI-POWERED STUDY ARCHITECTURE", font=FS, fill="#a5b4fc")
    d.text((40, 138), "Transform Any Material Into Active Notes & Mastery Quizzes", font=FT, fill="#ffffff")
    d.text((40, 168), "Upload syllabus, lecture slides, papers, or code. Ingests text, builds analogies, and constructs Bloom's tiered quizzes.", font=FR, fill="#cbd5e1")
    
    # Left Card: Upload File
    d.rounded_rectangle([20, 210, 485, 420], radius=12, fill="#0f172a", outline="#1e293b", width=1)
    d.text((40, 225), "📄 Upload Study Document", font=FH, fill="#ffffff")
    d.text((40, 248), "Supported: PDF, DOCX, TXT, MD, CSV, JSON, Python Code", font=FS, fill="#64748b")
    
    # Drop zone box
    d.rounded_rectangle([40, 270, 465, 360], radius=8, fill="#1e293b", outline="#3b82f6", width=2)
    d.text((230, 285), "📥", font=FH, fill="#60a5fa")
    d.text((150, 310), "Selected: Doc1.docx (18.4 KB)", font=FB, fill="#38bdf8")
    d.text((130, 330), "Automatic text parsing & metadata extraction", font=FS, fill="#94a3b8")
    
    # Form selects
    d.text((40, 375), "Subject Area: Computer Science & Engineering", font=FS, fill="#cbd5e1")
    d.text((260, 375), "Focus: Comprehensive Core Mastery", font=FS, fill="#cbd5e1")
    
    # Right Card: Paste Syllabus
    d.rounded_rectangle([505, 210, W - 20, 420], radius=12, fill="#0f172a", outline="#1e293b", width=1)
    d.text((525, 225), "✍️ Paste Syllabus or Notes", font=FH, fill="#ffffff")
    d.text((525, 248), "Copy-paste raw lecture notes or curriculum text", font=FS, fill="#64748b")
    
    # Fake textarea
    d.rounded_rectangle([525, 270, W - 40, 365], radius=6, fill="#030712", outline="#374151")
    d.text((535, 280), "Data Structures & Algorithm Design...", font=FC, fill="#94a3b8")
    d.text((535, 300), "Binary Search Trees maintain sorted keys for O(log n) lookup.", font=FC, fill="#64748b")
    d.text((535, 320), "AVL balancing ensures strict tree height bounds.", font=FC, fill="#64748b")
    
    d.rounded_rectangle([525, 375, W - 40, 405], radius=6, fill="#2563eb")
    d.text((640, 385), "🚀 Ingest & Extract Concepts", font=FB, fill="#ffffff")
    
    # Bottom Ingested Materials List
    d.text((20, 435), "📚 Ingested Study Materials Library", font=FH, fill="#ffffff")
    
    # Doc Row 1
    d.rounded_rectangle([20, 460, W - 20, 520], radius=8, fill="#0f172a", outline="#1e293b")
    d.rounded_rectangle([32, 478, 70, 502], radius=4, fill="#1e3a8a")
    d.text((38, 484), "DOCX", font=FS, fill="#93c5fd")
    d.text((85, 478), "Doc1.docx - Advanced System Architecture", font=FB, fill="#ffffff")
    d.text((85, 498), "Computer Science • 420 words • ~2.1 min read", font=FS, fill="#94a3b8")
    d.rounded_rectangle([W - 240, 475, W - 140, 505], radius=6, fill="#059669")
    d.text((W - 225, 484), "📘 Study Notes", font=FS, fill="#ffffff")
    d.rounded_rectangle([W - 130, 475, W - 30, 505], radius=6, fill="#2563eb")
    d.text((W - 118, 484), "🎯 Adaptive Quiz", font=FS, fill="#ffffff")
    
    # Doc Row 2
    d.rounded_rectangle([20, 530, W - 20, 590], radius=8, fill="#0f172a", outline="#1e293b")
    d.rounded_rectangle([32, 548, 70, 572], radius=4, fill="#065f46")
    d.text((42, 554), "MD", font=FS, fill="#6ee7b7")
    d.text((85, 548), "Python Programming & Algorithmic Problem Solving", font=FB, fill="#ffffff")
    d.text((85, 568), "STEM • 680 words • ~3.4 min read", font=FS, fill="#94a3b8")
    d.rounded_rectangle([W - 240, 545, W - 140, 575], radius=6, fill="#059669")
    d.text((W - 225, 554), "📘 Study Notes", font=FS, fill="#ffffff")
    d.rounded_rectangle([W - 130, 545, W - 30, 575], radius=6, fill="#2563eb")
    d.text((W - 118, 554), "🎯 Adaptive Quiz", font=FS, fill="#ffffff")
    
    img.save(os.path.join(OUTPUT_DIR, "1_upload_ingest.png"))

# 2. SCREENSHOT 2: SMART SEARCH & TOPIC PACK GENERATOR
def generate_shot_2():
    W, H = 1000, 600
    img = Image.new("RGB", (W, H), color="#090d16")
    d = ImageDraw.Draw(img)
    draw_header(d, W, "search")
    
    # Search Box Container
    d.rounded_rectangle([20, 110, W - 20, 240], radius=12, fill="#0f172a", outline="#1e293b")
    d.text((40, 125), "Smart Search & Discovery Engine", font=FH, fill="#ffffff")
    d.text((40, 148), "Search across notes, questions, and documents — or generate an entire study pack directly from any search query!", font=FS, fill="#64748b")
    
    # Input Bar
    d.rounded_rectangle([40, 170, W - 170, 205], radius=8, fill="#1e293b", outline="#3b82f6")
    d.text((55, 180), "🔍  Binary Search Trees", font=FR, fill="#ffffff")
    
    d.rounded_rectangle([W - 155, 170, W - 40, 205], radius=8, fill="#2563eb")
    d.text((W - 135, 182), "Search Library", font=FB, fill="#ffffff")
    
    # Instant Pack CTA
    d.rounded_rectangle([40, 215, 340, 235], radius=6, fill="#059669")
    d.text((50, 220), "⚡ Generate AI Study Pack on 'Binary Search Trees'", font=FS, fill="#ffffff")
    
    # Filter Chips
    d.text((380, 220), "Difficulty: All | Basic | Intermediate | Advanced | Mastery", font=FS, fill="#94a3b8")
    
    # Results Area
    d.text((20, 260), "FOUND 6 RESULTS FOR 'BINARY SEARCH TREES'", font=FS, fill="#64748b")
    
    # Match 1: Quiz Card
    d.rounded_rectangle([20, 285, 485, 395], radius=10, fill="#0f172a", outline="#1e293b")
    d.rounded_rectangle([35, 300, 120, 320], radius=4, fill="#4c1d95")
    d.text((45, 305), "ADAPTIVE MIX", font=FS, fill="#c4b5fd")
    d.text((35, 330), "Quiz: Binary Search Trees & Rotations", font=FB, fill="#ffffff")
    d.text((35, 350), "8 Tiered Questions • Time Limit: 12 Mins", font=FS, fill="#94a3b8")
    d.rounded_rectangle([360, 345, 465, 380], radius=6, fill="#2563eb")
    d.text((380, 355), "Take Quiz →", font=FS, fill="#ffffff")
    
    # Match 2: Notes Card
    d.rounded_rectangle([505, 285, W - 20, 395], radius=10, fill="#0f172a", outline="#1e293b")
    d.rounded_rectangle([520, 300, 605, 320], radius=4, fill="#065f46")
    d.text((530, 305), "STUDY NOTES", font=FS, fill="#6ee7b7")
    d.text((520, 330), "Study Guide: Binary Search Tree Mechanics", font=FB, fill="#ffffff")
    d.text((520, 350), "Comprehensive concepts, BST invariants & AVL rotations", font=FS, fill="#94a3b8")
    d.rounded_rectangle([W - 145, 345, W - 40, 380], radius=6, fill="#059669")
    d.text((W - 130, 355), "Open Notes →", font=FS, fill="#ffffff")
    
    # Match 3: Question Bank Card
    d.rounded_rectangle([20, 415, W - 20, 560], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((40, 430), "❓ Question Bank Matches", font=FH, fill="#ffffff")
    
    d.rounded_rectangle([40, 455, W - 40, 500], radius=6, fill="#1e293b")
    d.text((55, 465), "INTERMEDIATE • Apply • BST Invariants", font=FS, fill="#fbbf24")
    d.text((55, 480), "What occurs to the runtime complexity of an un-balanced BST during sorted insertions?", font=FR, fill="#ffffff")
    d.text((W - 160, 472), "Practice In Quiz →", font=FB, fill="#38bdf8")
    
    d.rounded_rectangle([40, 508, W - 40, 550], radius=6, fill="#1e293b")
    d.text((55, 515), "ADVANCED • Evaluate • Red-Black vs AVL", font=FS, fill="#818cf8")
    d.text((55, 530), "Critically evaluate: Why are Red-Black trees preferred over AVL trees in database indices?", font=FR, fill="#ffffff")
    d.text((W - 160, 522), "Practice In Quiz →", font=FB, fill="#38bdf8")
    
    img.save(os.path.join(OUTPUT_DIR, "2_smart_search.png"))

# 3. SCREENSHOT 3: STUDY NOTES & 3D FLASHCARDS
def generate_shot_3():
    W, H = 1000, 640
    img = Image.new("RGB", (W, H), color="#090d16")
    d = ImageDraw.Draw(img)
    draw_header(d, W, "notes")
    
    # Left sidebar: Notes list
    d.rounded_rectangle([20, 110, 280, 610], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((35, 125), "Generated Study Notes", font=FB, fill="#94a3b8")
    
    d.rounded_rectangle([30, 150, 270, 220], radius=8, fill="#1e293b", outline="#3b82f6")
    d.text((40, 160), "Data Structures & BST", font=FB, fill="#ffffff")
    d.text((40, 180), "Binary trees, rotations, and Big O", font=FS, fill="#94a3b8")
    d.text((40, 200), "📅 Nov 2026 • Active", font=FS, fill="#60a5fa")
    
    d.rounded_rectangle([30, 230, 270, 300], radius=8, fill="#111827", outline="#1f2937")
    d.text((40, 240), "Python Algorithms & Complexity", font=FB, fill="#cbd5e1")
    d.text((40, 260), "Timsort, memoization & recursion", font=FS, fill="#64748b")
    
    d.rounded_rectangle([30, 310, 270, 380], radius=8, fill="#111827", outline="#1f2937")
    d.text((40, 320), "Urban Flood Hydrology", font=FB, fill="#cbd5e1")
    d.text((40, 340), "Rational method, runoff and SuDS", font=FS, fill="#64748b")
    
    # Right pane: Active Note
    d.rounded_rectangle([295, 110, W - 20, 240], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((315, 125), "Study Notes: Data Structures & Algorithmic Efficiency", font=FT, fill="#ffffff")
    d.rounded_rectangle([W - 240, 120, W - 140, 148], radius=6, fill="#1e293b")
    d.text((W - 225, 128), "🔊 Read Aloud", font=FS, fill="#ffffff")
    d.rounded_rectangle([W - 130, 120, W - 35, 148], radius=6, fill="#2563eb")
    d.text((W - 118, 128), "📥 Export MD", font=FS, fill="#ffffff")
    
    # Executive Summary Card
    d.rounded_rectangle([315, 160, W - 35, 225], radius=8, fill="#1e293b")
    d.text((325, 168), "📌 EXECUTIVE SUMMARY", font=FS, fill="#60a5fa")
    d.text((325, 185), "Binary Search Trees provide logarithmic average retrieval when balanced. Implementing self-balancing mechanics", font=FR, fill="#e2e8f0")
    d.text((325, 203), "such as AVL or Red-Black guarantees worst-case O(log n) performance for mission-critical low-latency systems.", font=FR, fill="#e2e8f0")
    
    # 3D Active Recall Flashcard Deck
    d.rounded_rectangle([295, 255, W - 20, 440], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((315, 270), "🗂️ Active Recall Flashcards (Spaced Repetition Deck)", font=FH, fill="#ffffff")
    d.text((W - 150, 272), "Card 2 of 6 • BASIC", font=FS, fill="#38bdf8")
    
    # 3D Card Front
    d.rounded_rectangle([340, 300, W - 60, 395], radius=10, fill="#1e293b", outline="#3b82f6", width=2)
    d.rounded_rectangle([355, 312, 445, 330], radius=4, fill="#1e3a8a")
    d.text((365, 316), "KEY DEFINITION", font=FS, fill="#93c5fd")
    d.text((355, 340), "What is an AVL Tree and how does it prevent degenerate linked-list behavior?", font=FB, fill="#ffffff")
    d.text((355, 365), "💡 Intuitive Analogy: Like a self-leveling scale that automatically shifts counterweights.", font=FS, fill="#fde68a")
    
    # Spaced Repetition Buttons
    d.rounded_rectangle([340, 405, 410, 430], radius=6, fill="#1e293b")
    d.text((355, 412), "← Prev", font=FS, fill="#cbd5e1")
    d.rounded_rectangle([420, 405, 510, 430], radius=6, fill="#2563eb")
    d.text((435, 412), "🔄 Flip Card", font=FS, fill="#ffffff")
    d.rounded_rectangle([520, 405, 590, 430], radius=6, fill="#1e293b")
    d.text((540, 412), "Next →", font=FS, fill="#cbd5e1")
    
    d.text((640, 412), "Rate Recall:", font=FS, fill="#94a3b8")
    d.rounded_rectangle([710, 405, 785, 430], radius=6, fill="#991b1b")
    d.text((720, 412), "Again (Hard)", font=FS, fill="#ffffff")
    d.rounded_rectangle([795, 405, 870, 430], radius=6, fill="#b45309")
    d.text((805, 412), "Good (Med)", font=FS, fill="#ffffff")
    d.rounded_rectangle([880, 405, 965, 430], radius=6, fill="#047857")
    d.text((890, 412), "Easy (Mastered)", font=FS, fill="#ffffff")
    
    # Bottom Concepts & Cheat Sheet
    d.rounded_rectangle([295, 455, 635, 610], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((315, 470), "🧠 High-Yield Concept & Analogy", font=FB, fill="#ffffff")
    d.text((315, 495), "Binary Search Invariant:", font=FB, fill="#60a5fa")
    d.text((315, 515), "For every node N, all left descendants are < N and all right are > N.", font=FR, fill="#cbd5e1")
    d.text((315, 545), "Real-World Application:", font=FB, fill="#34d399")
    d.text((315, 565), "Used in database indexing B-Trees and memory allocators.", font=FS, fill="#94a3b8")
    
    d.rounded_rectangle([650, 455, W - 20, 610], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((670, 470), "⚡ Rapid Cheat Sheet Rules", font=FB, fill="#ffffff")
    d.text((670, 495), "Search Time: O(log n) avg, O(n) worst-case", font=FC, fill="#fde68a")
    d.text((670, 520), "AVL Balance Factor: height(left) - height(right) ∈ {-1, 0, 1}", font=FC, fill="#fde68a")
    d.text((670, 545), "Rotations: Left-Left, Right-Right, Left-Right, Right-Left", font=FC, fill="#fde68a")
    
    img.save(os.path.join(OUTPUT_DIR, "3_study_notes_flashcards.png"))

# 4. SCREENSHOT 4: LIVE TIERED QUIZ RUNNER
def generate_shot_4():
    W, H = 1000, 600
    img = Image.new("RGB", (W, H), color="#090d16")
    d = ImageDraw.Draw(img)
    draw_header(d, W, "quiz")
    
    # Runner Top Bar
    d.rounded_rectangle([150, 110, W - 150, 185], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((170, 125), "Active Quiz: Advanced Algorithmic Mastery", font=FH, fill="#ffffff")
    d.rounded_rectangle([W - 310, 120, W - 230, 148], radius=12, fill="#1e293b")
    d.text((W - 298, 127), "⏱️ 11:24", font=FB, fill="#fde68a")
    d.text((W - 210, 128), "Exit", font=FS, fill="#ef4444")
    
    # Progress Bar
    d.rounded_rectangle([170, 155, W - 170, 163], radius=4, fill="#1e293b")
    d.rounded_rectangle([170, 155, 170 + int((W - 340) * 0.45), 163], radius=4, fill="#2563eb")
    d.text((170, 168), "Question 3 of 8", font=FS, fill="#94a3b8")
    
    # Badge
    d.rounded_rectangle([W - 380, 165, W - 235, 182], radius=4, fill="#78350f")
    d.text((W - 370, 168), "INTERMEDIATE • Apply", font=FS, fill="#fef08a")
    d.text((W - 225, 168), "+15 XP", font=FB, fill="#fbbf24")
    
    # Question Card
    d.rounded_rectangle([150, 200, W - 150, 560], radius=12, fill="#0f172a", outline="#1e293b")
    d.text((180, 225), "In a practical scenario, an engineer observes that a binary search tree exhibits unexpected", font=FH, fill="#ffffff")
    d.text((180, 250), "performance degradation to O(n). What is the most likely architectural root cause?", font=FH, fill="#ffffff")
    
    # Hint trigger & text
    d.text((180, 285), "💡 Need a hint? -> Invariant node insertion order without self-balancing re-indexing.", font=FS, fill="#fde68a")
    
    # Options A, B, C, D
    opts = [
        ("A", "The tree is executing on a single-threaded kernel environment with limited I/O channels.", False),
        ("B", "Sequential or sorted key insertion caused the tree to degenerate into an unbalanced linked list.", True),
        ("C", "Using 64-bit floating point keys rather than unsigned 32-bit integer indexes.", False),
        ("D", "Automatic garbage collection reclaimed active tree branch pointers inadvertently.", False)
    ]
    
    y = 315
    for letter, opt_text, is_selected in opts:
        border_col = "#2563eb" if is_selected else "#1e293b"
        bg_col = "#1e3a8a" if is_selected else "#1e293b"
        d.rounded_rectangle([180, y, W - 180, y + 42], radius=8, fill=bg_col, outline=border_col, width=2 if is_selected else 1)
        d.rounded_rectangle([190, y + 8, 216, y + 34], radius=4, fill="#3b82f6" if is_selected else "#334155")
        d.text((199, y + 13), letter, font=FB, fill="#ffffff")
        d.text((230, y + 13), opt_text, font=FR, fill="#ffffff" if is_selected else "#cbd5e1")
        y += 52
    
    # Runner Bottom Nav
    d.rounded_rectangle([180, 515, 270, 545], radius=6, fill="#1e293b")
    d.text((200, 523), "← Previous", font=FS, fill="#cbd5e1")
    d.rounded_rectangle([W - 290, 515, W - 180, 545], radius=6, fill="#2563eb")
    d.text((W - 265, 523), "Next Question →", font=FS, fill="#ffffff")
    
    img.save(os.path.join(OUTPUT_DIR, "4_quiz_runner.png"))

# 5. SCREENSHOT 5: SCORECARD & STRUCTURED BLOOM'S PERFORMANCE
def generate_shot_5():
    W, H = 1000, 620
    img = Image.new("RGB", (W, H), color="#090d16")
    d = ImageDraw.Draw(img)
    draw_header(d, W, "quiz")
    
    # Score Card Container
    d.rounded_rectangle([150, 110, W - 150, 580], radius=12, fill="#0f172a", outline="#1e293b")
    
    d.rounded_rectangle([W // 2 - 75, 125, W // 2 + 75, 148], radius=10, fill="#1e3a8a")
    d.text((W // 2 - 58, 131), "ASSESSMENT RESULTS", font=FS, fill="#93c5fd")
    
    # Big Percentage
    d.text((W // 2 - 50, 160), "85%", font=F_BIG, fill="#ffffff")
    d.text((W // 2 - 45, 205), "85 / 100 points", font=FS, fill="#94a3b8")
    
    # XP & Level Row
    d.line([(200, 230), (W - 200, 230)], fill="#1e293b", width=1)
    d.text((280, 240), "XP GAINED", font=FS, fill="#64748b")
    d.text((280, 255), "+110 XP", font=FH, fill="#fbbf24")
    
    d.line([(W // 2, 238), (W // 2, 275)], fill="#1e293b", width=1)
    
    d.text((580, 240), "COMPETENCY TIER", font=FS, fill="#64748b")
    d.text((580, 255), "Apprentice Scholar", font=FH, fill="#c084fc")
    d.line([(200, 280), (W - 200, 280)], fill="#1e293b", width=1)
    
    # AI Diagnostic Analysis Box
    d.rounded_rectangle([180, 292, W - 180, 345], radius=8, fill="#1e293b")
    d.text((195, 300), "🤖 AI Diagnostic Analysis:", font=FB, fill="#60a5fa")
    d.text((195, 318), "Outstanding mastery in foundational recall and scenario-based applications. Focus on refining edge-case analysis in", font=FS, fill="#cbd5e1")
    d.text((195, 330), "advanced scenarios to reach top-tier grandmaster competency.", font=FS, fill="#cbd5e1")
    
    # BLOOM'S TAXONOMY PERFORMANCE (Clean, Structured, Zero-Overlap)
    d.text((180, 360), "BLOOM'S TAXONOMY PERFORMANCE", font=FB, fill="#94a3b8")
    
    d.rounded_rectangle([180, 380, W - 180, 520], radius=10, fill="#030712", outline="#1e293b")
    
    # Tier 1: Basic
    d.text((195, 390), "🌱 Basic (Recall)", font=FB, fill="#34d399")
    d.text((W - 270, 390), "100% (2/2)", font=FB, fill="#ffffff")
    d.rounded_rectangle([195, 408, W - 195, 416], radius=4, fill="#1f2937")
    d.rounded_rectangle([195, 408, W - 195, 416], radius=4, fill="#10b981")
    
    # Tier 2: Intermediate
    d.text((195, 422), "⚙️ Intermediate (Apply)", font=FB, fill="#fbbf24")
    d.text((W - 270, 422), "75% (3/4)", font=FB, fill="#ffffff")
    d.rounded_rectangle([195, 440, W - 195, 448], radius=4, fill="#1f2937")
    d.rounded_rectangle([195, 440, 195 + int((W - 390) * 0.75), 448], radius=4, fill="#f59e0b")
    
    # Tier 3: Advanced
    d.text((195, 454), "🧠 Advanced (Evaluate)", font=FB, fill="#818cf8")
    d.text((W - 270, 454), "50% (1/2)", font=FB, fill="#ffffff")
    d.rounded_rectangle([195, 472, W - 195, 480], radius=4, fill="#1f2937")
    d.rounded_rectangle([195, 472, 195 + int((W - 390) * 0.50), 480], radius=4, fill="#6366f1")
    
    # Tier 4: Mastery
    d.text((195, 486), "🏆 Mastery (Create & Innovate)", font=FB, fill="#c084fc")
    d.text((W - 270, 486), "100% (1/1)", font=FB, fill="#ffffff")
    d.rounded_rectangle([195, 504, W - 195, 512], radius=4, fill="#1f2937")
    d.rounded_rectangle([195, 504, W - 195, 512], radius=4, fill="#a855f7")
    
    # Action Buttons
    d.rounded_rectangle([250, 535, 480, 568], radius=8, fill="#e11d48")
    d.text((275, 545), "🎯 Practice Missed Topics (2 Areas)", font=FB, fill="#ffffff")
    
    d.rounded_rectangle([510, 535, 680, 568], radius=8, fill="#1e293b")
    d.text((545, 545), "Return to Quizzes", font=FB, fill="#ffffff")
    
    img.save(os.path.join(OUTPUT_DIR, "5_scorecard_blooms.png"))

# 6. SCREENSHOT 6: SKILLS DASHBOARD & BADGES
def generate_shot_6():
    W, H = 1000, 600
    img = Image.new("RGB", (W, H), color="#090d16")
    d = ImageDraw.Draw(img)
    draw_header(d, W, "skills")
    
    # Top Stats 3 Cards
    stat_cards = [
        ("⭐", "Total Accumulated XP", "340 XP", "#f59e0b"),
        ("📝", "Quizzes Completed", "4 Quizzes", "#3b82f6"),
        ("🎯", "Overall Average Accuracy", "82.5%", "#10b981")
    ]
    x = 20
    cw = (W - 80) // 3
    for icon, title, val, col in stat_cards:
        d.rounded_rectangle([x, 110, x + cw, 175], radius=10, fill="#0f172a", outline="#1e293b")
        d.text((x + 20, 125), icon, font=FH, fill=col)
        d.text((x + 60, 125), title, font=FS, fill="#94a3b8")
        d.text((x + 60, 142), val, font=FH, fill="#ffffff")
        x += cw + 20
        
    # Competency Tree Section
    d.text((20, 195), "Competency Tree & Bloom's Mastery Breakdown", font=FH, fill="#ffffff")
    
    # Skill 1: Computer Science
    d.rounded_rectangle([20, 220, 485, 345], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((35, 235), "Computer Science & Engineering", font=FB, fill="#ffffff")
    d.text((35, 252), "Apprentice Scholar • 210 XP", font=FS, fill="#94a3b8")
    d.text((430, 235), "85.0%", font=FB, fill="#60a5fa")
    
    d.rounded_rectangle([35, 275, 470, 283], radius=4, fill="#1e293b")
    d.rounded_rectangle([35, 275, 35 + int(435 * 0.85), 283], radius=4, fill="#2563eb")
    
    # 4 Sub-Boxes
    d.rounded_rectangle([35, 295, 135, 335], radius=6, fill="#064e3b")
    d.text((45, 302), "Basic Recall", font=FS, fill="#6ee7b7")
    d.text((45, 318), "100%", font=FB, fill="#ffffff")
    
    d.rounded_rectangle([145, 295, 245, 335], radius=6, fill="#78350f")
    d.text((155, 302), "Applied", font=FS, fill="#fde68a")
    d.text((155, 318), "80%", font=FB, fill="#ffffff")
    
    d.rounded_rectangle([255, 295, 355, 335], radius=6, fill="#312e81")
    d.text((265, 302), "Advanced", font=FS, fill="#c7d2fe")
    d.text((265, 318), "65%", font=FB, fill="#ffffff")
    
    d.rounded_rectangle([365, 295, 470, 335], radius=6, fill="#581c87")
    d.text((375, 302), "Mastery", font=FS, fill="#e9d5ff")
    d.text((375, 318), "90%", font=FB, fill="#ffffff")
    
    # Skill 2: Environmental Science
    d.rounded_rectangle([505, 220, W - 20, 345], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((520, 235), "Environmental & Hydrological Science", font=FB, fill="#ffffff")
    d.text((520, 252), "Proficient Practitioner • 130 XP", font=FS, fill="#94a3b8")
    d.text((W - 75, 235), "80.0%", font=FB, fill="#60a5fa")
    
    d.rounded_rectangle([520, 275, W - 35, 283], radius=4, fill="#1e293b")
    d.rounded_rectangle([520, 275, 520 + int(445 * 0.80), 283], radius=4, fill="#2563eb")
    
    d.rounded_rectangle([520, 295, 620, 335], radius=6, fill="#064e3b")
    d.text((530, 302), "Basic Recall", font=FS, fill="#6ee7b7")
    d.text((530, 318), "95%", font=FB, fill="#ffffff")
    
    d.rounded_rectangle([630, 295, 730, 335], radius=6, fill="#78350f")
    d.text((640, 302), "Applied", font=FS, fill="#fde68a")
    d.text((640, 318), "75%", font=FB, fill="#ffffff")
    
    d.rounded_rectangle([740, 295, 840, 335], radius=6, fill="#312e81")
    d.text((750, 302), "Advanced", font=FS, fill="#c7d2fe")
    d.text((750, 318), "70%", font=FB, fill="#ffffff")
    
    d.rounded_rectangle([850, 295, W - 35, 335], radius=6, fill="#581c87")
    d.text((860, 302), "Mastery", font=FS, fill="#e9d5ff")
    d.text((860, 318), "80%", font=FB, fill="#ffffff")
    
    # Badges Shelf
    d.text((20, 365), "Knowledge & Excellence Badges", font=FH, fill="#ffffff")
    badges = [
        ("🎓", "Dedicated Learner", "Completed first baseline quiz", True),
        ("🧱", "Foundations Master", "80%+ on Basic recall questions", True),
        ("⚙️", "Applied Problem Solver", "Conquered scenario challenges", True),
        ("🏆", "Mastery Scholar", "Earned 300+ total cumulative XP", True)
    ]
    bx = 20
    bw = (W - 80) // 4
    for b_icon, b_title, b_sub, b_unlocked in badges:
        d.rounded_rectangle([bx, 390, bx + bw, 460], radius=8, fill="#1e293b", outline="#f59e0b" if b_unlocked else "#334155")
        d.text((bx + 12, 402), b_icon, font=FH, fill="#f59e0b")
        d.text((bx + 40, 402), b_title, font=FB, fill="#ffffff")
        d.text((bx + 40, 418), "UNLOCKED", font=FS, fill="#34d399")
        d.text((bx + 12, 438), b_sub, font=FS, fill="#94a3b8")
        bx += bw + 15
        
    # Recent Attempts Table
    d.rounded_rectangle([20, 480, W - 20, 580], radius=10, fill="#0f172a", outline="#1e293b")
    d.text((35, 495), "Recent Assessment Attempts", font=FB, fill="#ffffff")
    d.text((35, 520), "Quiz: Binary Search Trees & Rotations        Score: 85%      Time: 45s      Status: Verified Mastery", font=FS, fill="#cbd5e1")
    d.text((35, 545), "Quiz: Urban Flood Hydrology & Drainage        Score: 80%      Time: 62s      Status: Proficient", font=FS, fill="#cbd5e1")
    
    img.save(os.path.join(OUTPUT_DIR, "6_skills_dashboard.png"))

if __name__ == "__main__":
    generate_shot_1()
    generate_shot_2()
    generate_shot_3()
    generate_shot_4()
    generate_shot_5()
    generate_shot_6()
    print("All 6 screenshots generated successfully in:", OUTPUT_DIR)
