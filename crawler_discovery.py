import os
import sys
import re
import json
import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def discover_all_urls():
    session = requests.Session()
    session.headers.update(HEADERS)
    
    visited_pages = set()
    to_visit_pages = set()
    found_pdfs = {}
    found_pages = {}
    
    # 1. Main sitemap
    try:
        r = session.get('https://www.anytime.gr/anytime-sitemap.xml', timeout=10)
        root = ET.fromstring(r.content)
        for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            url = elem.text.strip()
            to_visit_pages.add(url)
        print(f"Loaded {len(to_visit_pages)} URLs from anytime-sitemap.xml")
    except Exception as e:
        print(f"Error loading anytime-sitemap: {e}")
        to_visit_pages.add('https://www.anytime.gr/')

    # 2. Blog sitemaps
    blog_sitemaps = [
        'https://blog.anytime.gr/post-sitemap.xml',
        'https://blog.anytime.gr/page-sitemap.xml',
        'https://blog.anytime.gr/category-sitemap.xml'
    ]
    for b_sitemap in blog_sitemaps:
        try:
            r = session.get(b_sitemap, timeout=10)
            root = ET.fromstring(r.content)
            count = 0
            for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                url = elem.text.strip()
                to_visit_pages.add(url)
                count += 1
            print(f"Loaded {count} URLs from {b_sitemap}")
        except Exception as e:
            print(f"Error loading blog sitemap {b_sitemap}: {e}")

    # Helper function to crawl one page
    def process_url(url):
        new_urls = set()
        pdfs = []
        page_info = None
        try:
            resp = session.get(url, timeout=12)
            if resp.status_code != 200:
                return new_urls, pdfs, page_info
            
            content_type = resp.headers.get('Content-Type', '')
            if 'application/pdf' in content_type:
                pdfs.append((url, 'Direct PDF URL', url))
                return new_urls, pdfs, page_info
            
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.title.get_text(strip=True) if soup.title else ''
            
            page_info = {
                'url': url,
                'title': title,
                'status': resp.status_code,
                'html': resp.text
            }
            
            # Find links
            for tag in soup.find_all(['a', 'link', 'iframe', 'embed', 'source']):
                link = tag.get('href') or tag.get('src')
                if not link:
                    continue
                full_link = urljoin(url, link).split('#')[0].strip()
                if not full_link.startswith('http'):
                    continue
                
                parsed = urlparse(full_link)
                anchor_text = tag.get_text(strip=True)
                
                # Check for PDF or document
                if '.pdf' in full_link.lower() or 'kc-usercontent' in full_link.lower() and ('pdf' in full_link.lower() or 'eggrafo' in full_link.lower() or 'oroi' in full_link.lower()):
                    pdfs.append((full_link, anchor_text, url))
                elif any(d in parsed.netloc for d in ['anytime.gr', 'blog.anytime.gr']):
                    # Check file extensions to ignore
                    if not any(full_link.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.svg', '.gif', '.css', '.js', '.woff', '.woff2', '.mp4', '.webp', '.ico']):
                        new_urls.add(full_link)
                        
            # Regex scan for .pdf urls in script/data attributes
            for m in re.findall(r'https?://[^\"\'\s<>]+\.pdf[^\s\"\'<>]*', resp.text, re.IGNORECASE):
                pdfs.append((m, 'Regex In Page', url))
                
        except Exception as e:
            pass
        return new_urls, pdfs, page_info

    # Breadth-first parallel crawl
    print(f"\nStarting crawler with {len(to_visit_pages)} initial targets...")
    batch_size = 20
    round_num = 1
    
    while to_visit_pages:
        batch = list(to_visit_pages)[:batch_size]
        for u in batch:
            to_visit_pages.remove(u)
            visited_pages.add(u)
            
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(process_url, batch))
            
        for new_urls, pdfs, page_info in results:
            if page_info:
                found_pages[page_info['url']] = page_info
            for pdf_url, anchor, src_url in pdfs:
                if pdf_url not in found_pdfs:
                    found_pdfs[pdf_url] = {
                        'url': pdf_url,
                        'anchor': anchor,
                        'found_in': src_url
                    }
            for u in new_urls:
                if u not in visited_pages and u not in to_visit_pages:
                    # Don't wander off into excessive external loops
                    to_visit_pages.add(u)
                    
        print(f"Round {round_num}: Visited: {len(visited_pages)}, Queue: {len(to_visit_pages)}, Pages captured: {len(found_pages)}, PDFs discovered: {len(found_pdfs)}")
        round_num += 1
        
        # Safety break if queue grows too large
        if len(visited_pages) >= 500:
            print("Reached crawl limit of 500 pages.")
            break

    print("\n" + "="*60)
    print(f"CRAWL COMPLETE: {len(found_pages)} pages captured, {len(found_pdfs)} PDFs found.")
    print("="*60)
    
    print("\n--- Discovered PDFs ---")
    for p_url, p_meta in found_pdfs.items():
        print(f"[PDF] {p_url} | Anchor: {p_meta['anchor'][:50]} | From: {p_meta['found_in']}")

    return found_pages, found_pdfs

if __name__ == '__main__':
    pages, pdfs = discover_all_urls()
    os.makedirs('crawl_cache', exist_ok=True)
    with open('crawl_cache/discovered_pdfs.json', 'w', encoding='utf-8') as f:
        json.dump(pdfs, f, ensure_ascii=False, indent=2)
    with open('crawl_cache/discovered_pages.json', 'w', encoding='utf-8') as f:
        json.dump({k: {'url': v['url'], 'title': v['title']} for k, v in pages.items()}, f, ensure_ascii=False, indent=2)
    print("\nSaved discovery cache to crawl_cache/")
