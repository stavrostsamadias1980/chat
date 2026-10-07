"""
Anytime.gr End-to-End Crawler, Downloader, Text Extractor & RAG Dataset Builder
"""

import os
import sys
import re
import json
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF

sys.stdout.reconfigure(encoding='utf-8')

# Base directories
BASE_DIR = Path("g:/WIDGET-UI/anytime_rag_dataset")
RAW_PDF_DIR = BASE_DIR / "raw_pdfs"
EXTRACTED_PDF_DIR = BASE_DIR / "extracted_text" / "pdf_text"
EXTRACTED_WEB_DIR = BASE_DIR / "extracted_text" / "web_pages"
RAG_CHUNKS_DIR = BASE_DIR / "rag_ready_chunks"
CATEGORY_CHUNKS_DIR = RAG_CHUNKS_DIR / "by_category"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Category classification mapping rules based on URL, filename, or anchor
def classify_document(url: str, title: str = "", context: str = "") -> tuple[str, str, str]:
    """
    Returns (category, subcategory, doc_type)
    Categories:
      - car_insurance (Auto / Standard / Short / Smart / Mikti)
      - moto_insurance (Motorbike)
      - truck_trailer_insurance (Truck / Agricultural / Trailer)
      - home_property_insurance (Home / ENFIA / Airbnb / Loss of rent / Content)
      - health_insurance (Health / Child / Accident / Hospitals)
      - travel_insurance (Travel)
      - cyber_insurance (Cyber Security)
      - micro_mobility_ebikes (E-Bikes / E-Scooters)
      - business_insurance (Business)
      - roadside_assistance_claims (Accident care / Road assistance / Claims)
      - offers_partnerships (Discounts / Tolls / Partners)
      - legal_compliance_gdpr (GDPR / Terms of use / Deontology / Cancellation)
      - faq_general (General info & FAQs)
      - blog_educational_guides (Blog articles & guides)
    """
    combined = f"{url.lower()} {title.lower()} {context.lower()}"
    
    # Doc type detection
    doc_type = "general_info"
    if "ipid" in combined or "eggrafo_plirofori" in combined or "eggrafo-pliroforion" in combined:
        doc_type = "ipid_information_document"
    elif "oroi" in combined or "terms" in combined or "vivlio-oron" in combined:
        doc_type = "policy_terms_and_conditions"
    elif "enimerotiko" in combined:
        doc_type = "precontractual_information"
    elif "apozimiw" in combined or "apozimiosi" in combined or "anaggelia" in combined or "filikos" in combined:
        doc_type = "claims_and_compensation_guide"
    elif "enantiws" in combined or "upanaxwrisi" in combined or "dilosi" in combined:
        doc_type = "legal_declaration_cancellation"
    elif "nosokomei" in combined or "diagnostik" in combined or "iatrika" in combined:
        doc_type = "medical_network_directory"
    elif "faq" in combined or "erotiseis" in combined or "faqs" in combined:
        doc_type = "frequently_asked_questions"
    elif "offer" in combined or "ekptws" in combined:
        doc_type = "offer_discount_terms"
    elif "kodikas" in combined or "deontolog" in combined or "gdpr" in combined or "dedomen" in combined:
        doc_type = "legal_compliance_gdpr"

    # Category classification
    if any(k in combined for k in ["motor", "auto", "car", "smartdrive", "shortdrive", "mikti", "oxhma", "autokinit"]):
        return "car_insurance", "motor_auto", doc_type
    elif any(k in combined for k in ["moto", "motorbike", "dikykl", "mixan"]):
        return "moto_insurance", "motorcycle", doc_type
    elif any(k in combined for k in ["truck", "agro", "trailer", "fortig", "rymoulk"]):
        return "truck_trailer_insurance", "commercial_vehicles", doc_type
    elif any(k in combined for k in ["home", "katoik", "property", "enfia", "braxyxron", "rent", "spiti", "kotsovolos", "prosperty"]):
        return "home_property_insurance", "property_home", doc_type
    elif any(k in combined for k in ["health", "ygeia", "child", "accident_care", "nosokom", "diagnost", "iatrik", "ifriend"]):
        return "health_insurance", "health_care", doc_type
    elif any(k in combined for k in ["travel", "taxid"]):
        return "travel_insurance", "travel", doc_type
    elif any(k in combined for k in ["cyber", "personal-cyber"]):
        return "cyber_insurance", "cyber_risk", doc_type
    elif any(k in combined for k in ["ebike", "e-bike", "escooter", "patini", "urban_mobility"]):
        return "micro_mobility_ebikes", "e_mobility", doc_type
    elif any(k in combined for k in ["business", "epixeir"]):
        return "business_insurance", "commercial_business", doc_type
    elif any(k in combined for k in ["odiki", "carpoint", "driveon", "batarias", "apozimioseis"]):
        return "roadside_assistance_claims", "claims_services", doc_type
    elif any(k in combined for k in ["offer", "ekptwseis", "attiki-odos", "nea-odos", "kentriki-odos", "aigaiou", "seasmiles", "pomida", "polispark", "wallet"]):
        return "offers_partnerships", "discounts_benefits", doc_type
    elif any(k in combined for k in ["blog.anytime.gr", "blog/"]):
        return "blog_educational_guides", "insurance_guides", "educational_article"
    elif any(k in combined for k in ["privacy", "terms-of-use", "deontologias", "prostasias_dedomenon", "nomikis"]):
        return "legal_compliance_gdpr", "legal_terms", doc_type
    elif "faq" in combined:
        return "faq_general", "general_faq", doc_type
    else:
        return "general_info", "general", doc_type

