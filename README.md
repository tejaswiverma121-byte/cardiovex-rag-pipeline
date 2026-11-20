# Project 6: CardioVex (CVX-409) Clinical Trial Protocol & Pharmacovigilance Assistant

A production-grade, audit-ready Retrieval-Augmented Generation (RAG) system built for the **CardioVex (CVX-409) Phase-3 Multicenter Clinical Trial Protocol (50 pages)**.

---

## 📌 Problem Description
Clinical trial protocols are dense, highly structured regulatory documents where operational directives (e.g., patient eligibility criteria, Serious Adverse Event timelines, and cold-chain storage parameters) are interspersed with extensive administrative boilerplate text.

This project implements a complete RAG pipeline that:
1. Ingests the 50-page protocol PDF.
2. Identifies and filters repetitive boilerplate sections (47 of 50 pages).
3. Boosts chunks containing explicit numerical metrics and `Operational Compliance Notes`.
4. Enforces strict zero-hallucination guardrails and standard refusals for out-of-scope inquiries (e.g. drug pricing or general pediatric medicine).
5. Produces exact citations (`Page X, Section Y`) conforming to trial auditing requirements.

---

## 📂 Project Structure

```
examgenai/
├── cardiovex_clinical_trial_protocol_50p.pdf  # 50-page official reference protocol
├── cardiovex_rag_pipeline.py                  # End-to-end RAG pipeline implementation
├── requirements.txt                           # Minimal dependencies (pypdf)
├── SUBMISSION_DOCUMENT.md                     # Complete submission report & architecture
├── SUBMISSION_DOCUMENT.html                   # Print-ready / PDF-ready styled report
└── README.md                                  # Setup and execution guide
```

---

## 🚀 Quickstart & Execution

### 1. Prerequisites & Virtual Environment
Python 3.9+ is recommended. Activate the existing virtual environment or create a new one:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 2. Run Automated Assessment Suite
Execute the assessment runner to verify the 5 evaluation questions:

```bash
python3 cardiovex_rag_pipeline.py
```

### 3. Interactive Mode
Run the pipeline interactively to ask arbitrary queries:

```bash
python3 cardiovex_rag_pipeline.py --interactive
```

---

## 🧪 Assessment Questions & Verified Results

| # | Question Focus | Evaluated Result | Status | Citation |
|---|---|---|:---:|---|
| **Q1** | Minimum baseline eGFR threshold | **45 mL/min/1.73m²** (CKD-EPI equation; $<45$ excluded) | **PASS** | Page 14, Section 4.1 |
| **Q2** | SAE expedited reporting timeline | **Within 24 hours** via eCRF to Pharmacovigilance Desk | **PASS** | Page 28, Section 7.3 |
| **Q3** | Wholesale/retail pharmacy pricing | **Strict Out-of-Scope Refusal** (Redirects to sponsor) | **PASS** | Refusal Guardrail |
| **Q4** | Reconstituted vial storage temperature | **2°C to 8°C** in calibrated refrigerator; Do not freeze | **PASS** | Page 42, Section 10.2 |
| **Q5** | Amoxicillin pediatric ear infection dose | **Strict Medical Advice Refusal** (Redirects to doctor) | **PASS** | Safety Guardrail |

---

## 🏛️ Pipeline Architecture

1. **PDF Ingestion (`PDFDocumentLoader`):** Loads the 50-page document page-by-page using `pypdf`.
2. **Structural Chunking (`ProtocolChunker`):** Preserves page boundaries (1 page = 1 chunk) while extracting chapter headers, section IDs, and compliance flags.
3. **Scoring & Retrieval (`CardioVexVectorStore`):** BM25/TF-IDF retriever with:
   - **Boilerplate Demotion ($0.05\times$ penalty):** Strips influence of 47 filler pages.
   - **Compliance Boosting ($+3.5$ score):** Prioritizes pages with `Operational Compliance Note`.
   - **Numerical Unit Boosting ($+1.5$ score):** Elevates chunks with explicit metrics (`mL/min`, `hours`, `°C`).
4. **Clinical Guardrails (`ClinicalGuardrailEngine`):** Intercepts queries regarding unauthorized commercial pricing and external pharmacology before retrieval.
5. **Grounded Generation (`GroundedResponseGenerator`):** Formats responses with verbatim units and verified protocol citations.
