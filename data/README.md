# Data Documentation — Biomedical IR Assistant

This folder contains all datasets and evaluation files used in the Biomedical IR Assistant project.  
The data is organized for clarity and reproducibility.

---

## 📂 Files

### `pmc_oa.tar.gz`
- **Description:** Compressed archive of PubMed Central Open Access (PMC OA) articles.
- **Purpose:** Raw source data used to build the biomedical document index.
- **Notes:** Large file; excluded from GitHub if size exceeds limits. Regenerate locally if needed.

### Large Raw XML Files
- The full PMC XML files (e.g., `PMC012xxxxxx`) exceed GitHub’s 100 MB file limit.
- These are excluded from the repository via `.gitignore`.
- To reproduce indexing, place the raw XML files in `data/xml/` and run `src/indexing.py`.
- Alternatively, use the provided `pmc_subset.json` for demo-scale experiments.

### `pmc_subset.json`
- **Description:** Parsed subset of PMC OA articles in JSON format.
- **Schema:**
  - `docno`: Unique document identifier
  - `title`: Article title
  - `abstract`: Abstract text
  - `metadata`: Additional fields (authors, journal, year)
- **Purpose:** Demo-scale dataset used for retrieval pipelines.

### `queries.csv`
- **Description:** Query set for evaluation.
- **Schema:**
  - `qid`: Query ID
  - `query`: Text of biomedical search intent
- **Purpose:** Defines search tasks for evaluation and demo.

### `qrels_completed.csv`
- **Description:** Relevance judgments for evaluation.
- **Schema:**
  - `qid`: Query ID
  - `docno`: Document identifier
  - `label`: Relevance score (1 = relevant, 0 = not relevant)
- **Purpose:** Provides ground truth for computing MAP, Precision@10, and nDCG@10.

---

## 📂 Index Directory

### `index_dir/`
- **Description:** Terrier index files generated from `pmc_subset.json`.
- **Contents:** Lexicon, inverted index, metadata, and properties files.
- **Purpose:** Enables BM25, RM3, and MeSH pipelines to run efficiently.

---

## 🔎 Provenance

- Source: [PubMed Central Open Access Subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/)
- Preprocessing: Articles parsed into JSON (`pmc_subset.json`) and indexed with PyTerrier (`index_dir/`).
- Evaluation: Queries and qrels manually structured for demo-scale testing.

---

## 📝 Notes

- Full PMC OA dataset is large; only a subset is included for demonstration.
- Index files are regenerated using `src/indexing.py` if not present.
- Ensure `queries.csv` and `qrels_completed.csv` are updated before running `src/evaluate.py`.

