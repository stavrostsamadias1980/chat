"""
RAG Dataset Inspector, Query Tester & Embedding Loader for Anytime.gr
"""

import os
import sys
import json
import math
import re
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

DATASET_DIR = Path("g:/WIDGET-UI/anytime_rag_dataset")
CHUNKS_FILE = DATASET_DIR / "rag_ready_chunks" / "chunks.jsonl"
FAQ_FILE = DATASET_DIR / "rag_ready_chunks" / "faq_qa_pairs.jsonl"
CATALOG_FILE = DATASET_DIR / "rag_ready_chunks" / "rag_catalog.json"

def load_chunks():
    chunks = []
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                chunks.append(json.loads(line))
    return chunks

def load_faqs():
    faqs = []
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                faqs.append(json.loads(line))
    return faqs

# Simple BM25 / Keyword ranker for testing queries
def tokenize(text: str) -> list[str]:
    return [w.lower() for w in re.findall(r'\b\w+\b', text) if len(w) > 1]

class FastBM25:
    def __init__(self, corpus):
        self.corpus = corpus
        self.doc_len = [len(tokenize(d['text'])) for d in corpus]
        self.avg_dl = sum(self.doc_len) / (len(self.doc_len) or 1)
        self.df = Counter()
        for d in corpus:
            tokens = set(tokenize(d['text']))
            for t in tokens:
                self.df[t] += 1
        self.N = len(corpus)
        self.k1 = 1.5
        self.b = 0.75

    def search(self, query: str, top_k: int = 5, category_filter: str = None):
        q_tokens = tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            if category_filter and doc.get('category') != category_filter:
                continue
            doc_tokens = tokenize(doc['text'])
            doc_len = self.doc_len[idx]
            score = 0.0
            t_counts = Counter(doc_tokens)
            for t in q_tokens:
                if t in self.df:
                    idf = math.log((self.N - self.df[t] + 0.5) / (self.df[t] + 0.5) + 1.0)
                    tf = t_counts[t]
                    num = tf * (self.k1 + 1)
                    denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / (self.avg_dl or 1)))
                    score += idf * (num / denom)
            if score > 0:
                scores.append((score, doc))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores[:top_k]

def run_tests():
    print("==================================================")
    print("📚 ANYTIME.GR RAG DATASET VERIFICATION & SEARCH")
    print("==================================================")
    
    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    print(f"Total Documents: {catalog['statistics']['total_documents']}")
    print(f"  - PDFs: {catalog['statistics']['pdf_documents']}")
    print(f"  - Web Pages: {catalog['statistics']['web_documents']}")
    print(f"Total Chunks: {catalog['statistics']['total_chunks']}")
    print(f"Total FAQ QA Pairs: {catalog['statistics']['total_faq_pairs']}")
    print(f"Total Words: {catalog['statistics']['total_words']:,}")
    print("\nCategories Distribution:")
    for cat, info in sorted(catalog["categories_breakdown"].items()):
        print(f"  • {cat:<28}: {info['docs_count']:>2} docs | {info['chunks_count']:>4} chunks")

    chunks = load_chunks()
    bm25 = FastBM25(chunks)
    
    test_queries = [
        "Ποιες καλύψεις περιλαμβάνει η βασική ασφάλεια αυτοκινήτου Standard Drive;",
        "Τι είναι το πρόγραμμα Short Drive και πώς μετριούνται τα χιλιόμετρα;",
        "Ποιες είναι οι προϋποθέσεις για την έκπτωση στον ΕΝΦΙΑ για ασφάλιση κατοικίας;",
        "Πώς λειτουργεί ο φιλικός διακανονισμός σε περίπτωση τροχαίου ατυχήματος;",
        "Τι καλύπτει η παιδική ασφάλεια Child Care και ποια νοσοκομεία περιλαμβάνει;"
    ]

    print("\n" + "="*60)
    print("🔍 TESTING SAMPLE RAG RETRIEVAL QUERIES")
    print("="*60)
    
    for q in test_queries:
        print(f"\n[QUERY] {q}")
        results = bm25.search(q, top_k=2)
        for rank, (score, chunk) in enumerate(results, 1):
            print(f"  Rank #{rank} (Score: {score:.2f}) | [{chunk['category']}] | Doc: {chunk['doc_title']}")
            print(f"  Source: {chunk['source_type']} -> {chunk['source_url']}")
            snippet = chunk['text'].replace('\n', ' ')[:180]
            print(f"  Snippet: {snippet}...\n")

if __name__ == '__main__':
    run_tests()
