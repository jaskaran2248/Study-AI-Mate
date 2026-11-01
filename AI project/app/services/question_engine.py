"""
StudyMate AI - Question & Quiz Generation Engine
Generates tiered questions from Basic -> Intermediate -> Advanced -> Mastery.
Structured around Bloom's Revised Taxonomy to systematically build learner skills.
"""
import re
import random
import json
from typing import List, Dict, Any, Optional

BLOOM_LEVELS = {
    "basic": ["Remember", "Understand"],
    "intermediate": ["Apply", "Analyze"],
    "advanced": ["Evaluate", "Synthesize"],
    "mastery": ["Create", "Innovate & System Design"]
}

def generate_tiered_quiz(
    text: str,
    title: str,
    difficulty_tier: str = "Adaptive Mix",
    question_count: int = 10,
    time_limit_min: int = 15,
    custom_topic: str = ""
) -> Dict[str, Any]:
    """
    Generates a full quiz with questions across difficulty tiers.
    difficulty_tier can be: "Basic", "Intermediate", "Advanced", "Mastery", or "Adaptive Mix".
    """
    cleaned = text.strip()
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', cleaned) if len(s.strip()) > 20]
    if not sentences:
        sentences = [f"{title} is a core subject area in modern education."]

    concepts = extract_concept_pool(cleaned, title)
    tier_distribution = calculate_tier_distribution(difficulty_tier, question_count)
    all_questions = []
    
    # Basic Questions
    basic_q_count = tier_distribution.get("basic", 0)
    if basic_q_count > 0:
        basic_qs = generate_basic_questions(concepts, sentences, title, basic_q_count)
        all_questions.extend(basic_qs)
        
    # Intermediate Questions
    intermediate_q_count = tier_distribution.get("intermediate", 0)
    if intermediate_q_count > 0:
        inter_qs = generate_intermediate_questions(concepts, sentences, title, intermediate_q_count)
        all_questions.extend(inter_qs)
        
    # Advanced Questions
    advanced_q_count = tier_distribution.get("advanced", 0)
    if advanced_q_count > 0:
        adv_qs = generate_advanced_questions(concepts, sentences, title, advanced_q_count)
        all_questions.extend(adv_qs)
        
    # Mastery Questions
    mastery_q_count = tier_distribution.get("mastery", 0)
    if mastery_q_count > 0:
        master_qs = generate_mastery_questions(concepts, sentences, title, mastery_q_count)
        all_questions.extend(master_qs)

    while len(all_questions) < question_count:
        fallback_q = generate_adaptive_fallback_question(concepts, sentences, title, len(all_questions)+1)
        all_questions.append(fallback_q)

    final_questions = all_questions[:question_count]
    for idx, q in enumerate(final_questions):
        q["index"] = idx + 1

    return {
        "title": f"Quiz: {title} ({difficulty_tier} Mastery)",
        "topic": custom_topic or title,
        "description": f"Comprehensive skill assessment covering foundational recall to expert synthesis on {title}.",
        "difficulty_tier": difficulty_tier,
        "question_count": len(final_questions),
        "time_limit_min": time_limit_min,
        "tags": f"{title}, Skill Building, {difficulty_tier}",
        "questions": final_questions
    }

def calculate_tier_distribution(difficulty_tier: str, total_count: int) -> Dict[str, int]:
    """Calculates question count distribution across tiers."""
    tier = difficulty_tier.lower()
    
    if "basic" in tier:
        return {"basic": total_count, "intermediate": 0, "advanced": 0, "mastery": 0}
    elif "intermediate" in tier:
        return {"basic": 0, "intermediate": total_count, "advanced": 0, "mastery": 0}
    elif "advanced" in tier:
        return {"basic": 0, "intermediate": 0, "advanced": total_count, "mastery": 0}
    elif "mastery" in tier:
        return {"basic": 0, "intermediate": 0, "advanced": 0, "mastery": total_count}
    else:
        # Adaptive Mix: Balanced ladder progression (e.g. 30% Basic, 35% Intermediate, 25% Advanced, 10% Mastery)
        b = max(1, int(round(total_count * 0.30)))
        i = max(1, int(round(total_count * 0.35)))
        a = max(1, int(round(total_count * 0.25)))
        m = total_count - (b + i + a)
        if m < 1:
            m = 1
            if i > 1:
                i -= 1
        return {"basic": b, "intermediate": i, "advanced": a, "mastery": m}

