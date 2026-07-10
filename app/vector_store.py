import json
from pathlib import Path

import faiss
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_FILE = BASE_DIR / "data" / "catalog.json"
EMBEDDINGS_FILE = BASE_DIR / "data" / "embeddings.npy"
INDEX_FILE = BASE_DIR / "data" / "faiss.index"


def main():

    embeddings = np.load(EMBEDDINGS_FILE).astype("float32")

    print(f"Loaded embeddings: {embeddings.shape}")

    dimension = embeddings.shape[1]

    # Cosine similarity (works because embeddings are normalized)
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    faiss.write_index(index, str(INDEX_FILE))

    print("=" * 50)
    print("FAISS index created successfully!")
    print(f"Dimension : {dimension}")
    print(f"Vectors   : {index.ntotal}")
    print(f"Saved To  : {INDEX_FILE}")


if __name__ == "__main__":
    main()