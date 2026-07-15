import json
from pathlib import Path

from app.llm import ask_gemini

BASE_DIR = Path(__file__).resolve().parent.parent
CATALOG_FILE = BASE_DIR / "data" / "catalog.json"


def recommend(query: str):

    with open(CATALOG_FILE, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    catalog_text = ""

    for assessment in catalog:

        catalog_text += f"""
Assessment Name:
{assessment["name"]}

Category:
{assessment["category"]}

Description:
{assessment["description"]}

URL:
{assessment["url"]}

----------------------------------------
"""

    prompt = f"""
You are an SHL Assessment Recommendation Expert.

A recruiter wants to hire for the following role:

{query}

Below is the complete SHL Assessment Catalog.

{catalog_text}

Your task:

1. Select the THREE most suitable assessments.
2. Give an overall recommendation.
3. Assign each assessment a confidence score between 0 and 1.
4. Use ONLY assessments listed in the catalog.
5. Do NOT invent assessments.

Return ONLY valid JSON in this EXACT format:

{{
  "recommendation": "Overall recommendation",

  "selected": [
    {{
      "name": "Assessment Name",
      "score": 0.98
    }},
    {{
      "name": "Assessment Name",
      "score": 0.95
    }},
    {{
      "name": "Assessment Name",
      "score": 0.90
    }}
  ]
}}
"""

    response = ask_gemini(prompt)

    # Remove markdown if Gemini returns ```json ... ```
    response = response.strip()

    if response.startswith("```json"):
        response = response.replace("```json", "", 1)

    if response.startswith("```"):
        response = response.replace("```", "", 1)

    if response.endswith("```"):
        response = response[:-3]

    response = response.strip()

    try:
        result = json.loads(response)

    except Exception:

        return {
            "query": query,
            "recommendation": response,
            "assessments": []
        }

    selected = result.get("selected", [])

    selected_map = {}

    for item in selected:

        selected_map[item["name"]] = item["score"]

    matched = []

    for assessment in catalog:

        if assessment["name"] in selected_map:

            matched.append(
                {
                    "name": assessment["name"],
                    "category": assessment["category"],
                    "score": float(selected_map[assessment["name"]]),
                    "url": assessment["url"],
                }
            )

    # Highest confidence first
    matched.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return {
        "query": query,
        "recommendation": result["recommendation"],
        "assessments": matched,
    }


if __name__ == "__main__":

    while True:

        query = input("\nEnter Job Description ('exit' to quit): ")

        if query.lower() == "exit":
            break

        result = recommend(query)

        print("\n")
        print("=" * 80)
        print(result["recommendation"])
        print("=" * 80)

        for assessment in result["assessments"]:

            print(f"\nName      : {assessment['name']}")
            print(f"Category  : {assessment['category']}")
            print(f"Score     : {assessment['score']}")
            print(f"URL       : {assessment['url']}")