"""
File: app.py
Purpose: Streamlit user interface for the Biomedical IR Assistant.
Provides query input, retrieval method selection (BM25, RM3, MeSH),
and displays top-k results with download functionality.
"""

import streamlit as st
from src.main import load_index, bm25_pipeline, rm3_pipeline, run_query, mesh_pipeline

# -------------------------------
# Streamlit page setup
# -------------------------------
st.set_page_config(page_title="Biomedical IR Assistant", layout="wide")
st.title("Biomedical Information Retrieval Assistant")

# -------------------------------
# Load index and retrieval pipelines
# -------------------------------
index = load_index("index_dir")        # Load Terrier index from folder
bm25 = bm25_pipeline(index)            # Initialize BM25 pipeline
rm3 = rm3_pipeline(index)              # Initialize RM3 pipeline

# -------------------------------
# Query input field
# -------------------------------
query = st.text_input("Enter your biomedical query:")

# -------------------------------
# Retrieval method selection (radio buttons)
# -------------------------------
method = st.radio(
    "Choose retrieval method:",
    ("BM25 Baseline", "RM3 Expansion", "MeSH Expansion")
)

# -------------------------------
# Search button logic
# -------------------------------
if st.button("Search"):
    if query.strip():  # Ensure query is not empty
        # Select pipeline based on chosen method
        if method == "BM25 Baseline":
            results = run_query(bm25, query, k=10)
        elif method == "RM3 Expansion":
            results = run_query(rm3, query, k=10)
        else:  # MeSH Expansion
            results = mesh_pipeline(index, query).head(10)

        # Show MeSH expansion terms if applicable
        if method == "MeSH Expansion":
            from src.main import expand_with_mesh
            mesh_terms = expand_with_mesh(query)
            if mesh_terms:
                st.caption(f"Expanded with MeSH terms: {', '.join(mesh_terms)}")

        # Display result count
        st.write(f"Showing top {len(results)} results for '{query}' using {method}")

        # -------------------------------
        # Download results as CSV
        # -------------------------------
        st.download_button(
            "Download results",
            results.to_csv(index=False),
            "results.csv",
            "text/csv"
        )

        # -------------------------------
        # Display each retrieved document
        # -------------------------------
        for _, row in results.iterrows():
            doc_id = row.get("docno", "Unknown Doc")
            title = row.get("title", "No title available")
            abstract = row.get("abstract", "No abstract available")

            # Show document ID and title
            st.markdown(f"**{doc_id}** — {title}")

            # Show snippet (first 500 chars of abstract)
            snippet = abstract[:500] + ("..." if len(abstract) > 500 else "")
            st.write(snippet)

            # Expandable section for full abstract
            with st.expander(f"Show full abstract for {doc_id}"):
                st.write(abstract)

            # Divider between results
            st.divider()
