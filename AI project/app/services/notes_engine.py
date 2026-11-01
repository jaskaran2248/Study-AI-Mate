"""
StudyMate AI - Notes Generation Engine
Generates structured study notes, cheat sheets, flashcards, mind maps, and glossaries.
Emphasizes active recall, intuitive analogies, and structured conceptual mastery.
"""
import re
import json
from typing import Dict, Any, List

def generate_study_notes(text: str, title: str, subject: str = "General Studies") -> Dict[str, Any]:
    """
    Extracts key concepts, generates analogies, flashcards, mindmaps, and cheat sheets.
    """
    cleaned_text = text.strip()
    sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', cleaned_text) if len(s.strip()) > 15]
    
    # 1. Executive Summary Generation
    if len(sentences) <= 3:
        summary = cleaned_text
    else:
        intro_sentence = sentences[0]
        def_sentences = [s for s in sentences[1:15] if any(w in s.lower() for w in ['is defined as', 'refers to', 'means', 'plays a key role', 'important', 'used to', 'allows', 'enables'])]
        concl_sentences = [s for s in sentences[-3:] if any(w in s.lower() for w in ['therefore', 'in conclusion', 'overall', 'essential', 'crucial', 'future'])]
        
        selected = [intro_sentence]
        if def_sentences:
            selected.append(def_sentences[0])
        elif len(sentences) > 2:
            selected.append(sentences[1])
            
        if concl_sentences:
            selected.append(concl_sentences[0])
        elif len(sentences) > 4:
            selected.append(sentences[min(4, len(sentences)-1)])
            
        summary = " ".join(selected)

    # 2. Extract Key Concepts & Build Pedagogical Analogies
    concept_candidates = []
    
    colon_matches = re.findall(r'(?:^|\n)([A-Z][A-Za-z0-9\s_-]{2,30}):\s*([^\n]{20,250})', cleaned_text)
    for c_title, c_desc in colon_matches:
        concept_candidates.append((c_title.strip(), c_desc.strip()))

    list_matches = re.findall(r'(?:^|\n)[-*•\d\.]+\s+([A-Z][A-Za-z0-9\s_-]{2,30})[\s–—:\-]+([^\n]{20,250})', cleaned_text)
    for l_title, l_desc in list_matches:
        concept_candidates.append((l_title.strip(), l_desc.strip()))

    md_headings = re.findall(r'(?:^|\n)#{1,3}\s+([A-Za-z0-9\s_-]{3,40})\n+([^\n#]{20,300})', cleaned_text)
    for h_title, h_desc in md_headings:
        concept_candidates.append((h_title.strip(), h_desc.strip()))

    if len(concept_candidates) < 4:
        for s in sentences:
            m = re.search(r'\b([A-Z][a-z0-9]+(?:\s+[A-Z][a-z0-9]+)?)\s+(?:is|are|refers to|represents)\s+([^,.;]{15,180})', s)
            if m:
                c_title = m.group(1).strip()
                c_desc = f"{c_title} is {m.group(2).strip()}."
                if len(c_title) > 3 and c_title.lower() not in ['this', 'that', 'there', 'it', 'here']:
                    concept_candidates.append((c_title, c_desc))

    if len(concept_candidates) < 3:
        words = re.findall(r'\b[A-Z][a-z]{3,}\b', cleaned_text)
        stopwords = {'This', 'That', 'These', 'Those', 'With', 'From', 'When', 'What', 'Where', 'Which', 'Then', 'Also', 'Some', 'Most', 'Every'}
        filtered = [w for w in words if w not in stopwords]
        freq = {}
        for w in filtered:
            freq[w] = freq.get(w, 0) + 1
        top_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]
        for w, _ in top_words:
            matching_s = next((s for s in sentences if w.lower() in s.lower()), f"{w} is an essential foundational concept in {subject}.")
            concept_candidates.append((w, matching_s))

    seen = set()
    unique_concepts = []
    for c_title, c_desc in concept_candidates:
        slug = c_title.lower().strip()
        if slug not in seen and len(slug) >= 3:
            seen.add(slug)
            unique_concepts.append((c_title, c_desc))

    key_concepts = []
    analogies_pool = [
        "Think of it like a public library catalog: indexing information allows anyone to retrieve what they need in constant time.",
        "Similar to an electrical grid or water pipeline: efficiency increases when load is distributed evenly across nodes.",
        "Comparable to building a skyscraper: a sturdy architectural foundation prevents catastrophic failure under stress.",
        "Like an orchestra conductor: synchronizing individual instruments ensures harmonious, error-free collective execution.",
        "Just like a biological immune system: identifying signatures early prevents widespread system vulnerability.",
        "Like a GPS navigation routing system: calculating optimal paths dynamically avoids traffic bottlenecks."
    ]

    for i, (c_name, c_def) in enumerate(unique_concepts[:8]):
        analogy = analogies_pool[i % len(analogies_pool)]
        real_app = f"Implemented in real-world {subject} architectures to ensure scalable and fault-tolerant performance."
        insight = f"Foundational pillar for professional competency and advanced system analysis in {c_name}."
        
        key_concepts.append({
            "concept": c_name,
            "definition": c_def,
            "analogy": analogy,
            "real_world_application": real_app,
            "practical_insight": insight
        })

    # 3. Cheat Sheet Generation (Key Rules / Syntax / Theorems)
    cheat_sheet = []
    rule_patterns = [
        ("Core Principle", f"Mastery of {title} requires understanding fundamental axioms and operational parameters."),
        ("Execution Best Practice", "Always validate inputs, analyze edge cases, and maintain clean separation of concerns."),
        ("Performance & Complexity", "Prioritize algorithms and systems with bounded time/resource overhead."),
        ("Troubleshooting Rule", "Inspect error logs, verify state consistency, and test isolated components sequentially.")
    ]
    for idx, (rule_title, default_rule) in enumerate(rule_patterns):
        snippet = sentences[idx % len(sentences)] if sentences else default_rule
        cheat_sheet.append({
            "topic": f"{rule_title}: {unique_concepts[idx % len(unique_concepts)][0] if unique_concepts else title}",
            "rules_or_formula": snippet[:160] + ("..." if len(snippet) > 160 else ""),
            "quick_tip": f"Pro-Tip: Review this formula/rule before tackling intermediate & advanced challenges."
        })

    # 4. Active Recall Flashcards Deck
    flashcards = []
    for idx, c in enumerate(key_concepts):
        diff = "Basic" if idx < 3 else ("Intermediate" if idx < 6 else "Advanced")
        flashcards.append({
            "front": f"What is {c['concept']} and what role does it serve in {subject}?",
            "back": f"{c['definition']}\n\nAnalogy: {c['analogy']}",
            "tag": c['concept'],
            "difficulty": diff
        })

    if len(sentences) >= 3:
        flashcards.append({
            "front": f"Explain the practical significance of: '{sentences[min(2, len(sentences)-1)][:90]}...'",
            "back": f"This principle ensures robust execution, scalability, and predictable outcomes in {subject}.",
            "tag": "Application",
            "difficulty": "Intermediate"
        })
        flashcards.append({
            "front": f"What is the high-level system impact of {title} in practical environments?",
            "back": f"It establishes verified operational patterns, reduces computational overhead, and ensures predictable behavior in {subject}.",
            "tag": "System Impact",
            "difficulty": "Advanced"
        })

    # 5. Visual Mind Map (Mermaid + Markdown Outline)
    mindmap_nodes = [f'  Root["📘 {title}"]']
    for idx, c in enumerate(key_concepts[:6]):
        cid = f"C{idx+1}"
        safe_name = re.sub(r'[^A-Za-z0-9\s]', '', c['concept'])[:25]
        mindmap_nodes.append(f'  Root --> {cid}["{safe_name}"]')
        mindmap_nodes.append(f'  {cid} --> {cid}_app["Practical Application"]')
    
    mermaid_chart = "graph TD\n" + "\n".join(mindmap_nodes)

    # 6. Glossary Generation
    glossary = []
    for c in key_concepts:
        glossary.append({
            "term": c['concept'],
            "definition": c['definition']
        })

    return {
        "title": title or "Comprehensive Study Notes",
        "summary": summary,
        "key_concepts": key_concepts,
        "cheat_sheet": cheat_sheet,
        "flashcards": flashcards,
        "mindmap": mermaid_chart,
        "glossary": glossary
    }
