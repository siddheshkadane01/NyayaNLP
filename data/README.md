# Data

This project uses multiple legal datasets/corpora.

## Folder meanings

- `data/raw/` — original datasets/corpora (downloaded or manually placed)
- `data/processed/` — cleaned/normalized outputs ready for training
- `data/annotated/` — human-labeled data (e.g., Label Studio exports)

## Step 1: Dataset acquisition (roles)

### InLegalNER (English legal NER)
- **Role:** English Legal NER baseline + training source
- **How we use it:** fine-tune token-classification models
- **Status:** downloadable via Hugging Face Datasets
- **Location after download:** `data/raw/inlegalner/`

Note: this dataset may be **gated** on Hugging Face. If the download fails with an authentication error:

1) Open the dataset page in your browser and request/accept access (if prompted)
2) Authenticate locally:

```bash
huggingface-cli login
```

3) Re-run the download.

Download command:

```bash
source .venv/bin/activate
python data/download_datasets.py --inlegalner
```

### HLDC (Hindi legal corpus)
- **Role:** Hindi legal text source
- **How we use it:** sentence segmentation + human annotation for NER/segmentation
- **Status:** may require manual download + annotation workflow
- **Suggested location:** `data/raw/hldc/` (place raw files here)

### MILPaC (cross-lingual alignment)
- **Role:** aligned statutes / parallel data for cross-lingual experiments
- **How we use it:** alignment + clause/section segmentation dataset creation
- **Status:** often manual download depending on source
- **Suggested location:** `data/raw/milpac/`

### IL-TUR (benchmark evaluation)
- **Role:** benchmarking and evaluation
- **How we use it:** evaluate model robustness
- **Status:** depends on source/access
- **Suggested location:** `data/raw/il-tur/`

## Manifest

When you download datasets using `data/download_datasets.py`, a manifest is written to:

- `data/raw/datasets_manifest.json`

This records what was downloaded, where it was saved, and basic split/feature info.