def clean_filename(url: str) -> str:
    raw_name = url.split('/')[-1].split('?')[0]
    decoded = urllib.parse.unquote(raw_name)
    # Remove special query/param noise
    cleaned = re.sub(r'[\+\s]+', '_', decoded)
    cleaned = re.sub(r'[^\w\.\-\(\)]', '_', cleaned)
    if not cleaned.lower().endswith('.pdf'):
        cleaned += '.pdf'
    return cleaned

def download_file(url: str, target_path: Path) -> bool:
    try:
        if target_path.exists() and target_path.stat().st_size > 500:
            return True
        target_path.parent.mkdir(parents=True, exist_ok=True)
        resp = requests.get(url, headers=HEADERS, timeout=20)
        if resp.status_code == 200 and len(resp.content) > 200:
            with open(target_path, 'wb') as f:
                f.write(resp.content)
            return True
        else:
            print(f"Failed download {url}: HTTP {resp.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def extract_pdf_content(pdf_path: Path) -> dict:
    """Extracts structured text per page from PDF using PyMuPDF."""
    pages_text = []
    total_text = ""
    try:
        doc = fitz.open(str(pdf_path))
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text("text").strip()
            if text:
                pages_text.append({
                    "page_number": page_num + 1,
                    "text": text
                })
                total_text += f"\n\n--- Page {page_num + 1} ---\n" + text
        doc.close()
    except Exception as e:
        print(f"Error reading PDF {pdf_path.name}: {e}")
    
    return {
        "pages_count": len(pages_text),
        "pages": pages_text,
        "full_text": total_text.strip()
    }

def clean_html_content(html: str, url: str) -> dict:
    """Extracts structured text, headings, FAQ items, and sections from HTML."""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove scripts, styles, navbars, footers for clean content
    for s in soup(['script', 'style', 'noscript', 'header', 'footer', 'nav', 'svg', 'iframe']):
        s.decompose()
        
    title = soup.title.get_text(strip=True) if soup.title else ""
    
    # Check for FAQ accordions or structured QA
    faqs = []
    for item in soup.find_all(class_=re.compile(r'accordion|faq|collapse|question|answer', re.I)):
        q = item.find(['h2', 'h3', 'h4', 'h5', 'strong', 'summary', 'button'])
        if q:
            q_text = q.get_text(strip=True)
            # Find sibling or body text
            ans_text = item.get_text(strip=True).replace(q_text, '').strip()
            if len(q_text) > 5 and len(ans_text) > 10:
                faqs.append({"question": q_text, "answer": ans_text})
                
    # Extract main content text
    main_el = soup.find(['main', 'article', 'div#main', 'div#content', 'div.container']) or soup.body
    if main_el:
        paragraphs = []
        for elem in main_el.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'table']):
            txt = elem.get_text(strip=True)
            if txt and len(txt) > 3:
                tag = elem.name
                if tag.startswith('h'):
                    level = tag[1]
                    paragraphs.append(f"\n{'#' * int(level)} {txt}\n")
                elif tag == 'li':
                    paragraphs.append(f"- {txt}")
                else:
                    paragraphs.append(txt)
        cleaned_text = "\n\n".join(paragraphs)
    else:
        cleaned_text = soup.get_text(separator="\n", strip=True)
        
    return {
        "title": title,
        "url": url,
        "cleaned_text": cleaned_text,
        "faqs": faqs
    }

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 150) -> list[str]:
    """Semantic paragraph & sliding window chunking."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = []
    current_length = 0
    
    for p in paragraphs:
        p_str = p.strip()
        if not p_str:
            continue
        p_len = len(p_str)
        if current_length + p_len > chunk_size and current_chunk:
            combined = "\n\n".join(current_chunk)
            chunks.append(combined)
            # Retain overlap from end of previous chunk if available
            if overlap > 0 and len(current_chunk) > 1:
                current_chunk = [current_chunk[-1], p_str]
                current_length = len(current_chunk[0]) + p_len
            else:
                current_chunk = [p_str]
                current_length = p_len
        else:
            current_chunk.append(p_str)
            current_length += p_len
            
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))
        
    return chunks

print("Loaded builder module definitions.")