def extract_concept_pool(text: str, default_title: str) -> List[Dict[str, str]]:
    """Extracts concepts and definition pairs from raw text."""
    pool = []
    
    colons = re.findall(r'(?:^|\n)([A-Z][A-Za-z0-9\s_-]{2,30}):\s*([^\n]{20,250})', text)
    for c_title, c_desc in colons:
        pool.append({"name": c_title.strip(), "description": c_desc.strip()})
        
    bullets = re.findall(r'(?:^|\n)[-*•\d\.]+\s+([A-Z][A-Za-z0-9\s_-]{2,30})[\s–—:\-]+([^\n]{20,250})', text)
    for b_title, b_desc in bullets:
        pool.append({"name": b_title.strip(), "description": b_desc.strip()})

    sentences = re.split(r'[.!?]\s+', text)
    for s in sentences:
        m = re.search(r'\b([A-Z][A-Za-z0-9\s]{2,25})\s+(?:is defined as|is|refers to|represents)\s+([^,.;]{15,150})', s)
        if m:
            name = m.group(1).strip()
            if name.lower() not in ['this', 'that', 'it', 'there', 'they']:
                pool.append({"name": name, "description": m.group(2).strip()})

    if len(pool) < 4:
        words = re.findall(r'\b[A-Z][a-z]{3,}\b', text)
        stopwords = {'This', 'That', 'These', 'Those', 'With', 'From', 'When', 'What', 'Where', 'Which'}
        unique_words = list(dict.fromkeys([w for w in words if w not in stopwords]))
        for w in unique_words[:6]:
            pool.append({
                "name": w,
                "description": f"Core component of {default_title} governing system behavior and operational reliability."
            })
            
    if not pool:
        pool = [
            {"name": default_title, "description": f"Primary subject domain focused on {default_title} competencies."},
            {"name": "Foundational Principles", "description": "Core concepts and laws establishing theoretical consistency."},
            {"name": "System Architecture", "description": "The structural design and interaction between components."},
            {"name": "Practical Optimization", "description": "Techniques to maximize efficiency and minimize latency or error rates."}
        ]
        
    return pool

# ==================== TIER GENERATORS ====================

def generate_basic_questions(concepts: List[Dict[str, str]], sentences: List[str], title: str, count: int) -> List[Dict[str, Any]]:
    """Tier 1: Basic / Foundational (Remember, Understand)"""
    questions = []
    
    distractor_templates = [
        "A legacy protocol that has been entirely deprecated due to structural vulnerabilities.",
        "An unrelated peripheral mechanism that only executes during catastrophic hardware failure.",
        "A static data structure that cannot adapt to dynamic changes or user interactions.",
        "A proprietary standard restricted to non-standard closed commercial environments."
    ]
    
    for i in range(count):
        concept = concepts[i % len(concepts)]
        other_concepts = [c for c in concepts if c['name'] != concept['name']]
        
        if i % 2 == 0:
            correct_ans = concept['description']
            if len(correct_ans) > 120:
                correct_ans = correct_ans[:117] + "..."
                
            distractors = []
            if other_concepts:
                for oc in other_concepts[:3]:
                    desc = oc['description']
                    if len(desc) > 120:
                        desc = desc[:117] + "..."
                    distractors.append(desc)
            while len(distractors) < 3:
                distractors.append(distractor_templates[len(distractors) % len(distractor_templates)])
                
            options = [correct_ans] + distractors[:3]
            random.shuffle(options)
            
            questions.append({
                "question_text": f"What is the primary definition and role of '{concept['name']}' in {title}?",
                "question_type": "mcq",
                "difficulty": "basic",
                "bloom_level": "Remember & Understand",
                "options": options,
                "correct_answer": correct_ans,
                "explanation": f"'{concept['name']}' is defined as: {concept['description']}. Understanding foundational terms is essential to mastering {title}.",
                "hint": f"Recall how '{concept['name']}' was defined in the foundational overview.",
                "points": 10,
                "subtopic": concept['name']
            })
        else:
            is_true = (i % 4 != 1)
            if is_true:
                q_text = f"True or False: In {title}, '{concept['name']}' plays an active role in {concept['description'][:80]}."
                correct_ans = "True"
                expl = f"Correct! '{concept['name']}' indeed directly relates to {concept['description']}."
            else:
                q_text = f"True or False: In {title}, '{concept['name']}' is considered completely irrelevant and has zero application."
                correct_ans = "False"
                expl = f"False! '{concept['name']}' is actually vital: {concept['description']}."
                
            questions.append({
                "question_text": q_text,
                "question_type": "tf",
                "difficulty": "basic",
                "bloom_level": "Understand",
                "options": ["True", "False"],
                "correct_answer": correct_ans,
                "explanation": expl,
                "hint": f"Consider the importance of '{concept['name']}' in standard {title} workflows.",
                "points": 10,
                "subtopic": concept['name']
            })
            
    return questions

