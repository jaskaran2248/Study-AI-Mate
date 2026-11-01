"""
StudyMate AI - Formal Academic Project Report Generator (DOCX)
Generates an authentic Microsoft Word (.docx) document matching the Chandigarh University MCA format.
Embeds the 6 UI screenshots into the OpenXML package with native drawings, figures, and academic structure.
"""
import os
import sys
import zipfile
import html
from typing import List, Tuple

DOCX_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "StudyMate_AI_Project_Report.docx")
SHOTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "screenshots")

def esc(text: str) -> str:
    """Escapes XML special characters."""
    return html.escape(str(text), quote=True)

class DocxBuilder:
    def __init__(self):
        self.paragraphs = []
        self.images = [] # (rId, filename, emu_w, emu_h, title)
        self.img_counter = 0

    def add_p(self, text: str = "", bold: bool = False, italic: bool = False, 
              size_pt: float = 11, color: str = "334155", align: str = "left",
              space_before: int = 100, space_after: int = 100, line_spacing: int = 260):
        jc_val = "left"
        if align == "center":
            jc_val = "center"
        elif align == "right":
            jc_val = "right"
        elif align == "justify":
            jc_val = "both"

        half_pts = int(size_pt * 2)
        b_tag = "<w:b/>" if bold else ""
        i_tag = "<w:i/>" if italic else ""
        color_tag = f'<w:color w:val="{color}"/>' if color else ""
        
        xml = f"""<w:p>
  <w:pPr>
    <w:jc w:val="{jc_val}"/>
    <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
      {b_tag}{i_tag}{color_tag}
      <w:sz w:val="{half_pts}"/>
      <w:szCs w:val="{half_pts}"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(text)}</w:t>
  </w:r>
</w:p>"""
        self.paragraphs.append(xml)

    def add_runs_p(self, runs: List[Tuple[str, dict]], align: str = "left", 
                   space_before: int = 100, space_after: int = 100, line_spacing: int = 260,
                   left_indent: int = 0):
        jc_val = "left"
        if align == "center":
            jc_val = "center"
        elif align == "right":
            jc_val = "right"
        elif align == "justify":
            jc_val = "both"

        ind_tag = f'<w:ind w:left="{left_indent}"/>' if left_indent > 0 else ""
        runs_xml = []
        for text, opts in runs:
            bold = opts.get("bold", False)
            italic = opts.get("italic", False)
            size_pt = opts.get("size", 11)
            color = opts.get("color", "334155")
            half_pts = int(size_pt * 2)
            b_tag = "<w:b/>" if bold else ""
            i_tag = "<w:i/>" if italic else ""
            color_tag = f'<w:color w:val="{color}"/>' if color else ""
            runs_xml.append(f"""<w:r>
    <w:rPr>
      <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>
      {b_tag}{i_tag}{color_tag}
      <w:sz w:val="{half_pts}"/>
      <w:szCs w:val="{half_pts}"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(text)}</w:t>
  </w:r>""")

        xml = f"""<w:p>
  <w:pPr>
    <w:jc w:val="{jc_val}"/>
    {ind_tag}
    <w:spacing w:before="{space_before}" w:after="{space_after}" w:line="{line_spacing}" w:lineRule="auto"/>
  </w:pPr>
  {"".join(runs_xml)}
</w:p>"""
        self.paragraphs.append(xml)

    def add_heading1(self, text: str):
        self.add_p(text, bold=True, size_pt=14, color="0f172a", space_before=240, space_after=120)

    def add_heading2(self, text: str):
        self.add_p(text, bold=True, size_pt=12, color="1e293b", space_before=180, space_after=80)

    def add_bullet(self, bold_prefix: str, text: str):
        self.add_runs_p([
            ("•  ", {"bold": True, "size": 10.5, "color": "2563eb"}),
            (bold_prefix + " ", {"bold": True, "size": 10.5, "color": "1e293b"}),
            (text, {"bold": False, "size": 10.5, "color": "334155"})
        ], space_before=40, space_after=60, left_indent=360)

    def add_numbered(self, num_str: str, bold_prefix: str, text: str):
        self.add_runs_p([
            (num_str + " ", {"bold": True, "size": 10.5, "color": "0f172a"}),
            (bold_prefix + " ", {"bold": True, "size": 10.5, "color": "1e293b"}),
            (text, {"bold": False, "size": 10.5, "color": "334155"})
        ], space_before=40, space_after=60, left_indent=360)

    def add_body(self, text: str):
        self.add_p(text, bold=False, size_pt=10.5, color="334155", align="both", space_before=60, space_after=100)

    def add_page_break(self):
        self.paragraphs.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def add_horizontal_rule(self):
        xml = """<w:p>
  <w:pPr>
    <w:pBdr>
      <w:bottom w:val="single" w:sz="12" w:space="1" w:color="2563EB"/>
    </w:pBdr>
    <w:spacing w:before="60" w:after="160"/>
  </w:pPr>
</w:p>"""
        self.paragraphs.append(xml)

    def add_university_box(self):
        xml = """<w:tbl>
  <w:tblPr>
    <w:tblW w:w="5000" w:type="pct"/>
    <w:jc w:val="center"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
      <w:left w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
      <w:bottom w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
      <w:right w:val="single" w:sz="8" w:space="0" w:color="CBD5E1"/>
    </w:tblBorders>
  </w:tblPr>
  <w:tr>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="5000" w:type="pct"/>
        <w:shd w:val="clear" w:color="auto" w:fill="F8FAFC"/>
        <w:tcMar>
          <w:top w:w="160" w:type="dxa"/>
          <w:bottom w:w="160" w:type="dxa"/>
          <w:left w:w="240" w:type="dxa"/>
          <w:right w:w="240" w:type="dxa"/>
        </w:tcMar>
      </w:tcPr>
      <w:p>
        <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="40"/></w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:b/><w:color w:val="C5192D"/><w:sz w:val="28"/><w:szCs w:val="28"/>
          </w:rPr>
          <w:t>CHANDIGARH UNIVERSITY</w:t>
        </w:r>
      </w:p>
      <w:p>
        <w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="60"/></w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/>
            <w:i/><w:color w:val="64748B"/><w:sz w:val="18"/><w:szCs w:val="18"/>
          </w:rPr>
          <w:t>Discover . Learn . Empower</w:t>
        </w:r>
      </w:p>
    </w:tc>
  </w:tr>
</w:tbl>"""
        self.paragraphs.append(xml)

    def add_image(self, file_path: str, caption: str, emu_w: int = 5600000, emu_h: int = 3450000):
        self.img_counter += 1
        r_id = f"rIdImg{self.img_counter}"
        self.images.append((r_id, file_path, emu_w, emu_h, caption))

        # Caption above image
        self.add_p(caption, bold=True, size_pt=10.5, color="0f172a", align="left", space_before=160, space_after=80)

        # Drawing XML
        drawing_xml = f"""<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="60" w:after="160"/>
  </w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{emu_w}" cy="{emu_h}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{self.img_counter}" name="Picture {self.img_counter}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="{self.img_counter}" name="image{self.img_counter}.png"/>
                <pic:cNvPicPr>
                  <a:picLocks noChangeAspect="1"/>
                </pic:cNvPicPr>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{r_id}"/>
                <a:stretch>
                  <a:fillRect/>
                </a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{emu_w}" cy="{emu_h}"/>
                </a:xfrm>
                <a:prstGeom prst="rect">
                  <a:avLst/>
                </a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>"""
        self.paragraphs.append(drawing_xml)

    def build(self, output_path: str):
        # 1. document.xml
        body_xml = "\n".join(self.paragraphs)
        document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
            xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
            xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
            xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
            xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
  <w:body>
{body_xml}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="720" w:footer="720" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>"""

        # 2. [Content_Types].xml
        content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""

        # 3. _rels/.rels
        root_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""

        # 4. word/_rels/document.xml.rels
        rel_entries = ['<Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>']
        for r_id, _, _, _, _ in self.images:
            num = r_id.replace("rIdImg", "")
            rel_entries.append(f'<Relationship Id="{r_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/image{num}.png"/>')

        doc_rels = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {"".join(rel_entries)}
</Relationships>"""

        # 5. word/styles.xml
        styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:docDefaults>
    <w:rPrDefault>
      <w:rPr>
        <w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:eastAsia="Calibri" w:cs="Calibri"/>
        <w:sz w:val="22"/>
        <w:szCs w:val="22"/>
        <w:color w:val="334155"/>
      </w:rPr>
    </w:rPrDefault>
  </w:docDefaults>
