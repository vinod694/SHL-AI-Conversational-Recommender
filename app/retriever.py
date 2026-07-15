import json
import re
from pathlib import Path

from app.llm import ask_gemini

BASE_DIR = Path(__file__).resolve().parent.parent
CATALOG_FILE = BASE_DIR / "data" / "catalog.json"


class Retriever:

    def __init__(self):

        print("Loading catalog...")

        with open(CATALOG_FILE, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

        print(f"Loaded {len(self.catalog)} assessments.")

    def extract_keywords(self, query: str):

        prompt = f"""
Extract only the important hiring keywords from this job description.

Return ONLY comma-separated keywords.

Job Description:
{query}
"""

        response = ask_gemini(prompt)

        keywords = [
            k.strip().lower()
            for k in response.split(",")
            if k.strip()
        ]

        return keywords

    def score_assessment(self, assessment, keywords):

        score = 0

        title = assessment.get("name", "").lower()
        category = assessment.get("category", "").lower()
        description = assessment.get("description", "").lower()

        for keyword in keywords:

            keyword = re.escape(keyword)

            if re.search(keyword, title):
                score += 5

            if re.search(keyword, category):
                score += 3

            if re.search(keyword, description):
                score += 1

        return score

    def search(self, query, top_k=3):

        print("Extracting keywords...")

        keywords = self.extract_keywords(query)

        print("Keywords:", keywords)

        scored = []

        for assessment in self.catalog:

            score = self.score_assessment(
                assessment,
                keywords
            )

            if score > 0:

                item = assessment.copy()
                item["score"] = score

                scored.append(item)

        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scored[:top_k]