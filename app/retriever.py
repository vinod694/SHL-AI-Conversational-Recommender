import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ==========================================================
# Paths
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_FILE = BASE_DIR / "data" / "catalog.json"
INDEX_FILE = BASE_DIR / "data" / "faiss.index"

# ==========================================================
# Configuration
# ==========================================================

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 5

SIMILARITY_THRESHOLD = 0.15

DEBUG = True


class Retriever:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
    MODEL_NAME,
    local_files_only=True
)

        print("Loading catalog...")

        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        print("Loading FAISS index...")

        self.index = faiss.read_index(str(INDEX_FILE))

        print("\nRetriever Ready!\n")

    def search(self, query, top_k=TOP_K):

        # ----------------------------------------
        # Convert query into embedding
        # ----------------------------------------

        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        # ----------------------------------------
        # Search FAISS
        # ----------------------------------------

        distances, indices = self.index.search(
            np.array([query_embedding]),
            top_k
        )

        results = []

        # ----------------------------------------
        # Process Results
        # ----------------------------------------

        for score, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            if DEBUG:
                print(
                    f"Raw Score: {score:.4f} | "
                    f"{self.catalog[idx]['name']}"
                )

            if score < SIMILARITY_THRESHOLD:
                continue

            assessment = self.catalog[idx].copy()

            assessment["score"] = round(float(score), 4)

            results.append(assessment)

        return results


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    retriever = Retriever()

    while True:

        print("=" * 70)

        query = input(
            "\nEnter your query ('exit' to quit): "
        )

        if query.lower() == "exit":
            break

        print()

        results = retriever.search(query)

        print()

        if not results:

            print("❌ No relevant assessments found.")
            print(
                "Try using different keywords.\n"
            )

            continue

        print("=" * 70)

        print(
            f"Top {len(results)} Matching Assessments\n"
        )

        for i, item in enumerate(results, start=1):

            print(f"{i}. {item['name']}")

            print(f"Score      : {item['score']}")

            print(f"Category   : {item['category']}")

            print(f"URL        : {item['url']}")

            print("-" * 70)