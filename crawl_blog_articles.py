import os
import sys
import json
import re
import urllib.parse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

from build_rag_dataset import (
    BASE_DIR, EXTRACTED_WEB_DIR, RAG_CHUNKS_DIR, CATEGORY_CHUNKS_DIR, HEADERS,
    clean_html_content, chunk_text
)

sys.stdout.reconfigure(encoding='utf-8')

def ingest_blog_articles():
    print("="*60)
    print("📰 INGESTING ALL ANYTIME.GR BLOG & EDUCATIONAL ARTICLES")
    print("="*60)
    
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    # 1. Fetch post sitemap
    sitemap_url = "https://blog.anytime.gr/post-sitemap.xml"
    try:
        r = session.get(sitemap_url, timeout=15)
        post_urls = [u.strip() for u in re.findall(r'<loc>(.*?)</loc>', r.text, re.DOTALL) if 'blog.anytime.gr' in u]
        print(f"Discovered {len(post_urls)} blog articles from sitemap.")
    except Exception as e:
        print(f"Error fetching blog sitemap: {e}")
        return

    blog_out_dir = EXTRACTED_WEB_DIR / "blog_educational_guides"
    blog_out_dir.mkdir(parents=True, exist_ok=True)
    
    def process_article(url):
        try:
            resp = session.get(url, timeout=12)
            if resp.status_code != 200:
                return None
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Extract title
            title = soup.title.get_text(strip=True) if soup.title else url
            title = re.sub(r'\s*[-|]\s*Anytime\s*Blog.*', '', title, flags=re.I)
            
            # Main article element
            article = soup.find('article') or soup.find(class_=re.compile(r'entry-content|post-content|content', re.I))
            if not article:
                article = soup.body
                
            for s in article(['script', 'style', 'noscript', 'nav', 'header', 'footer', 'aside']):
                s.decompose()
                
            paragraphs = []
            for elem in article.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'p', 'li']):
                txt = elem.get_text(strip=True)
                if len(txt) > 3:
                    if elem.name.startswith('h'):
                        paragraphs.append(f"\n### {txt}\n")
                    elif elem.name == 'li':
                        paragraphs.append(f"- {txt}")
                    else:
                        paragraphs.append(txt)
                        
            cleaned_text = "\n\n".join(paragraphs).strip()
            if len(cleaned_text) < 150:
                return None
                
            slug = url.strip('/').split('/')[-1]
            slug = re.sub(r'[^\w\-]', '_', slug)
            
            doc_record = {
                "id": f"blog_{slug}",
                "title": title,
                "category": "blog_educational_guides",
                "subcategory": "insurance_guides",
                "doc_type": "educational_article",
                "source_type": "blog_post",
                "source_url": url,
                "character_count": len(cleaned_text),
                "word_count": len(cleaned_text.split()),
                "content": cleaned_text
            }
            
            # Save md & json
            md_file = blog_out_dir / f"{slug}.md"
            json_file = blog_out_dir / f"{slug}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(doc_record, f, ensure_ascii=False, indent=2)
                
            md_content = f"""# {doc_record['title']}
**Category:** blog_educational_guides | **Type:** educational_article
**Source URL:** {url}

---

{doc_record['content']}
"""
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
                
            return doc_record
        except Exception as e:
            return None

    articles_data = []
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = [executor.submit(process_article, u) for u in post_urls]
        for f in as_completed(futures):
            res = f.result()
            if res:
                articles_data.append(res)
                if len(articles_data) % 25 == 0:
                    print(f"  Processed {len(articles_data)} / {len(post_urls)} articles...")

    print(f"\n✅ Successfully extracted {len(articles_data)} educational articles.")
    
    # Generate chunks for blog articles
    blog_chunks = []
    for doc in articles_data:
        chunks = chunk_text(doc["content"], chunk_size=750, overlap=100)
        for c_idx, c_text in enumerate(chunks):
            blog_chunks.append({
                "chunk_id": f"chk_{doc['id']}_{c_idx+1:03d}",
                "doc_id": doc["id"],
                "doc_title": doc["title"],
                "source_type": doc["source_type"],
                "source_url": doc["source_url"],
                "category": doc["category"],
                "subcategory": doc["subcategory"],
                "doc_type": doc["doc_type"],
                "chunk_index": c_idx + 1,
                "total_chunks_in_doc": len(chunks),
                "char_length": len(c_text),
                "token_estimate": len(c_text) // 4,
                "text": c_text
            })

    # Save category chunk file
    blog_cat_file = CATEGORY_CHUNKS_DIR / "blog_educational_guides_chunks.jsonl"
    with open(blog_cat_file, 'w', encoding='utf-8') as f:
        for chk in blog_chunks:
            f.write(json.dumps(chk, ensure_ascii=False) + "\n")
            
    print(f"  [SAVED] Blog chunks: {blog_cat_file.name} ({len(blog_chunks)} chunks)")

    # Append to master chunks.jsonl
    master_chunks_path = RAG_CHUNKS_DIR / "chunks.jsonl"
    with open(master_chunks_path, 'a', encoding='utf-8') as f:
        for chk in blog_chunks:
            f.write(json.dumps(chk, ensure_ascii=False) + "\n")
            
    print(f"  [UPDATED] Appended to Master RAG chunks: {master_chunks_path}")

    # Update Catalog
    catalog_path = RAG_CHUNKS_DIR / "rag_catalog.json"
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)
        
    catalog["statistics"]["total_documents"] += len(articles_data)
    catalog["statistics"]["blog_documents"] = len(articles_data)
    catalog["statistics"]["total_chunks"] += len(blog_chunks)
    catalog["statistics"]["total_characters"] += sum(d["character_count"] for d in articles_data)
    catalog["statistics"]["total_words"] += sum(d["word_count"] for d in articles_data)
    catalog["statistics"]["categories_count"] += 1
    
    catalog["categories_breakdown"]["blog_educational_guides"] = {
        "chunks_count": len(blog_chunks),
        "docs_count": len(articles_data)
    }
    
    for d in articles_data:
        catalog["documents"].append({
            "id": d["id"],
            "title": d["title"],
            "category": d["category"],
            "subcategory": d["subcategory"],
            "doc_type": d["doc_type"],
            "source_type": d["source_type"],
            "source_url": d["source_url"],
            "character_count": d["character_count"],
            "word_count": d["word_count"]
        })
        
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)
        
    print(f"  [UPDATED] Master Catalog: {catalog_path}")
    print("\n🎉 ALL BLOG ARTICLES SUCCESSFULLY PROCESSED AND INTEGRATED!")

if __name__ == '__main__':
    ingest_blog_articles()
