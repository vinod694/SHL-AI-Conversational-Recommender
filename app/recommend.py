from app.retriever import Retriever
from app.llm import ask_gemini
from app.prompts import SYSTEM_PROMPT

retriever = None

def get_retriever():
    global retriever

    if retriever is None:
        retriever = Retriever()

    return retriever


def recommend(query: str):

    retriever = get_retriever()

    assessments = retriever.search(query)

    if not assessments:
        return {
            "query": query,
            "recommendation": "No suitable SHL assessments were found for this job description.",
            "assessments": []
        }

    top_assessments = assessments[:3]

    context = ""

    for assessment in top_assessments:

        context += f"""
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
{SYSTEM_PROMPT}

Recruiter Request:

{query}

Available SHL Assessments:

{context}

Return recommendations ONLY using the assessments listed above.

For each assessment provide:

1. Why it is recommended
2. Skills evaluated
3. Official SHL URL

Do not invent assessments.
"""

    recommendation = ask_gemini(prompt)

    return {
        "query": query,
        "recommendation": recommendation,
        "assessments": top_assessments
    }


if __name__ == "__main__":

    print("=" * 80)
    print("SHL AI Assessment Recommendation System")
    print("=" * 80)

    while True:

        query = input("\nEnter Job Description ('exit' to quit): ")

        if query.lower() == "exit":
            print("\nGoodbye!")
            break

        print("\nSearching SHL Catalog...\n")

        result = recommend(query)

        print("=" * 80)
        print(result["recommendation"])
        print("=" * 80)