def generate_intermediate_questions(concepts: List[Dict[str, str]], sentences: List[str], title: str, count: int) -> List[Dict[str, Any]]:
    """Tier 2: Intermediate (Apply, Analyze)"""
    questions = []
    
    for i in range(count):
        concept = concepts[i % len(concepts)]
        
        scenario_types = [
            (
                f"You are building a production implementation in {title}. When integrating '{concept['name']}', what is the recommended engineering approach?",
                f"Ensure modular abstraction and validate data contracts before processing.",
                [
                    "Bypass validation to maximize raw throughput at the expense of integrity.",
                    "Hardcode all operational thresholds directly into client-side templates.",
                    "Execute the logic synchronously on the main thread without exception handling."
                ],
                f"Applying '{concept['name']}' safely requires modularity and strict boundary validation to prevent silent regressions."
            ),
            (
                f"In a practical scenario, an engineer observes that '{concept['name']}' exhibits unexpected performance degradation. What is the most likely root cause?",
                f"Inefficient resource allocation or unbounded state accumulation in memory.",
                [
                    "Using standard UTF-8 text formatting instead of raw binary hex.",
                    "The system being connected to an open-source technical repository.",
                    "Executing the process within a standard Linux or Windows kernel environment."
                ],
                f"Performance degradation in '{concept['name']}' typically stems from resource leaks, improper indexing, or unbounded state."
            ),
            (
                f"How does '{concept['name']}' compare to alternative approaches in {title}?",
                f"It offers superior predictability and maintainability under standard operational loads.",
                [
                    "It eliminates the need for any unit testing or peer review.",
                    "It can only be executed on specialized hardware accelerators.",
                    "It restricts user access completely to single-threaded sequential execution."
                ],
                f"In practice, '{concept['name']}' is favored because it provides balanced trade-offs, structured predictability, and long-term maintainability."
            )
        ]
        
        q_stem, correct_opt, distractors, explanation = scenario_types[i % len(scenario_types)]
        options = [correct_opt] + distractors
        random.shuffle(options)
        
        questions.append({
            "question_text": q_stem,
            "question_type": "mcq",
            "difficulty": "intermediate",
            "bloom_level": "Apply & Analyze",
            "options": options,
            "correct_answer": correct_opt,
            "explanation": explanation,
            "hint": "Analyze the real-world trade-offs between system safety, scalability, and code maintainability.",
            "points": 15,
            "subtopic": f"{concept['name']} (Applied)"
        })
        
    return questions

def generate_advanced_questions(concepts: List[Dict[str, str]], sentences: List[str], title: str, count: int) -> List[Dict[str, Any]]:
    """Tier 3: Advanced (Evaluate, Synthesize)"""
    questions = []
    
    for i in range(count):
        concept = concepts[i % len(concepts)]
        
        advanced_scenarios = [
            (
                f"Critically evaluate: When architecting a high-throughput, fault-tolerant system around '{concept['name']}', which architectural trade-off must be prioritized?",
                f"Balancing consistency guarantees against network partition tolerance (CAP theorem implications).",
                [
                    "Eliminating all logging and metrics collectors to save minor disk I/O.",
                    "Forcing all client requests through a single non-replicated database instance.",
                    "Assuming network latency is always zero across distributed nodes."
                ],
                f"At an advanced engineering level, '{concept['name']}' requires managing distributed consistency vs availability trade-offs, resilient failovers, and idempotency."
            ),
            (
                f"Suppose a severe race condition or edge case occurs during the lifecycle of '{concept['name']}'. What synthesis strategy resolves the issue cleanly?",
                f"Implement immutable state transitions and distributed optimistic concurrency locks.",
                [
                    "Disable multithreading and reboot the machine whenever a collision occurs.",
                    "Suppress all warnings and return null to the caller silently.",
                    "Increase server RAM without addressing concurrency mechanics."
                ],
                f"Resolving concurrency edge cases in '{concept['name']}' requires immutable state transitions and deterministic locking or queue serialization."
            )
        ]
        
        q_stem, correct_opt, distractors, explanation = advanced_scenarios[i % len(advanced_scenarios)]
        options = [correct_opt] + distractors
        random.shuffle(options)
        
        questions.append({
            "question_text": q_stem,
            "question_type": "mcq",
            "difficulty": "advanced",
            "bloom_level": "Evaluate & Synthesize",
            "options": options,
            "correct_answer": correct_opt,
            "explanation": explanation,
            "hint": "Think about edge conditions, distributed system guarantees, and fault-tolerance patterns.",
            "points": 20,
            "subtopic": f"{concept['name']} (Advanced Evaluation)"
        })
        
    return questions

