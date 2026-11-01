"""
StudyMate AI - Sample Data & Curated Learning Modules
Seeds the database with high-yield sample documents, notes, and quizzes.
Ensures the app is immediately full of rich, interactive content upon initial launch.
"""
import os
import json
from app.database import get_connection
from app.services.text_extractor import compute_document_metadata
from app.services.notes_engine import generate_study_notes
from app.services.question_engine import generate_tiered_quiz

SAMPLE_MODULES = [
    {
        "title": "Python Programming & Algorithmic Problem Solving",
        "subject": "Computer Science & Engineering",
        "sdg_target": "Digital Literacy & Software Systems",
        "filename": "python_algorithms.md",
        "content": """# Python Programming & Algorithmic Thinking

Python is a high-level, interpreted programming language designed for readability and rapid development. In modern software engineering, Python serves as the primary gateway for computational thinking and technical literacy.

## Core Language Foundations

Variables: In Python, variables are dynamically typed references to objects stored in heap memory. Unlike statically typed languages, variable names do not dictate memory allocations directly.
Data Structures: Core built-in structures include lists (dynamic arrays with O(1) amortized append), dictionaries (hash maps with average O(1) key lookup), tuples (immutable sequences), and sets (hash-based unique collections).
List Comprehensions: Provide a concise syntax for transforming iterables: `[x**2 for x in items if x % 2 == 0]`.
Functions: First-class citizens in Python. Functions can be passed as arguments, assigned to variables, and returned from other functions.

## Algorithmic Complexity & Optimization

Time Complexity: Big O notation measures the asymptotic upper bound of an algorithm's execution time as input size n approaches infinity.
Binary Search: Requires a sorted sequence and operates in O(log n) time by halving the search space at each iteration.
Sorting Algorithms: Python's built-in `sorted()` utilizes Timsort, an adaptive hybrid of Merge Sort and Insertion Sort with O(n log n) worst-case time complexity.
Memory Management: Python utilizes automatic reference counting combined with a cyclic garbage collector to reclaim unused heap memory.

## Asynchronous & Concurrent Execution

Generators: Functions utilizing `yield` return lazy iterators that produce values on demand, maintaining low memory overhead when processing massive datasets.
Decorators: Higher-order functions that modify or extend the behavior of callable objects without permanently changing their source code.
AsyncIO: Single-threaded cooperative multitasking model utilizing an event loop for non-blocking I/O operations.

## Practical Engineering Significance

Algorithmic thinking enables engineers to decompose complex real-world problems into verifiable, scalable sub-components."""
    },
    {
        "title": "Climate Science & Clean Energy Technologies",
        "subject": "Environmental Science",
        "sdg_target": "Renewable Thermodynamics & Clean Infrastructure",
        "filename": "climate_clean_energy.txt",
        "content": """Climate Science & Renewable Energy Engineering

Transitioning to modern power systems requires understanding renewable thermodynamics, energy conversion efficiency, and sustainable infrastructure.

Photovoltaic Solar Energy: Photovoltaic cells convert photons directly into electricity via the photoelectric effect in semiconductor p-n junctions. Silicon wafer cells achieve practical efficiencies between 18% and 23%.
Wind Turbine Aerodynamics: Wind kinetic energy is converted into mechanical rotation. Betz's law establishes the theoretical maximum power extraction limit of an ideal turbine rotor at 59.3%.
Grid-Scale Energy Storage: Renewable intermittency necessitates energy storage solutions, including lithium-iron-phosphate (LFP) batteries, pumped hydroelectric storage, and green hydrogen electrolysis.
Greenhouse Gas Life Cycle Assessment: Life cycle assessment (LCA) quantifies carbon dioxide equivalent emissions across extraction, manufacturing, operation, and decommissioning phases.
Smart Grid Modernization: Integrating distributed energy resources (DERs) requires automated load balancing, phasor measurement units, and bidirectional metering."""
    },
    {
        "title": "AI Ethics, Bias Mitigation & Inclusive Systems",
        "subject": "Artificial Intelligence & Ethics",
        "sdg_target": "Algorithmic Fairness & Model Transparency",
        "filename": "ai_ethics_systems.md",
        "content": """Artificial Intelligence Ethics & Inclusive Systems

As machine learning systems govern critical infrastructure, ensuring equitable performance, algorithmic transparency, and bias mitigation is paramount.

Algorithmic Bias: Machine learning models inherit and amplify systematic historical biases present in training corpora. In automated evaluation systems, uncalibrated models can disproportionately disadvantage specific groups.
Explainable AI (XAI): Refers to methods and techniques that produce human-interpretable explanations for model predictions, such as SHAP (Shapley Additive exPlanations) and LIME.
Differential Privacy: Mathematical framework ensuring that the inclusion or exclusion of any individual record in a dataset cannot be determined from aggregate query outputs, protecting user data privacy.
Universal Design for Learning (UDL): Framework providing multiple means of representation, engagement, and expression, ensuring diverse users have equal access.
Hallucination Detection: Mechanistic interpretability techniques that detect factual divergence in large language models before presenting explanations to users."""
    }
]

def seed_sample_data():
    """Seeds the database with curated sample documents, notes, and quizzes if empty."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as count FROM documents")
    row = cursor.fetchone()
    if row and row['count'] > 0:
        conn.close()
        return

    print("Seeding StudyMate AI with curated learning modules...")

    for module in SAMPLE_MODULES:
        meta = compute_document_metadata(module['content'])
        
        sample_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_materials", module['filename'])
        try:
            with open(sample_path, 'w', encoding='utf-8') as f:
                f.write(module['content'])
        except Exception:
            pass

        cursor.execute("""
        INSERT INTO documents (
            title, filename, file_type, content, word_count,
            reading_time_min, subject, sdg_target, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            module['title'], module['filename'], os.path.splitext(module['filename'])[1][1:],
            module['content'], meta['word_count'], meta['reading_time_min'],
            module['subject'], module['sdg_target'], meta['tags']
        ))
        doc_id = cursor.lastrowid

        notes_data = generate_study_notes(module['content'], module['title'], module['subject'])
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

        quiz_data = generate_tiered_quiz(
            module['content'], module['title'],
            difficulty_tier="Adaptive Mix",
            question_count=8,
            time_limit_min=12,
            custom_topic=module['title']
        )
        
        cursor.execute("""
        INSERT INTO quizzes (
            document_id, title, topic, description,
            difficulty_tier, question_count, time_limit_min, tags
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc_id, quiz_data['title'], quiz_data['topic'],
            quiz_data['description'], quiz_data['difficulty_tier'],
            quiz_data['question_count'], quiz_data['time_limit_min'],
            quiz_data['tags']
        ))
        quiz_id = cursor.lastrowid

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

    conn.commit()
    conn.close()
    print("Sample modules seeded successfully!")
