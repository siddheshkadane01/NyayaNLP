# Multilingual Legal NLP (Indian Languages)

This project is a research-grade plan for building a **multilingual legal NLP system** focused on **Indian legal text** (English + Hindi, optionally Marathi). The system targets:

- **Legal NER** (token classification / named entity extraction)
- **Clause / section extraction** (segmentation)
- **Cross-lingual transfer** (zero-shot + few-shot)
- **Semantic alignment** (meaning consistency across languages)
- **Prototype API deployment** (FastAPI)

## What You Build (Simple I/O)

### 1) Legal NER (Entity Extraction)
- **Input:** Legal text (sentence/paragraph) in English/Hindi/etc.
- **Output:** Entities with spans/labels (e.g., `ACT`, `SECTION`, `CLAUSE`, `COURT`, `DATE`, `PENALTY`).

Example:
- Input: `Under Section 302 of IPC, the accused ...`
- Output: `SECTION=302`, `ACT=IPC`

### 2) Clause / Section Segmentation
- **Input:** Long legal passage (multiple sentences).
- **Output:** Split/marked structure such as clause blocks or sentence tags like `CLAUSE_START` / `CLAUSE_CONTINUE`.

### 3) Cross-lingual Transfer
- **Input:** Model trained on English-heavy data, tested on Hindi/Marathi.
- **Output:** Language-wise metrics (Precision/Recall/F1), plus a comparison of:
  - **Zero-shot:** train on English, test on Hindi/Marathi
  - **Few-shot:** fine-tune with ~50–200 labeled samples per target language

### 4) Semantic Alignment (Consistency)
- **Input:** Parallel or comparable statute text across languages (e.g., English vs Hindi).
- **Output:** Similarity score and mismatch flags when meaning is likely inconsistent.

### 5) API Prototype
- **Input:** Request to endpoints like `/extract-entities`, `/segment-clauses`.
- **Output:** JSON results containing extracted entities and clause segments.

---

## Recommended Models

- **Primary:** `xlm-roberta-base` (strong cross-lingual baseline)
- **Baseline comparison:** IndicBERT
- **Efficiency:** LoRA/QLoRA via `peft`

---

## Datasets Mentioned (Role Mapping)

From the project notes:

- **InLegalNER** → English Legal NER dataset
- **HLDC** → Hindi legal corpus (requires annotation for NER/segmentation tasks)
- **MILPaC** → Cross-lingual / aligned statutes for alignment and segmentation work
- **IL-TUR** → Benchmark evaluation dataset

> Note: Exact dataset formats differ; you normalize them into a HuggingFace token-classification / sentence-classification format.

---

## Repo References

- [project.md](project.md) — 2-month condensed plan
- [steps.txt](steps.txt) — full execution manual (research-grade)

---

## Setup (Python)

Create and activate a virtual environment:

```bash
python -m venv legal_ai
source legal_ai/bin/activate
```

Install dependencies (core set used in the notes):

```bash
pip install torch transformers datasets seqeval peft
pip install indic-nlp-library sentence-transformers
pip install fastapi uvicorn pandas numpy scikit-learn
```

---

## Suggested Project Structure

This is the intended structure described in the notes (create as you implement):

```text
legal-ai/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── annotated/
│
├── training/
│   ├── ner_train.py
│   ├── clause_train.py
│
├── evaluation/
│   ├── metrics.py
│   ├── error_analysis.py
│
├── inference/
│   ├── ner_infer.py
│
├── api/
│   ├── app.py
│
└── report/
```

---

## Execution Roadmap (High Level)

### Month 1
- Collect and clean multilingual legal corpus (English + Hindi + optional Marathi)
- Define annotation schema (ACT, SECTION, CLAUSE, COURT, DATE, PENALTY)
- Annotate ~1,000–2,000 sentences per language (or start with smaller + expand)
- Train baselines: mBERT/IndicBERT, then XLM-R
- Evaluate per-language; do error analysis

### Month 2
- Cross-lingual transfer: zero-shot and few-shot experiments
- Semantic alignment: sentence similarity across translations
- Build FastAPI prototype (`/extract-entities`, `/segment-clauses`)
- Final evaluation + report (language-wise + entity-wise metrics, fairness notes)

---

## Metrics

Common metrics used in the plan:
- Precision / Recall / F1 (entity-wise + language-wise)
- Cross-lingual performance gap
- Alignment quality: cosine similarity / BERTScore (optional)

---

## Outcome

By the end, you should have:
- A multilingual legal NER + clause segmentation model
- Cross-lingual transfer results (zero-shot + few-shot)
- A semantic alignment checker for translated statutes
- A demo-ready API service
- A report suitable for internship/research submission
