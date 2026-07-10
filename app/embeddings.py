import json
from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG = BASE_DIR / "data" / "catalog.json"
OUTPUT = BASE_DIR / "data" / "embeddings.npy"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_catalog():
    with open(CATALOG, "r", encoding="utf-8") as f:
        return json.load(f)


def main():

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    catalog = load_catalog()

    texts = [item["embedding_text"] for item in catalog]

    print(f"Generating embeddings for {len(texts)} assessments...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    np.save(OUTPUT, embeddings)

    print()

    print("=" * 50)

    print("Embeddings generated successfully!")

    print(f"Shape : {embeddings.shape}")

    print(f"Saved : {OUTPUT}")


if __name__ == "__main__":
    main()