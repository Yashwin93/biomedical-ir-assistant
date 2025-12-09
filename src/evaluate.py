"""
File: evaluate.py
Purpose: Evaluate BM25, RM3, and MeSH pipelines using standard IR metrics.
Generates evaluation results (MAP, Precision@10, nDCG@10) and saves them to CSV,
with a bar chart visualization comparing system performance.
"""

import pandas as pd
import pyterrier as pt
import matplotlib.pyplot as plt
from ir_measures import MAP, P, nDCG
from .main import load_index, bm25_pipeline, rm3_pipeline, expand_with_mesh

# --- Initialize PyTerrier ---
# Ensures Terrier IR platform is ready before running experiments
if not pt.started():
    pt.init()

def mesh_pipeline_eval(index):
    """
    Define MeSH expansion pipeline for evaluation.
    Expands query terms using MeSH synonyms before applying BM25.

    Args:
        index (pt.Index): Terrier index object.

    Returns:
        pt.Pipeline: Query expansion pipeline with BM25 retrieval.
    """
    bm25 = bm25_pipeline(index)
    # Expand query with MeSH terms before BM25
    return pt.apply.query(lambda q: q["query"] + " " + " ".join(expand_with_mesh(q["query"]))) >> bm25

def evaluate_systems(queries, qrels):
    """
    Evaluate BM25, RM3, and MeSH pipelines using standard IR metrics.

    Args:
        queries (pd.DataFrame): DataFrame with columns ['qid','query'].
        qrels (pd.DataFrame): DataFrame with columns ['qid','docno','label'].

    Returns:
        pd.DataFrame: Evaluation results with metrics for each pipeline.
    """
    index = load_index("index_dir")
    bm25 = bm25_pipeline(index)
    rm3 = rm3_pipeline(index)
    mesh = mesh_pipeline_eval(index)

    # Ensure qid types match across queries and qrels
    queries["qid"] = queries["qid"].astype(str)
    qrels["qid"] = qrels["qid"].astype(str)

    # Run experiment with three pipelines and standard IR metrics
    results = pt.Experiment(
        [bm25, rm3, mesh],
        queries,
        qrels,
        eval_metrics=[MAP, P@10, nDCG@10]
    )
    return results

if __name__ == "__main__":
    # --- Load queries and qrels from files ---
    queries = pd.read_csv("data/queries.csv")
    qrels = pd.read_csv("data/qrels_completed.csv")

    # Run evaluation across BM25, RM3, and MeSH pipelines
    results = evaluate_systems(queries, qrels)

    # Map system names to cleaner labels for readability
    name_map = {
        "TerrierRetr(BM25)": "BM25",
        "(TerrierRetr(BM25) >> QueryExpansion(C:\\Users\\yashw\\biomedical-ir-assistant\\index_dir/data.properties,3,10,<org.terrier.querying.RM3 at 0x...>)) >> TerrierRetr(BM25)": "RM3",
        "(pt.apply.query() >> TerrierRetr(BM25))": "MeSH"
    }

    # Replace names in results DataFrame
    results["name"] = results["name"].map(lambda x: name_map.get(x, x))

    # Save results to CSV
    results.to_csv("results/evaluation_metrics.csv", index=False)
    print("✅ Saved results to results/evaluation_metrics.csv")

    # --- Visualization of metrics ---
    metrics = ["AP", "P@10", "nDCG@10"]
    systems = results["name"].tolist()
    scores = [results[metric].tolist() for metric in metrics]

    x = range(len(metrics))
    width = 0.25

    plt.figure(figsize=(10,6))
    for i, system in enumerate(systems):
        # Plot bar chart for each system across metrics
        plt.bar([p + width*i for p in x], scores[i], width=width, label=system)

    plt.xticks([p + width for p in x], metrics)
    plt.ylabel("Score")
    plt.title("Biomedical IR Evaluation: BM25 vs RM3 vs MeSH")
    plt.legend()
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig("results/evaluation_chart.png")
    plt.show()
