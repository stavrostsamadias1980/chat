"""
Interactive Anytime.gr RAG Search Tool
Run via:
  python interactive_search.py "Η ερώτησή σας εδώ"
Or simply:
  python interactive_search.py
"""

import sys
import os
import json
import math
import re
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

DATASET_DIR = Path(__file__).resolve().parent / "anytime_rag_dataset"
CHUNKS_FILE = DATASET_DIR / "rag_ready_chunks" / "chunks.jsonl"
FAQ_FILE = DATASET_DIR / "rag_ready_chunks" / "faq_qa_pairs.jsonl"

def tokenize(text: str) -> list[str]:
    # Simple greek and english tokenizer with basic lowercase
    text = text.lower()
    # Normalize Greek accents for search robustness
    trans = str.maketrans("άέήίόύώϊϋΐΰ", "αεηιουωιυιυ")
    text = text.translate(trans)
    return [w for w in re.findall(r'\b\w+\b', text) if len(w) > 1]

class SearchEngine:
    def __init__(self):
        print("⏳ Φόρτωση RAG Chunks & FAQs...")
        self.chunks = []
        if CHUNKS_FILE.exists():
            with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        self.chunks.append(json.loads(line))
                        
        self.faqs = []
        if FAQ_FILE.exists():
            with open(FAQ_FILE, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        self.faqs.append(json.loads(line))
                        
        print(f"✅ Φορτώθηκαν {len(self.chunks)} RAG Chunks και {len(self.faqs)} FAQ pairs!")
        
        # Build BM25 index for chunks
        self.doc_len = [len(tokenize(d['text'])) for d in self.chunks]
        self.avg_dl = sum(self.doc_len) / (len(self.doc_len) or 1)
        self.df = Counter()
        for d in self.chunks:
            tokens = set(tokenize(d['text']))
            for t in tokens:
                self.df[t] += 1
        self.N = len(self.chunks)
        self.k1 = 1.5
        self.b = 0.75

    def search_faqs(self, query: str, top_k: int = 3):
        q_tokens = set(tokenize(query))
        faq_scores = []
        for faq in self.faqs:
            q_text = faq.get("question", "")
            a_text = faq.get("answer", "")
            tokens = set(tokenize(q_text + " " + a_text))
            overlap = len(q_tokens.intersection(tokens))
            if overlap > 0:
                # give higher weight to question match
                q_overlap = len(q_tokens.intersection(set(tokenize(q_text))))
                score = (q_overlap * 3.0) + overlap
                faq_scores.append((score, faq))
        faq_scores.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in faq_scores[:top_k]]

    def search_chunks(self, query: str, top_k: int = 4, category: str = None):
        q_tokens = tokenize(query)
        scores = []
        for idx, doc in enumerate(self.chunks):
            if category and doc.get('category') != category:
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

    def query(self, user_query: str, category: str = None, top_k: int = 3):
        print("\n" + "="*75)
        print(f"🔍 ΕΡΩΤΗΣΗ: \"{user_query}\"")
        if category:
            print(f"📁 Φίλτρο Κατηγορίας: [{category}]")
        print("="*75)

        # 1. Check FAQs first
        faq_results = self.search_faqs(user_query, top_k=2)
        if faq_results:
            print("\n💡 ΑΜΕΣΕΣ ΣΥΧΝΕΣ ΕΡΩΤΗΣΕΙΣ (FAQ MATCHES):")
            for idx, faq in enumerate(faq_results, 1):
                print(f"  [{idx}] ❓ {faq['question']}")
                print(f"      💬 {faq['answer'][:250]}...")
                print(f"      🔗 Πηγή: {faq['source_url']}\n")

        # 2. Check Chunks (from PDFs and Web content)
        chunk_results = self.search_chunks(user_query, top_k=top_k, category=category)
        if chunk_results:
            print("📑 ΣΧΕΤΙΚΑ ΑΠΟΣΠΑΣΜΑΤΑ ΑΠΟ ΕΓΓΡΑΦΑ & PDFs (RAG CHUNKS):")
            for rank, (score, chunk) in enumerate(chunk_results, 1):
                doc_type = chunk.get('doc_type', 'general')
                src_type = chunk.get('source_type', 'unknown').upper()
                print(f"\n  ┌─ [Αποτέλεσμα #{rank}] (Score: {score:.2f}) | Τύπος: {src_type} ({doc_type})")
                print(f"  │  Τίτλος: {chunk['doc_title']}")
                print(f"  │  Κατηγορία: {chunk['category']} / {chunk['subcategory']}")
                print(f"  │  URL / Αρχείο: {chunk['source_url']}")
                print(f"  └──────────────────────────────────────────────────────────")
                
                # Format text with nice indent
                lines = chunk['text'].strip().split('\n')
                print("     " + "\n     ".join(lines[:12]))
                if len(lines) > 12:
                    print("     [...]")
        else:
            print("⚠️ Δεν βρέθηκαν σχετικά αποτελέσματα.")

def main():
    engine = SearchEngine()
    
    if len(sys.argv) > 1:
        query_text = " ".join(sys.argv[1:])
        engine.query(query_text)
    else:
        print("\n" + "="*60)
        print("🌟 ΠΛΗΚΤΡΟΛΟΓΗΣΤΕ ΤΗΝ ΕΡΩΤΗΣΗ ΣΑΣ (ή 'exit' για έξοδο)")
        print("="*60)
        while True:
            try:
                q = input("\n👉 Ερώτηση: ").strip()
                if not q or q.lower() in ['exit', 'quit', 'q']:
                    break
                engine.query(q)
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    main()
