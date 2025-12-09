# Testing Log — Biomedical IR Assistant

This file records the final testing of the Biomedical IR Assistant before submission.

---

## Environment Setup
- ✅ Virtual environment created and activated
- ✅ Dependencies installed via `pip install -r requirements.txt`

## Indexing
- ✅ Index files already present in `index_dir/`
- ⚠️ Indexing script (`src/indexing.py`) not re-run to avoid overwriting existing index
- ✅ Verified index loads correctly via `load_index("index_dir")`

## Application (Streamlit UI)
- ✅ `streamlit run app.py` launches successfully
- ✅ Query input works
- ✅ Retrieval methods tested:
  - BM25 Baseline → returns top-10 results
  - RM3 Expansion → returns expanded results
  - MeSH Expansion → shows MeSH terms and results
- ✅ CSV download button produces `results.csv`

## Evaluation
- ✅ `python src/evaluate.py` runs successfully
- ✅ Metrics computed: MAP, Precision@10, nDCG@10
- ✅ Results saved to `results/evaluation_metrics.csv`
- ✅ Chart generated at `results/evaluation_chart.png`

## Data
- ✅ `data/queries.csv` and `data/qrels_completed.csv` load correctly
- ✅ Schema matches documentation in `data/README.md`

## Documentation
- ✅ Root `README.md` explains objectives, setup, usage, and evaluation
- ✅ `data/README.md` describes dataset schema and provenance
- ✅ Inline comments/docstrings present in all `.py` files

---

## Conclusion
All components tested successfully. The system is reproducible and ready for submission.
