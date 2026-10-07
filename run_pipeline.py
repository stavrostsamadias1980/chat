import os
import sys
import json
import re
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import fitz

from build_rag_dataset import (
    BASE_DIR, RAW_PDF_DIR, EXTRACTED_PDF_DIR, EXTRACTED_WEB_DIR,
    RAG_CHUNKS_DIR, CATEGORY_CHUNKS_DIR, HEADERS,
    classify_document, clean_filename, download_file,
    extract_pdf_content, clean_html_content, chunk_text
)

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("="*70)
    print("🚀 STARTING ANYTIME.GR RAG DATASET INGESTION & PIPELINE BUILDER")
    print("="*70)

    # 1. Ensure output directories exist
    RAW_PDF_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACTED_PDF_DIR.mkdir(parents=True, exist_ok=True)
    EXTRACTED_WEB_DIR.mkdir(parents=True, exist_ok=True)
    RAG_CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORY_CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

    # 2. Load discovered PDFs and pages from cache or discovery
    pdf_cache_file = Path("crawl_cache/discovered_pdfs.json")
    page_cache_file = Path("crawl_cache/discovered_pages.json")

    if not pdf_cache_file.exists() or not page_cache_file.exists():
        print("Discovery cache not found. Please run crawler_discovery.py first.")
        return

    with open(pdf_cache_file, "r", encoding="utf-8") as f:
        discovered_pdfs = json.load(f)

    with open(page_cache_file, "r", encoding="utf-8") as f:
        discovered_pages = json.load(f)

    print(f"📊 Discovered Items: {len(discovered_pdfs)} PDF URLs, {len(discovered_pages)} Web Pages")

    # =========================================================================
    # STEP 1: DOWNLOAD & ORGANIZE ALL PDFs
    # =========================================================================
    print("\n" + "="*50)
    print("📥 STEP 1: DOWNLOADING & ORGANIZING ALL PDFs")
    print("="*50)

    pdf_metadata_list = []
    
    def process_pdf_item(item):
        url, meta = item
        clean_name = clean_filename(url)
        anchor = meta.get('anchor', '')
        found_in = meta.get('found_in', '')
        
        category, subcategory, doc_type = classify_document(url, anchor, found_in)
        
        cat_pdf_dir = RAW_PDF_DIR / category
        cat_pdf_dir.mkdir(parents=True, exist_ok=True)
        pdf_path = cat_pdf_dir / clean_name
        
        success = download_file(url, pdf_path)
        if success:
            file_size = pdf_path.stat().st_size
            return {
                "id": f"pdf_{category}_{clean_name}",
                "filename": clean_name,
                "local_path": str(pdf_path.relative_to(BASE_DIR)).replace('\\', '/'),
                "absolute_path": str(pdf_path),
                "url": url,
                "category": category,
                "subcategory": subcategory,
                "doc_type": doc_type,
                "anchor_text": anchor,
                "source_page": found_in,
                "file_size_bytes": file_size
            }
        return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_pdf_item, item) for item in discovered_pdfs.items()]
        for f in as_completed(futures):
            res = f.result()
            if res:
                pdf_metadata_list.append(res)
                print(f"  [OK] [{res['category']:<25}] {res['filename']} ({res['file_size_bytes']//1024} KB)")

    print(f"\n✅ Successfully downloaded and categorized {len(pdf_metadata_list)} PDFs.")

    # =========================================================================
    # STEP 2: EXTRACT STRUCTURED TEXT FROM ALL PDFs
    # =========================================================================
    print("\n" + "="*50)
    print("📄 STEP 2: EXTRACTING TEXT FROM ALL PDFs")
    print("="*50)

    pdf_extracted_docs = []
    for pdf_meta in pdf_metadata_list:
        pdf_path = Path(pdf_meta["absolute_path"])
        extracted = extract_pdf_content(pdf_path)
        
        if not extracted["full_text"]:
            print(f"  [WARN] No text extracted from {pdf_path.name}")
            continue

        category = pdf_meta["category"]
        out_cat_dir = EXTRACTED_PDF_DIR / category
        out_cat_dir.mkdir(parents=True, exist_ok=True)
        
        stem = pdf_path.stem
        md_file = out_cat_dir / f"{stem}.md"
        json_file = out_cat_dir / f"{stem}.json"
        
        doc_record = {
            "id": pdf_meta["id"],
            "title": pdf_meta["anchor_text"] or stem.replace('_', ' ').title(),
            "category": category,
            "subcategory": pdf_meta["subcategory"],
            "doc_type": pdf_meta["doc_type"],
            "source_type": "pdf",
            "source_url": pdf_meta["url"],
            "relative_pdf_path": pdf_meta["local_path"],
            "pages_count": extracted["pages_count"],
            "character_count": len(extracted["full_text"]),
            "word_count": len(extracted["full_text"].split()),
            "content": extracted["full_text"],
            "pages": extracted["pages"]
        }
        
        # Save JSON
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(doc_record, f, ensure_ascii=False, indent=2)
            
        # Save Markdown with frontmatter
        md_content = f"""# {doc_record['title']}
**Category:** {doc_record['category']} | **Subcategory:** {doc_record['subcategory']} | **Type:** {doc_record['doc_type']}
**Source PDF:** [{pdf_meta['filename']}]({doc_record['source_url']})
**Pages:** {doc_record['pages_count']}

---

{doc_record['content']}
"""
        with open(md_file, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        pdf_extracted_docs.append(doc_record)
        print(f"  [TEXT] Extracted {extracted['pages_count']} pages ({len(extracted['full_text'].split())} words) from {pdf_path.name}")

    print(f"\n✅ Extracted text from {len(pdf_extracted_docs)} PDFs.")

    # =========================================================================
    # STEP 3: CRAWL, EXTRACT & STRUCTURE ALL WEB PAGES & FAQs
    # =========================================================================
    print("\n" + "="*50)
    print("🌐 STEP 3: FETCHING & STRUCTURING WEB PAGES & FAQs")
    print("="*50)

    web_extracted_docs = []
    faq_pairs_list = []
    
    session = requests.Session()
    session.headers.update(HEADERS)

    def process_web_page(page_url):
        try:
            resp = session.get(page_url, timeout=12)
            if resp.status_code != 200 or 'text/html' not in resp.headers.get('Content-Type', ''):
                return None
            
            resp.encoding = 'utf-8'
            cleaned = clean_html_content(resp.text, page_url)
            if not cleaned["cleaned_text"] or len(cleaned["cleaned_text"]) < 100:
                return None
            
            title = cleaned["title"]
            category, subcategory, doc_type = classify_document(page_url, title, cleaned["cleaned_text"][:500])
            
            # Safe filename slug
            parsed_path = urllib.parse.urlparse(page_url).path.strip('/')
            slug = re.sub(r'[^\w\-]', '_', parsed_path) or 'homepage'
            if 'blog.anytime.gr' in page_url:
                slug = 'blog_' + slug
                
            out_cat_dir = EXTRACTED_WEB_DIR / category
            out_cat_dir.mkdir(parents=True, exist_ok=True)
            
            md_file = out_cat_dir / f"{slug}.md"
            json_file = out_cat_dir / f"{slug}.json"
            
            doc_record = {
                "id": f"web_{category}_{slug}",
                "title": title or slug,
                "category": category,
                "subcategory": subcategory,
                "doc_type": doc_type,
                "source_type": "web_page",
                "source_url": page_url,
                "character_count": len(cleaned["cleaned_text"]),
                "word_count": len(cleaned["cleaned_text"].split()),
                "content": cleaned["cleaned_text"],
                "faqs": cleaned["faqs"]
            }
            
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(doc_record, f, ensure_ascii=False, indent=2)
                
            md_content = f"""# {doc_record['title']}
**Category:** {doc_record['category']} | **Subcategory:** {doc_record['subcategory']} | **Type:** {doc_record['doc_type']}
**Source URL:** {page_url}

---

{doc_record['content']}
"""
            with open(md_file, "w", encoding="utf-8") as f:
                f.write(md_content)
                
            # Collect FAQ pairs
            for idx, qa in enumerate(cleaned["faqs"]):
                faq_pairs_list.append({
                    "id": f"faq_{category}_{slug}_{idx+1}",
                    "category": category,
                    "subcategory": subcategory,
                    "question": qa["question"],
                    "answer": qa["answer"],
                    "source_url": page_url,
                    "source_title": title
                })
                
            return doc_record
        except Exception as e:
            return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_web_page, u) for u in discovered_pages.keys()]
        for f in as_completed(futures):
            res = f.result()
            if res:
                web_extracted_docs.append(res)
                print(f"  [WEB] [{res['category']:<25}] {res['title'][:50]} ({res['word_count']} words)")

    print(f"\n✅ Extracted and categorized {len(web_extracted_docs)} web pages & {len(faq_pairs_list)} FAQ pairs.")

    # =========================================================================
    # STEP 4: GENERATE RAG-READY CHUNKS & METADATA
    # =========================================================================
    print("\n" + "="*50)
    print("✂️ STEP 4: GENERATING RAG CHUNKS & EMBEDDING PAYLOADS")
    print("="*50)

    all_chunks = []
    chunks_by_category = {}
    
    all_docs = pdf_extracted_docs + web_extracted_docs
    
    chunk_counter = 0
    for doc in all_docs:
        chunks = chunk_text(doc["content"], chunk_size=800, overlap=120)
        category = doc["category"]
        
        if category not in chunks_by_category:
            chunks_by_category[category] = []
            
        for c_idx, chunk_text_content in enumerate(chunks):
            chunk_counter += 1
            chunk_obj = {
                "chunk_id": f"chk_{doc['id']}_{c_idx+1:03d}",
                "doc_id": doc["id"],
                "doc_title": doc["title"],
                "source_type": doc["source_type"],
                "source_url": doc["source_url"],
                "category": category,
                "subcategory": doc["subcategory"],
                "doc_type": doc["doc_type"],
                "chunk_index": c_idx + 1,
                "total_chunks_in_doc": len(chunks),
                "char_length": len(chunk_text_content),
                "token_estimate": len(chunk_text_content) // 4,
                "text": chunk_text_content
            }
            all_chunks.append(chunk_obj)
            chunks_by_category[category].append(chunk_obj)

    # Save Master chunks.jsonl
    master_chunks_path = RAG_CHUNKS_DIR / "chunks.jsonl"
    with open(master_chunks_path, "w", encoding="utf-8") as f:
        for chk in all_chunks:
            f.write(json.dumps(chk, ensure_ascii=False) + "\n")
    print(f"  [SAVED] Master RAG chunks: {master_chunks_path} ({len(all_chunks)} chunks)")

    # Save Category chunks.jsonl
    for cat, c_list in chunks_by_category.items():
        cat_file = CATEGORY_CHUNKS_DIR / f"{cat}_chunks.jsonl"
        with open(cat_file, "w", encoding="utf-8") as f:
            for chk in c_list:
                f.write(json.dumps(chk, ensure_ascii=False) + "\n")
        print(f"  [SAVED] Category chunk file: {cat_file.name} ({len(c_list)} chunks)")

    # Save FAQ QA pairs
    faq_qa_path = RAG_CHUNKS_DIR / "faq_qa_pairs.jsonl"
    with open(faq_qa_path, "w", encoding="utf-8") as f:
        for qa in faq_pairs_list:
            f.write(json.dumps(qa, ensure_ascii=False) + "\n")
    print(f"  [SAVED] Structured FAQ QA pairs: {faq_qa_path} ({len(faq_pairs_list)} Q&As)")

    # =========================================================================
    # STEP 5: BUILD MASTER CATALOG & MANIFEST
    # =========================================================================
    catalog = {
        "dataset_name": "Anytime.gr Insurance Knowledge Base for RAG",
        "description": "Complete scraped & extracted knowledge base of anytime.gr including policy terms, IPIDs, coverage guides, FAQ, forms, and web content categorized for RAG.",
        "statistics": {
            "total_documents": len(all_docs),
            "pdf_documents": len(pdf_extracted_docs),
            "web_documents": len(web_extracted_docs),
            "total_chunks": len(all_chunks),
            "total_faq_pairs": len(faq_pairs_list),
            "total_characters": sum(doc["character_count"] for doc in all_docs),
            "total_words": sum(doc["word_count"] for doc in all_docs),
            "categories_count": len(chunks_by_category)
        },
        "categories_breakdown": {
            cat: {
                "chunks_count": len(c_list),
                "docs_count": len(set(c["doc_id"] for c in c_list))
            } for cat, c_list in chunks_by_category.items()
        },
        "documents": [
            {
                "id": doc["id"],
                "title": doc["title"],
                "category": doc["category"],
                "subcategory": doc["subcategory"],
                "doc_type": doc["doc_type"],
                "source_type": doc["source_type"],
                "source_url": doc["source_url"],
                "character_count": doc["character_count"],
                "word_count": doc["word_count"]
            } for doc in all_docs
        ]
    }

    catalog_path = RAG_CHUNKS_DIR / "rag_catalog.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
    print(f"  [SAVED] Master Catalog: {catalog_path}")

    print("\n" + "="*70)
    print("🎉 RAG DATASET INGESTION COMPLETED SUCCESSFULLY!")
    print(f"📁 Root directory: {BASE_DIR}")
    print(f"📄 Total PDFs Processed: {len(pdf_extracted_docs)}")
    print(f"🌐 Total Web Pages Processed: {len(web_extracted_docs)}")
    print(f"🧩 Total RAG Chunks Generated: {len(all_chunks)}")
    print(f"❓ Total FAQ Q&A Pairs: {len(faq_pairs_list)}")
    print("="*70)

if __name__ == "__main__":
    main()
