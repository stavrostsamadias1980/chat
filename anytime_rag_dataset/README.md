# 🏛️ Anytime.gr RAG Knowledge Base & Dataset

Πλήρες dataset εγγράφων, όρων ασφάλισης, ενημερωτικών εντύπων (IPIDs), διαδικασιών αποζημίωσης, συχνών ερωτήσεων (FAQs) και πληροφοριών καλύψεων από το **[anytime.gr](https://www.anytime.gr)**, οργανωμένο και έτοιμο για εκπαίδευση / τροφοδοσία σε συστήματα **RAG (Retrieval-Augmented Generation)**, Vector Databases και LLMs.

---

## 📊 Στατιστικά Dataset

| Μετρική | Τιμή |
| :--- | :--- |
| **Συνολικά Έγγραφα** | **165** (67 PDFs + 98 Web Pages) |
| **Συνολικά Chunks (RAG Chunks)** | **2.430** |
| **FAQ Ερωταπαντήσεις (Structured Q&A)** | **787 ζεύγη** |
| **Σύνολο Λέξεων** | **429.625 λέξεις** |
| **Γλώσσα** | Ελληνικά (Greek, UTF-8) |
| **Πρωτογενείς Πηγές** | `www.anytime.gr`, `assets-eu-01.kc-usercontent.com` (Kontent.ai CDN) |

---

## 📁 Δομή Φακέλων & Οργάνωση

```text
anytime_rag_dataset/
│
├── 📂 raw_pdfs/                           <-- Τα αυθεντικά αρχεία PDF κατηγοριοποιημένα
│   ├── 📁 car_insurance/                 <-- IPID & Όροι Αυτοκινήτου (Standard, Short, Smart, Μικτή)
│   ├── 📁 moto_insurance/                <-- IPID Μοτοσυκλέτας
│   ├── 📁 truck_trailer_insurance/       <-- IPID & Όροι Φορτηγών, Αγροτικών & Trailer
│   ├── 📁 home_property_insurance/       <-- Όροι Κατοικίας, ΕΝΦΙΑ, Βραχυχρόνια Μίσθωση, Prosperty
│   ├── 📁 health_insurance/              <-- Child Care, Accident Care, Health Value, Νοσοκομεία
│   ├── 📁 travel_insurance/              <-- IPID, Όροι Travel Premium, Αποζημιώσεις
│   ├── 📁 cyber_insurance/               <-- Βιβλίο Όρων & IPID Cyber Insurance
│   ├── 📁 micro_mobility_ebikes/         <-- IPID & Όροι e-Bikes & e-Scooters
│   ├── 📁 business_insurance/            <-- IPID & Όροι Επιχείρησης
│   ├── 📁 roadside_assistance_claims/    <-- Φιλικός Διακανονισμός, Έντυπα Αποζημίωσης, Οδική
│   ├── 📁 legal_compliance_gdpr/         <-- GDPR, Κώδικας Δεοντολογίας, Δηλώσεις Εναντίωσης
│   └── 📁 offers_partnerships/           <-- Όροι προσφορών και συνεργασιών
│
├── 📂 extracted_text/
│   ├── 📁 pdf_text/                      <-- Εξαγμένα πλήρη κείμενα από τα PDFs ανά σελίδα (.md & .json)
│   └── 📁 web_pages/                     <-- Καθαρισμένα κείμενα από όλες τις σελίδες & καλύψεις (.md & .json)
│
├── 📂 rag_ready_chunks/                  <-- ΕΤΟΙΜΑ CHUNKS ΓΙΑ EMBEDDINGS & VECTOR DBs
│   ├── 📄 chunks.jsonl                   <-- Ενιαίο Master αρχείο με όλα τα 2.430 chunks με metadata
│   ├── 📄 faq_qa_pairs.jsonl             <-- 787 αυτόνομα ζεύγη Ερώτησης-Απάντησης
│   ├── 📄 rag_catalog.json               <-- Master Catalog με ευρετήριο και στατιστικά
│   └── 📁 by_category/                   <-- Μεμονωμένα chunks ανά κατηγορία:
│       ├── car_insurance_chunks.jsonl (415 chunks)
│       ├── home_property_insurance_chunks.jsonl (424 chunks)
│       ├── legal_compliance_gdpr_chunks.jsonl (385 chunks)
│       ├── faq_general_chunks.jsonl (364 chunks)
│       ├── truck_trailer_insurance_chunks.jsonl (155 chunks)
│       ├── health_insurance_chunks.jsonl (142 chunks)
│       ├── micro_mobility_ebikes_chunks.jsonl (137 chunks)
│       ├── general_info_chunks.jsonl (134 chunks)
│       ├── business_insurance_chunks.jsonl (87 chunks)
│       ├── travel_insurance_chunks.jsonl (77 chunks)
│       ├── cyber_insurance_chunks.jsonl (42 chunks)
│       ├── offers_partnerships_chunks.jsonl (39 chunks)
│       └── roadside_assistance_claims_chunks.jsonl (29 chunks)
│
└── 📄 rag_loader_example.py              <-- Έτοιμος κώδικας φόρτωσης σε LlamaIndex, LangChain, ChromaDB
```

---

## 🏷️ Metadata Schema ανά Chunk (`chunks.jsonl`)

Κάθε εγγραφή στο `chunks.jsonl` είναι ένα έγκυρο JSON αντικείμενο με τα εξής πεδία:

```json
{
  "chunk_id": "chk_pdf_car_insurance_eggrafo_pliroforion_standard_092023_001",
  "doc_id": "pdf_car_insurance_eggrafo_pliroforion_standard_092023",
  "doc_title": "Έγγραφο Πληροφοριών Standard Drive",
  "source_type": "pdf", // ή "web_page"
  "source_url": "https://assets-eu-01.kc-usercontent.com/.../eggrafo_pliroforion_standard_092023.pdf.pdf",
  "category": "car_insurance",
  "subcategory": "motor_auto",
  "doc_type": "ipid_information_document", // policy_terms, claims_guide, faq, κλπ.
  "chunk_index": 1,
  "total_chunks_in_doc": 6,
  "char_length": 782,
  "token_estimate": 195,
  "text": "ΕΓΓΡΑΦΟ ΠΛΗΡΟΦΟΡΙΩΝ ΓΙΑ ΤΟ ΑΣΦΑΛΙΣΤΙΚΟ ΠΡΟΪΟΝ..."
}
```

---

## 🚀 Πώς να το χρησιμοποιήσετε στο δικό σας RAG σύστημα

### 1. Γρήγορη Δοκιμή Αναζήτησης (BM25 Search)
Εκτελέστε το παρεχόμενο script αναζήτησης:
```bash
python query_and_verify_rag.py
```

### 2. Φόρτωση σε LlamaIndex
```python
import json
from llama_index.core import Document, VectorStoreIndex

documents = []
with open("anytime_rag_dataset/rag_ready_chunks/chunks.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        chk = json.loads(line)
        documents.append(Document(
            text=chk["text"],
            doc_id=chk["chunk_id"],
            metadata={
                "category": chk["category"],
                "doc_title": chk["doc_title"],
                "source_url": chk["source_url"],
                "doc_type": chk["doc_type"]
            }
        ))

# Δημιουργία Vector Index
index = VectorStoreIndex.from_documents(documents)
query_engine = index.as_query_engine()
response = query_engine.query("Ποιες καλύψεις έχει το πρόγραμμα Smart Drive;")
print(response)
```

### 3. Φόρτωση σε LangChain & ChromaDB / FAISS
```python
import json
from langchain.schema import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings # ή HuggingFaceEmbeddings

docs = []
with open("anytime_rag_dataset/rag_ready_chunks/chunks.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        chk = json.loads(line)
        docs.append(Document(page_content=chk["text"], metadata=chk))

# vector_store = Chroma.from_documents(docs, OpenAIEmbeddings())
```

---

## 📑 Βασικές Κατηγορίες Καλύψεων & Εγγράφων που περιλαμβάνονται

1. **Αυτοκίνητο & Οχήματα (Auto & Motor)**
   - Προγράμματα: *Standard Drive, Short Drive (με μετρητή χιλιομέτρων), Smart Drive (με τηλεματική εφαρμογή), Μικτή Ασφάλεια*.
   - Έγγραφα: IPIDs, Όροι ασφάλισης, Όροι εφαρμογών, Φιλικός διακανονισμός, Έντυπο αναγγελίας αποζημίωσης.
2. **Μοτοσυκλέτα (Moto)**: Πλήρες IPID & καλύψεις δικύκλων.
3. **Φορτηγά, Αγροτικά & Trailer**: IPIDs & προγράμματα επαγγελματικών οχημάτων.
4. **Κατοικία & Περιουσία (Home & Property)**
   - Κτήριο, Περιεχόμενο, Κτήριο & Περιεχόμενο.
   - Έκπτωση ΕΝΦΙΑ (διαδικασίες, προϋποθέσεις, απαραίτητες καλύψεις).
   - Βραχυχρόνια Μίσθωση (Airbnb) & Απώλεια Ενοικίων (Prosperty).
5. **Υγεία (Health)**: Child Care, Accident Care, Health Value, Λίστες συνεργαζόμενων δημόσιων/ιδιωτικών νοσοκομείων & διαγνωστικών κέντρων, διαδικασίες αποζημίωσης.
6. **Ταξιδιωτική Ασφάλιση (Travel)**: IPID, όροι Travel Premium, αποζημιώσεις ακύρωσης/ιατρικών.
7. **Cyber Insurance**: Βιβλίο Όρων & IPID προστασίας online συναλλαγών/κυβερνοεπιθέσεων.
8. **e-Bikes & e-Scooters**: IPIDs & όροι μικροκινητικότητας.
9. **Επιχείρηση (Business)**: IPID & όροι επαγγελματικής στέγης.
10. **Οδική Βοήθεια & Αποζημιώσεις**: Διαδικασίες 24/7, αλλαγή μπαταρίας επί τόπου, Carpoint, Drive On.
11. **Συχνές Ερωτήσεις (FAQs)**: 787 λεπτομερείς ερωταπαντήσεις για όλα τα θέματα.