def generate_mastery_questions(concepts: List[Dict[str, str]], sentences: List[str], title: str, count: int) -> List[Dict[str, Any]]:
    """Tier 4: Mastery / Expert (Create, System Design & Architecture)"""
    questions = []
    
    for i in range(count):
        concept = concepts[i % len(concepts)]
        
        mastery_scenarios = [
            (
                f"[System Design & Architecture] You are tasked with deploying an enterprise-grade, fault-tolerant platform utilizing '{concept['name']}' to serve high concurrent traffic. Which architectural design best guarantees high availability and resilient data consistency?",
                f"A decentralized, distributed event-driven architecture with localized caching, backpressure control, and lightweight state serialization.",
                [
                    "A monolithic server hosted in a single data center requiring uncompressed high-bandwidth synchronization.",
                    "A rigid synchronous pipeline that halts all processing if a single downstream consumer experiences latency.",
                    "An unoptimized polling routine that queries the primary database on an infinite tight loop."
                ],
                f"Mastery in system architecture demands resilient design patterns: event-driven queues, localized caching, and backpressure control ensure predictable scalability under load."
            ),
            (
                f"[Expert Synthesis & Innovation] If you were to formulate a novel evolution of '{concept['name']}' to address future technical constraints, what core innovation should anchor your paradigm?",
                f"Self-healing adaptive heuristics capable of dynamic self-reconfiguration based on real-time observational telemetry.",
                [
                    "A return to legacy batch scheduling with rigid manual interventions.",
                    "Hardcoded lookup tables that reject any unknown input without remediation.",
                    "Complete reliance on unverified third-party scripts without security validation."
                ],
                f"True mastery involves innovating beyond existing patterns: adaptive heuristics and automated self-healing enable resilient, future-proof systems."
            )
        ]
        
        q_stem, correct_opt, distractors, explanation = mastery_scenarios[i % len(mastery_scenarios)]
        options = [correct_opt] + distractors
        random.shuffle(options)
        
        questions.append({
            "question_text": q_stem,
            "question_type": "mcq",
            "difficulty": "mastery",
            "bloom_level": "Create & Innovate",
            "options": options,
            "correct_answer": correct_opt,
            "explanation": explanation,
            "hint": "Focus on high-level system architecture, resilient access, and forward-looking innovations.",
            "points": 25,
            "subtopic": f"{concept['name']} (System Design)"
        })
        
    return questions

def generate_adaptive_fallback_question(concepts: List[Dict[str, str]], sentences: List[str], title: str, index: int) -> Dict[str, Any]:
    """Generates an additional question if needed to meet exact count."""
    concept = concepts[index % len(concepts)]
    correct = f"It provides structured, verifiable foundations for {concept['name']}."
    distractors = [
        f"It causes irreversible corruption in the {title} data pipeline.",
        "It was invented exclusively for analog radio transmission in 1920.",
        "It violates all modern security and architectural standards."
    ]
    options = [correct] + distractors
    random.shuffle(options)
    
    return {
        "question_text": f"Why is understanding '{concept['name']}' considered fundamental to developing technical mastery in {title}?",
        "question_type": "mcq",
        "difficulty": "intermediate",
        "bloom_level": "Analyze",
        "options": options,
        "correct_answer": correct,
        "explanation": f"Developing deep competency in {title} requires mastering {concept['name']} to reason about design choices and real-world system behavior.",
        "hint": "Consider the long-term impact on foundational skill building.",
        "points": 15,
        "subtopic": concept['name']
    }
