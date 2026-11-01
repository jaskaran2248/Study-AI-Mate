"""
StudyMate AI - Text Extractor & Ingestion Pipeline
Extracts clean, structured text from PDF, DOCX, TXT, MD, CSV, JSON, and source files.
Runs locally without requiring heavyweight binary dependencies.
"""
import re
import os
import zipfile
import json
import xml.etree.ElementTree as ET
from typing import Tuple, Dict, Any, List

def extract_text_from_file(file_path: str, filename: str) -> Tuple[str, str]:
    """
    Extracts text from given file.
    Returns: (extracted_text, file_type)
    """
    ext = os.path.splitext(filename)[1].lower()
    
    if ext in ['.txt', '.md', '.markdown', '.rst', '.csv', '.py', '.js', '.ts', '.html', '.css', '.java', '.c', '.cpp', '.sql']:
        return extract_plain_text(file_path), ext[1:]
    
    elif ext == '.json':
        return extract_json_text(file_path), 'json'
    
    elif ext == '.docx':
        return extract_docx_text(file_path), 'docx'
        
    elif ext == '.pdf':
        return extract_pdf_text(file_path), 'pdf'
        
    else:
        try:
            return extract_plain_text(file_path), ext[1:] if ext else 'unknown'
        except Exception:
            raise ValueError(f"Unsupported file format: {ext}")

def extract_plain_text(file_path: str) -> str:
    """Reads standard text files with fallback encodings."""
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(file_path, 'r', encoding=enc) as f:
                return f.read().strip()
        except UnicodeDecodeError:
            continue
    with open(file_path, 'rb') as f:
        return f.read().decode('utf-8', errors='ignore').strip()

def extract_json_text(file_path: str) -> str:
    """Extracts text and formatted strings from JSON data."""
    raw = extract_plain_text(file_path)
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            lines = []
            for k, v in data.items():
                lines.append(f"{k}: {v}")
            return "\n".join(lines)
        elif isinstance(data, list):
            return "\n".join(str(item) for item in data)
        return str(data)
    except Exception:
        return raw

def extract_docx_text(file_path: str) -> str:
    """
    Extracts text from DOCX files by reading word/document.xml from the zip archive.
    Does not require external python-docx library.
    """
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            paragraphs = []
            for p in tree.iterfind('.//w:p', namespaces):
                texts = [node.text for node in p.iterfind('.//w:t', namespaces) if node.text]
                if texts:
                    paragraphs.append(''.join(texts))
            
            text = '\n\n'.join(paragraphs).strip()
            if text:
                return text
    except Exception as e:
        print(f"DOCX extraction notice: {e}")
    
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
        extracted = re.findall(rb'<w:t[^>]*>(.*?)</w:t>', content)
        return '\n'.join(x.decode('utf-8', errors='ignore') for x in extracted).strip()
    except Exception:
        return "Unable to parse DOCX contents."

def extract_pdf_text(file_path: str) -> str:
    """
    Pure Python PDF stream parser.
    Extracts text strings from text-based PDF streams and BT...ET blocks.
    """
    try:
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            pages = [page.extract_text() for page in reader.pages if page.extract_text()]
            if pages:
                return "\n\n".join(pages).strip()
        except ImportError:
            pass

        with open(file_path, 'rb') as f:
            pdf_data = f.read()

        import zlib
        text_chunks = []
        
        stream_matches = re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', pdf_data, re.DOTALL)
        for match in stream_matches:
            raw_stream = match.group(1)
            try:
                decompressed = zlib.decompress(raw_stream)
                tjs = re.findall(rb'\((.*?)\)\s*T[jJ]', decompressed)
                if tjs:
                    chunk = " ".join([t.decode('latin1', errors='ignore') for t in tjs])
                    if len(chunk.strip()) > 10:
                        text_chunks.append(chunk.strip())
                
                array_tjs = re.findall(rb'\[(.*?)\]\s*TJ', decompressed)
                for atj in array_tjs:
                    parts = re.findall(rb'\((.*?)\)', atj)
                    chunk = "".join([p.decode('latin1', errors='ignore') for p in parts])
                    if len(chunk.strip()) > 5:
                        text_chunks.append(chunk.strip())
            except Exception:
                continue

        uncompressed_tjs = re.findall(rb'\(([^()]{4,})\)\s*T[jJ]', pdf_data)
        for utj in uncompressed_tjs:
            try:
                dec = utj.decode('utf-8', errors='ignore')
                if len(dec.strip()) > 5:
                    text_chunks.append(dec.strip())
            except Exception:
                pass

        if text_chunks:
            combined = "\n\n".join(text_chunks)
            clean_text = re.sub(r'[ \t]+', ' ', combined)
            return clean_text.strip()
            
    except Exception as e:
        print(f"PDF native extraction warning: {e}")

    return "PDF uploaded. (For complex scanned images, text-based PDF or pasting syllabus is recommended)."

def compute_document_metadata(text: str) -> Dict[str, Any]:
    """
    Computes word count, reading time, extracted key terms, and suggested category focus.
    """
    words = re.findall(r'\b[A-Za-z0-9_-]+\b', text)
    word_count = len(words)
    reading_time = round(max(0.5, word_count / 200.0), 1) if word_count > 0 else 0.0
    
    text_lower = text.lower()
    
    focus_domain = "General Curriculum"
    if any(k in text_lower for k in ['climate', 'environment', 'sustainability', 'green', 'carbon', 'ecology', 'renewable', 'energy']):
        focus_domain = "Environmental & Natural Science"
    elif any(k in text_lower for k in ['algorithm', 'code', 'python', 'software', 'ai', 'data', 'computer', 'engineering', 'tree']):
        focus_domain = "Computer Science & Engineering"
    elif any(k in text_lower for k in ['calculus', 'probability', 'statistics', 'derivative', 'gradient', 'math']):
        focus_domain = "Mathematics & Quantitative Methods"
    elif any(k in text_lower for k in ['ethics', 'governance', 'policy', 'privacy', 'transparency']):
        focus_domain = "Ethics, Governance & Systems"
    
    stopwords = {
        'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'for', 'on', 'with', 'as', 'by',
        'at', 'from', 'this', 'an', 'be', 'are', 'was', 'were', 'it', 'not', 'or', 'which',
        'has', 'have', 'can', 'will', 'all', 'into', 'their', 'more', 'about', 'also', 'such'
    }
    
    word_freq: Dict[str, int] = {}
    for w in words:
        wl = w.lower()
        if len(wl) > 3 and wl not in stopwords and not wl.isnumeric():
            word_freq[wl] = word_freq.get(wl, 0) + 1
            
    sorted_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    top_tags = [kw.capitalize() for kw, count in sorted_keywords[:6]]
    
    return {
        "word_count": word_count,
        "reading_time_min": reading_time,
        "sdg_target": focus_domain,
        "tags": ", ".join(top_tags) if top_tags else "Study, Concepts, Skills"
    }
