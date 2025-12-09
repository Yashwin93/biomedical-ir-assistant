"""
File: main.py
Purpose: Defines retrieval pipelines for the Biomedical IR Assistant.
Includes BM25 baseline, RM3 pseudo-relevance feedback, and MeSH-based query expansion.
"""

import os
import pyterrier as pt

def init_pyterrier():
    """
    Initialize PyTerrier if not already started.
    Ensures Terrier IR platform is ready for indexing and retrieval.
    """
    if not pt.started():
        pt.init()

def load_index(index_path="index_dir"):
    """
    Load Terrier index from the specified path.

    Args:
        index_path (str): Relative path to the index directory.

    Returns:
        pt.Index: Loaded Terrier index object.
    """
    init_pyterrier()
    # Construct absolute path to index directory
    abs_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), index_path)
    return pt.IndexFactory.of(abs_path)

def bm25_pipeline(index):
    """
    Define BM25 retrieval pipeline.

    Args:
        index (pt.Index): Terrier index object.

    Returns:
        pt.BatchRetrieve: BM25 pipeline with metadata fields.
    """
    return pt.BatchRetrieve(index, wmodel="BM25", metadata=["docno", "title", "abstract"])

def rm3_pipeline(index):
    """
    Define RM3 pseudo-relevance feedback pipeline.

    Args:
        index (pt.Index): Terrier index object.

    Returns:
        pt.Pipeline: RM3 expansion applied on BM25 baseline.
    """
    bm25 = bm25_pipeline(index)
    # RM3 expands queries using top-ranked BM25 documents, then re-runs BM25
    return bm25 >> pt.rewrite.RM3(index) >> bm25

def run_query(pipeline, query, k=10):
    """
    Run a query on the given pipeline.

    Args:
        pipeline (pt.Pipeline): Retrieval pipeline (BM25, RM3, or MeSH).
        query (str): Query string.
        k (int): Number of top results to return.

    Returns:
        pd.DataFrame: Top-k retrieved documents.
    """
    return pipeline.search(query).head(k)

# -------------------------------
# Simple lookup dictionary for demo purposes.
# Maps biomedical terms to MeSH synonyms.
# -------------------------------
MESH_LOOKUP = {
    "cancer": ["neoplasm", "tumor", "carcinoma"],
    "diabetes": ["hyperglycemia", "insulin resistance"],
    "stroke": ["cerebrovascular accident", "brain ischemia"],
}

def expand_with_mesh(query):
    """
    Expand query terms using a simple MeSH synonym dictionary.

    Args:
        query (str): Original query string.

    Returns:
        list: Expansion terms from MeSH lookup.
    """
    expansions = []
    for term in query.lower().split():
        if term in MESH_LOOKUP:
            expansions.extend(MESH_LOOKUP[term])
    return expansions

def mesh_pipeline(index, query):
    """
    Expand the query with MeSH terms, then run BM25.

    Args:
        index (pt.Index): Terrier index object.
        query (str): Original query string.

    Returns:
        pd.DataFrame: Retrieved documents using expanded query.
    """
    mesh_terms = expand_with_mesh(query)
    expanded_query = query + " " + " ".join(mesh_terms)
    bm25 = bm25_pipeline(index)
    return bm25.search(expanded_query)
