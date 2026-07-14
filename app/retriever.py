import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).resolve().parent.parent

CATALOG_FILE = BASE_DIR / "data" / "catalog.json"
INDEX_FILE = BASE_DIR / "data" / "faiss.index"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

TOP_K = 3
SIMILARITY_THRESHOLD = 0.15


class Retriever:

    def __init__(self):

        print("STEP A - Starting Retriever")

        print("STEP B - Loading SentenceTransformer")
        self.model = SentenceTransformer(MODEL_NAME)
        print("STEP C - SentenceTransformer Loaded")

        print("STEP D - Loading catalog")
        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)
        print("STEP E - Catalog Loaded")

        print("STEP F - Loading FAISS")
        self.index = faiss.read_index(str(INDEX_FILE))
        print("STEP G - FAISS Loaded")

        print("Retriever Ready")

    def search(self, query, top_k=TOP_K):

        print("STEP H - Encoding Query")

        query_embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        ).astype("float32")

        print("STEP I - Query Encoded")

        distances, indices = self.index.search(
            np.array([query_embedding]),
            top_k
        )

        print("STEP J - FAISS Search Complete")

        results = []

        for score, idx in zip(distances[0], indices[0]):

            if idx == -1:
                continue

            if score < SIMILARITY_THRESHOLD:
                continue

            assessment = self.catalog[idx].copy()
            assessment["score"] = round(float(score), 4)

            results.append(assessment)

        print(f"STEP K - Returning {len(results)} results")

        return results