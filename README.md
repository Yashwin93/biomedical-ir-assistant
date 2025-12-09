# Biomedical IR Assistant (BM25 vs RM3 vs MeSH)

## 🎯 Objective
This project compares three biomedical document retrieval pipelines — BM25, RM3 pseudo-relevance feedback, and MeSH-based semantic expansion — using PyTerrier and a Streamlit interface. It demonstrates how semantic enrichment improves retrieval effectiveness and provides a reproducible evaluation workflow.

## Features
- BM25 baseline and RM3 expansion pipelines
- MeSH-based query enrichment using biomedical vocabulary
- Metadata-aware retrieval (docno, title, abstract)
- Streamlit UI with method toggle, top-10 abstract display, and Excel download
- Evaluation metrics: MAP, Precision@10, nDCG@10
- Modular codebase with clear separation of concerns

## Quick start (<= 6 minutes)
1. Clone repo:
   git clone https://github.com/Yashwin93/biomedical-ir-assistant.git
   cd biomedical-ir-assistant

2. Create virtual environment (Windows):
   python -m venv .venv
   .\.venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Build tiny demo index (first run):
   python -m src.indexing

5. Run the app:
   streamlit run src/app.py

## Code structure
BIOMEDICAL-IR-ASSISTANT/
│
├── .venv/                        # Virtual environment (excluded from GitHub)
│
├── app.py                        # Streamlit UI (outside src)
│
├── data/                         # Raw and processed data
│   ├── xml/                      # Original XML files (optional)
│   ├── pmc_oa.tar.gz             # Compressed PMC OA dataset
│   ├── pmc_subset.json           # Parsed biomedical documents
│   ├── queries.csv               # Query set for evaluation
│   ├── qrels_completed.csv       # Relevance judgments
|   ├── README.md                 # Data Documentation — Biomedical IR Assistant  
│
├── index_dir/                    # Terrier index files
│   ├── data.direct.bf
│   ├── data.document.fsarrayfile
│   ├── data.inverted.bf
│   ├── data.lexicon.fsomapfile
│   ├── data.meta.idx
│   └── ...                       # Other index artifacts
│
├── results/                      # Evaluation outputs
│   ├── evaluation_metrics.csv
│   ├── evaluation_chart.png
│
├── src/                          # Source code
│   ├── __init__.py
│   ├── evaluate.py               # Evaluation logic
│   ├── indexing.py               # Index builder
│   ├── main.py                   # BM25, RM3, MeSH pipelines
│   ├── utils.py                  # Path helpers
│
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies


## Data
All data files are stored in the data/ folder.
- pmc_subset.json contains biomedical abstracts and metadata.
- queries.csv defines search intents.
- qrels_completed.csv contains relevance judgments.
See data/README.md for schema and provenance details

## Evaluation
To run evaluation:
python src/evaluate.py

This will compute MAP, Precision@10, and nDCG@10 across all pipelines and save results to results/evaluation_metrics.csv. A chart is also generated for visual comparison.

- Full datasets and large indexes are excluded. Regenerate locally via indexing.py.
- RM3 expands queries using top-ranked BM25 documents, so results will differ by design.
- MeSH expansion enriches queries with biomedical vocabulary for improved recall.

## References
See project_report.pdf for academic references and visuals supporting this implementation.


## Notes
- Full datasets and large indexes are excluded. Regenerate locally via indexing.py.
- RM3 reorders results by expanding queries using top-ranked BM25 docs — so BM25 and RM3 will differ by design.