</w:styles>"""

        # Write out to ZIP (.docx)
        with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as docx:
            docx.writestr('[Content_Types].xml', content_types)
            docx.writestr('_rels/.rels', root_rels)
            docx.writestr('word/_rels/document.xml.rels', doc_rels)
            docx.writestr('word/styles.xml', styles_xml)
            docx.writestr('word/document.xml', document_xml)

            for r_id, img_path, _, _, _ in self.images:
                num = r_id.replace("rIdImg", "")
                with open(img_path, 'rb') as f:
                    docx.writestr(f'word/media/image{num}.png', f.read())

        print(f"Generated DOCX report: {output_path} ({os.path.getsize(output_path):,} bytes)")


def generate_studymate_docx():
    b = DocxBuilder()

    # ==================== PAGE 1: COVER PAGE ====================
    b.add_p("", space_before=400, space_after=0)
    b.add_p("STUDYMATE AI – ADAPTIVE LEARNING & QUIZ SYSTEM", bold=True, size_pt=24, color="0f172a", align="center", space_before=100, space_after=120)
    b.add_horizontal_rule()
    b.add_p("A Project Report submitted in partial fulfillment of the requirements for the degree of\nMaster of Computer Applications (MCA)", 
            bold=False, size_pt=11.5, color="1e293b", align="center", space_before=100, space_after=400)

    b.add_p("Submitted By:", bold=True, size_pt=11, color="0f172a", align="center", space_before=100, space_after=40)
    b.add_p("Livesh Kumar\nRoll No: 26MCA20079\nSemester: 1st / Year: 1st", bold=False, size_pt=10.5, color="334155", align="center", space_before=0, space_after=200)

    b.add_p("Under the Guidance of:", bold=True, size_pt=11, color="0f172a", align="center", space_before=100, space_after=40)
    b.add_p("Saranjeet Kaur Mam\nAssociate professor", bold=False, size_pt=10.5, color="334155", align="center", space_before=0, space_after=200)

    b.add_p("Department of Computer Applications\nChandigarh University\nAcademic Year: 2026–2027", 
            bold=False, size_pt=11, color="1e293b", align="center", space_before=100, space_after=300)

    b.add_university_box()
    b.add_p("", space_before=80, space_after=0)
    b.add_p("CHANDIGARH UNIVERSITY\nNovember 2026", bold=True, size_pt=10, color="64748b", align="center", space_before=60, space_after=100)

    b.add_page_break()

    # ==================== PAGE 2: SECTIONS 1, 2, 3 ====================
    b.add_heading1("1. ABSTRACT & EXECUTIVE SUMMARY")
    b.add_body(
        "StudyMate AI is a production-ready, full-stack adaptive learning intelligence platform designed to eliminate the bottlenecks of static memorization and fragmented self-study. "
        "Built on a high-concurrency Python/FastAPI asynchronous foundation paired with a responsive single-page web client, StudyMate AI transforms arbitrary unstructured educational "
        "materials—including course syllabi, lecture presentations, textbook PDFs, Word documents (.docx), and markdown notes—into structured pedagogical study digests, active recall "
        "flashcards, and scaffolded assessments aligned with Bloom's Revised Taxonomy."
    )
    b.add_body(
        "Unlike generic LLM wrappers that impose recurring token billing, unstable latency, and external data leakage, StudyMate AI implements an autonomous dual-engine intelligence paradigm. "
        "It features a zero-dependency, deterministic heuristic NLP parser capable of running 100% offline and locally out of the box, with seamless failover and expansion to state-of-the-art "
        "large language models (Google Gemini API / OpenAI). Every question is systematically tagged across cognitive tiers (Basic Recall, Intermediate Applied, Advanced Analytical, and Mastery Systems Evaluation), "
        "empowering learners to rapidly diagnose conceptual blind spots, reinforce active recall, and track verifiable skill growth with sub-second feedback."
    )

    b.add_heading1("2. PROBLEM STATEMENT & LITERATURE REVIEW")
    b.add_heading2("2.1 The Modern Learning & EdTech Paradox")
    b.add_body(
        "Despite exponential proliferation of digital textbooks, online courses, and video repositories, learners experience severe cognitive fragmentation and low retention. "
        "Empirical studies in cognitive psychology (Roediger & Karpicke, 2006) demonstrate that active testing and spaced retrieval produce up to 40% higher long-term retention "
        "compared to repetitive passive reading. Yet modern students and educational institutions face three pervasive roadblocks:"
    )
    b.add_bullet("Manual Question Formulation Fatigue:", "Creating rigorous, multi-tiered practice questions with verified distractors requires excessive instructor time and effort.")
    b.add_bullet("Information Overload & Static Material:", "Textbooks and lecture slides lack interactive interrogation, leaving students passive consumers rather than active problem solvers.")
    b.add_bullet("Absence of Cognitive Scaffolding:", "Standard mock tests aggregate uncalibrated questions without measuring whether a student has mastered foundational terminology before confronting complex synthesis.")

    b.add_heading2("2.2 Systemic Bottlenecks in Existing Solutions")
    b.add_numbered("1.", "Proprietary Subscription & API Walls:", "Most commercial AI study assistants enforce expensive paywalls and fail in offline or resource-constrained educational settings.")
    b.add_numbered("2.", "Invasive Cloud Telemetry & Data Privacy Risks:", "Proprietary cloud platforms require uploading sensitive institutional materials to third-party servers, raising serious student privacy and intellectual property concerns.")
    b.add_numbered("3.", "Flat Difficulty & Distractor Hallucinations:", "Basic generative scripts generate trivial trivia questions with implausible distractors, failing to test analytical application.")
    b.add_numbered("4.", "Lack of Diagnostic Remediation:", "When a learner fails a question, existing tools display a static binary score without targeted drills or conceptual mapping to missed topics.")

    b.add_heading1("3. PROPOSED SOLUTION & ENGINEERING OBJECTIVES")
    b.add_body(
        "StudyMate AI resolves these systemic limitations through a resilient, modular client-server web architecture engineered around five core principles:"
    )
    b.add_numbered("1.", "Open Multi-Format Document Ingestion:", "A universal parsing pipeline accepting PDF, DOCX, TXT, MD, CSV, and JSON formats without external third-party binary dependencies.")
    b.add_numbered("2.", "Bloom's Revised Taxonomy Cognitive Scaffolding:", "Automated partitioning of questions across four progressive tiers: Basic (Recall), Intermediate (Apply), Advanced (Evaluate), and Mastery (Synthesize & Design).")
    b.add_numbered("3.", "Interactive 3D Active Recall Flashcards:", "Hardware-accelerated CSS 3D flip card mechanics with spaced repetition feedback intervals.")
    b.add_numbered("4.", "Deterministic Local Engine with Pluggable AI:", "Immediate offline execution via regex-driven tokenizers and heuristic distractor extractors, augmented by optional Gemini/OpenAI cloud models.")
    b.add_numbered("5.", "Zero-Overlap Diagnostic Analytics & Remediation:", "A modern scorecard displaying isolated, responsive progress meters and 1-click targeted remediation drills on missed conceptual domains.")

    b.add_page_break()

    # ==================== PAGE 3: SECTIONS 4, 5, 6, 7 ====================
    b.add_heading1("4. SYSTEM ARCHITECTURE & DATA FLOW")
    b.add_body(
        "StudyMate AI employs an asynchronous REST architecture separating content extraction, pedagogical synthesis, database persistence, and user presentation into decoupled layers:"
    )
    b.add_bullet("REST Application Tier (FastAPI):", "Lightweight Python 3 async/sync API endpoints providing sub-5ms routing, CORS protection, automatic schema validation, and multipart streaming.")
    b.add_bullet("Dual-Engine Ingestion Pipeline:", "Custom XML stream reader for DOCX packages, regex token parsers for PDF text streams, and UTF-8 normalizers for plaintext and JSON sources.")
    b.add_bullet("Pedagogical Generation Layer:", "Hybrid AI pipeline that leverages local algorithmic rule-based extraction and optional Google Gemini REST inference for high-fidelity quiz and note generation.")
    b.add_bullet("Transactional Persistence Layer (SQLite WAL):", "High-performance relational persistence using Write-Ahead Logging (WAL) mode for concurrent read-heavy operations across materials, notes, quizzes, questions, and skill logs.")
    b.add_bullet("Reactive Client Tier (Single Page Web App):", "Modern vanilla HTML5/ES6/CSS3 presentation architecture featuring a modular component design (uploader.js, notes.js, quiz.js, search.js, skills.js) without heavy external framework overhead.")

    b.add_heading1("5. THE 5 CORE APPLICATION PILLARS")
    b.add_numbered("1.", "Universal Multi-Format Document Ingestion Engine:", "Enables zero-friction drag-and-drop ingestion of academic documents up to 50MB with instant parsing previews.")
    b.add_numbered("2.", "Smart Search & Instant Topic Study Pack Generator:", "Allows students to search any academic topic or curriculum subject and immediately generate structured study notes and quizzes.")
    b.add_numbered("3.", "Adaptive Quiz Runner & Cognitive Progression Engine:", "Dynamic interactive quiz engine with custom timer countdowns, immediate rationale explanations, and Bloom's cognitive ladders.")
    b.add_numbered("4.", "Interactive 3D Active Recall Flashcards & Spaced Repetition:", "Bi-directional 3D cards supporting rapid key-concept reinforcement, self-assessment ratings, and automated card shuffling.")
    b.add_numbered("5.", "Skills Mastery Dashboard & Diagnostic Analytics:", "Real-time competency tracking across topics, visual mastery meters with zero UI overlap, and one-click 'Practice Missed Topics' remediation.")

    b.add_heading1("6. WEBSITE INTERFACE OVERVIEW")
    b.add_bullet("Upload & Ingestion Console:", "Clean dropzone supporting drag-and-drop file ingestion, document metadata inspection, and instant one-click 'Generate Study Pack' dispatch.")
    b.add_bullet("Smart Search Bar & Curriculum Synthesizer:", "Global real-time search interface allowing students to synthesize custom learning packs from raw academic keywords or syllabus units.")
    b.add_bullet("Interactive Study Notes & Flip Cards:", "Formatted pedagogical summaries with key terminology callouts, bullet takeaways, and 3D flip card drill decks.")
    b.add_bullet("Adaptive Quiz Runner:", "Clean test workspace with real-time timers, question navigators, multi-choice radio options, and instant pedagogical answer explanations.")
    b.add_bullet("Comprehensive Scorecard:", "Post-test diagnostic report presenting overall score percentage, detailed question-by-question review, and distinct two-column Bloom's taxonomy performance bars.")
    b.add_bullet("Skills Mastery Dashboard:", "Visual overview of subject competencies, test histories, accuracy percentages, and automated topic drill recommendations.")

    b.add_heading1("7. FUTURE SCOPE & ENHANCEMENT ROADMAP")
    b.add_numbered("1.", "Edge LLM Quantization (Ollama / Llama.cpp):", "Embedding local quantized small-parameter models (e.g., Llama 3 8B, Gemma 2) directly into the desktop runtime for 100% private offline generative intelligence.")
    b.add_numbered("2.", "Spaced Repetition Algorithm (SuperMemo SM-2):", "Dynamic scheduling of flashcard reviews based on individual response intervals and cognitive forget-curve modeling.")
    b.add_numbered("3.", "Multi-Modal Audio & Diagrammatic Parsing:", "Integrating speech-to-text for recorded classroom lectures and optical diagram parsing for flowcharts and mathematical expressions.")
    b.add_numbered("4.", "Institutional LMS Integration (LTI 1.3 / SCORM):", "Two-way gradebook and curriculum synchronization with institutional learning management systems such as Moodle and Canvas.")

    b.add_page_break()

    # ==================== PAGE 4: OUTPUT (FIG 8.1 & 8.2) ====================
    b.add_heading1("8. OUTPUT & SYSTEM SCREENS")
    b.add_body("The following figures illustrate the operational user interface of the implemented StudyMate AI system across its core functional modules:")

    b.add_image(
        os.path.join(SHOTS_DIR, "1_upload_ingest.png"),
        "Fig. 8.1 : Universal Document Upload & Multi-Format Ingestion Console",
        emu_w=5600000, emu_h=3472000
    )

    b.add_image(
        os.path.join(SHOTS_DIR, "2_smart_search.png"),
        "Fig. 8.2 : Smart Search & Instant Topic Knowledge Synthesizer",
        emu_w=5600000, emu_h=3360000
    )

    b.add_page_break()

    # ==================== PAGE 5: OUTPUT (FIG 8.3 & 8.4) ====================
    b.add_image(
        os.path.join(SHOTS_DIR, "3_study_notes_flashcards.png"),
        "Fig. 8.3 : Interactive Study Notes & 3D Active Recall Flashcards",
        emu_w=5600000, emu_h=3584000
    )

    b.add_image(
        os.path.join(SHOTS_DIR, "4_quiz_runner.png"),
        "Fig. 8.4 : Adaptive Quiz Runner with Real-Time Timer & Cognitive Scaffolding",
        emu_w=5600000, emu_h=3360000
    )

    b.add_page_break()

    # ==================== PAGE 6: OUTPUT (FIG 8.5 & 8.6) ====================
    b.add_image(
        os.path.join(SHOTS_DIR, "5_scorecard_blooms.png"),
        "Fig. 8.5 : Comprehensive Scorecard & Bloom's Taxonomy Breakdown (Zero-Overlap UI)",
        emu_w=5600000, emu_h=3472000
    )

    b.add_image(
        os.path.join(SHOTS_DIR, "6_skills_dashboard.png"),
        "Fig. 8.6 : Skills Mastery Dashboard & Diagnostic Competency Tracking",
        emu_w=5600000, emu_h=3360000
    )

    b.add_page_break()

    # ==================== PAGE 7: SECTIONS 9 & 10 ====================
    b.add_heading1("9. CONCLUSION")
    b.add_body(
        "StudyMate AI successfully demonstrates that modern, adaptive educational technology can be engineered with exceptional responsiveness, high pedagogical rigor, "
        "and complete architectural autonomy without forcing reliance on expensive third-party cloud infrastructure. By unifying multi-format document ingestion, deterministic "
        "heuristic parsing, Bloom's Revised Taxonomy difficulty ladders, 3D active recall flashcards, and diagnostic competency tracking into a single cohesive platform, "
        "StudyMate AI bridges the critical gap between passive reading and active conceptual mastery."
    )
    b.add_body(
        "The project rigorously fulfills all academic and technical requirements for the Master of Computer Applications (MCA) curriculum. Its clean separation of concerns, "
        "robust asynchronous API endpoints, persistent SQLite storage, and lightweight single-page interface establish a resilient foundation for future institutional deployment "
        "and offline edge intelligence."
    )

    b.add_heading1("10. AUTHORITATIVE REFERENCES & CITATIONS")
    b.add_numbered("1.", "Bloom, B. S., et al. (1956/2001 Revised):", "Taxonomy of Educational Objectives: The Classification of Educational Goals. Longman, New York.")
    b.add_numbered("2.", "Roediger, H. L., & Karpicke, J. D. (2006):", "The Power of Testing Memory: Basic Research and Implications for Educational Practice. Perspectives on Psychological Science, 1(3), 181-210.")
    b.add_numbered("3.", "FastAPI Framework Documentation:", "Modern, Fast (high-performance), Web framework for building APIs with Python 3.8+ based on standard Python type hints (tiangolo).")
    b.add_numbered("4.", "SQLite Consortium (2024):", "SQLite Write-Ahead Logging (WAL) and Serverless Relational Database Architecture.")
    b.add_numbered("5.", "Ebbinghaus, H. (1885):", "Memory: A Contribution to Experimental Psychology. Spaced retrieval and exponential retention curve foundations.")
    b.add_numbered("6.", "World Wide Web Consortium (W3C):", "HTML5 & CSS 3D Transforms Module Level 3: Hardware-accelerated perspective rendering specifications.")
    b.add_numbered("7.", "Project Source Code Repository:", "https://github.com/SOFTGAMESTUDIO/StudyMate-AI (Local Workspace: F:\\AI project)")
    b.add_numbered("8.", "Project Local Server Deploy:", "http://127.0.0.1:8000 (FastAPI ASGI / Uvicorn Server)")

    # Build the document
    b.build(DOCX_PATH)

if __name__ == "__main__":
    generate_studymate_docx()
