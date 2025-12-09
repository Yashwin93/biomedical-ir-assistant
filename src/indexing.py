import os
import json
import tarfile
import requests
import pandas as pd
import pyterrier as pt
from bs4 import BeautifulSoup
from .utils import path   # your helper for absolute paths

# --- Step 1: Initialize PyTerrier ---
def init_pyterrier():
    import pyterrier as pt
    if not pt.java.started():
        pt.java.init()

# --- Step 2: Download PMC OA tar.gz ---
def download_pmc(url, out_path="data/pmc_oa.tar.gz"):
    os.makedirs("data", exist_ok=True)
    r = requests.get(url, stream=True)
    with open(path(out_path), "wb") as f:
        f.write(r.content)
    print(f"✅ Downloaded {out_path}")

# --- Step 3: Extract XML files ---
def extract_pmc(tar_path="data/pmc_oa.tar.gz", extract_dir="data/xml"):
    os.makedirs(path(extract_dir), exist_ok=True)
    with tarfile.open(path(tar_path), "r:gz") as tar:
        tar.extractall(path(extract_dir))
    print(f"✅ Extracted files into {extract_dir}")

# --- Step 4: Parse XML into JSON ---
def parse_pmc_xml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "lxml")
        title = soup.find("article-title").get_text(" ", strip=True) if soup.find("article-title") else ""
        abstract = " ".join([p.get_text(" ", strip=True) for p in soup.find_all("abstract")])
        body = " ".join([p.get_text(" ", strip=True) for p in soup.find_all("p")])
        return {"title": title, "abstract": abstract, "body": body}
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

def build_json(xml_dir="data/xml", out_file="data/pmc_subset.json"):
    docs = []
    for root, _, files in os.walk(path(xml_dir)):
        for file in files:
            if file.endswith(".xml"):
                parsed = parse_pmc_xml(os.path.join(root, file))
                if parsed and (parsed["title"] or parsed["abstract"] or parsed["body"]):
                    docs.append(parsed)
    with open(path(out_file), "w", encoding="utf-8") as f:
        json.dump(docs, f, indent=2)
    print(f"✅ Parsed {len(docs)} documents into {out_file}")
    return out_file

# --- Step 5: Build Terrier index ---
def build_index(json_file="data/pmc_subset.json", index_dir="index_dir"):
    init_pyterrier()
    with open(path(json_file), "r", encoding="utf-8") as f:
        docs = json.load(f)

    docs_df = pd.DataFrame([
        {
            "docno": f"doc{i}",
            "title": d.get("title", ""),
            "abstract": d.get("abstract", ""),
            "body": d.get("body", ""),
            "text": (d.get("title","") + " " + d.get("abstract","") + " " + d.get("body","")).strip()
        }
        for i, d in enumerate(docs)
    ])

    indexer = pt.IterDictIndexer(path(index_dir), meta={'docno': 20, 'title': 256, 'abstract': 2048})
    index_ref = indexer.index(docs_df.to_dict(orient="records"))
    print(f"✅ Indexed {len(docs_df)} documents into {index_dir}")
    return index_ref

# --- Step 6: Orchestrate everything ---
def run_pipeline():
    url = "https://ftp.ncbi.nlm.nih.gov/pub/pmc/oa_bulk/oa_comm/xml/oa_comm_xml.incr.2025-10-01.tar.gz"
    download_pmc(url)
    extract_pmc()
    json_file = build_json()
    build_index(json_file)

if __name__ == "__main__":
    run_pipeline()

