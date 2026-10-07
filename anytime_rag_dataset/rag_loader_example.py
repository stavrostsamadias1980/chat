"""
Ready-to-use RAG Ingestion & VectorDB Loader Examples for Anytime.gr Dataset
Supported Frameworks:
  1. LangChain
  2. LlamaIndex
  3. ChromaDB / SentenceTransformers
  4. Google Gemini Embeddings
"""

import json
from pathlib import Path

DATASET_DIR = Path("g:/WIDGET-UI/anytime_rag_dataset")
CHUNKS_PATH = DATASET_DIR / "rag_ready_chunks" / "chunks.jsonl"
FAQS_PATH = DATASET_DIR / "rag_ready_chunks" / "faq_qa_pairs.jsonl"

def get_raw_chunks(category: str = None):
    """Loads all chunks or filtered by category."""
    chunks = []
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                item = json.loads(line)
                if category is None or item.get("category") == category:
                    chunks.append(item)
    return chunks

# -------------------------------------------------------------
# 1. LAMBDA / LLAMA-INDEX LOADER
# -------------------------------------------------------------
def load_into_llama_index():
    try:
        from llama_index.core import Document, VectorStoreIndex
        chunks = get_raw_chunks()
        documents = []
        for chk in chunks:
            doc = Document(
                text=chk["text"],
                doc_id=chk["chunk_id"],
                metadata={
                    "doc_title": chk["doc_title"],
                    "source_type": chk["source_type"],
                    "source_url": chk["source_url"],
                    "category": chk["category"],
                    "subcategory": chk["subcategory"],
                    "doc_type": chk["doc_type"],
                    "chunk_index": chk["chunk_index"]
                }
            )
            documents.append(doc)
        print(f"[LlamaIndex] Prepared {len(documents)} Document objects ready for VectorStoreIndex.from_documents(documents)")
        return documents
    except ImportError:
        print("[LlamaIndex] llama-index not installed. Install with `pip install llama-index`")

# -------------------------------------------------------------
# 2. LANGCHAIN LOADER
# -------------------------------------------------------------
def load_into_langchain():
    try:
        from langchain.schema import Document
        chunks = get_raw_chunks()
        documents = []
        for chk in chunks:
            doc = Document(
                page_content=chk["text"],
                metadata={
                    "id": chk["chunk_id"],
                    "title": chk["doc_title"],
                    "source": chk["source_url"],
                    "source_type": chk["source_type"],
                    "category": chk["category"],
                    "doc_type": chk["doc_type"]
                }
            )
            documents.append(doc)
        print(f"[LangChain] Prepared {len(documents)} Document objects ready for FAISS.from_documents(documents, embeddings)")
        return documents
    except ImportError:
        print("[LangChain] langchain not installed. Install with `pip install langchain`")

# -------------------------------------------------------------
# 3. CHROMADB NATIVE LOADER
# -------------------------------------------------------------
def load_into_chromadb(collection_name="anytime_insurance_rag"):
    try:
        import chromadb
        client = chromadb.Client()
        collection = client.get_or_create_collection(name=collection_name)
        
        chunks = get_raw_chunks()
        
        # Batch insert
        batch_size = 500
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            collection.add(
                ids=[c["chunk_id"] for c in batch],
                documents=[c["text"] for c in batch],
                metadatas=[{
                    "title": c["doc_title"],
                    "url": c["source_url"],
                    "category": c["category"],
                    "doc_type": c["doc_type"]
                } for c in batch]
            )
        print(f"[ChromaDB] Successfully inserted {len(chunks)} chunks into collection '{collection_name}'")
        return collection
    except ImportError:
        print("[ChromaDB] chromadb not installed. Install with `pip install chromadb`")

if __name__ == "__main__":
    print(f"Total available chunks in dataset: {len(get_raw_chunks())}")
    load_into_llama_index()
    load_into_langchain()
