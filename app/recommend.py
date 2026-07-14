from app.retriever import Retriever
from app.llm import ask_gemini
from app.prompts import SYSTEM_PROMPT

retriever = None


def get_retriever():
    global retriever

    if retriever is None:
        print("STEP 1 - Creating Retriever")
        retriever = Retriever()
        print("STEP 2 - Retriever Created")

    return retriever


def recommend(query: str):

    print("STEP 3 - recommend() called")

    retriever = get_retriever()

    print("STEP 4 - Searching")

    assessments = retriever.search(query)

    print(f"STEP 5 - Found {len(assessments)} assessments")

    if not assessments:
        return {
            "query": query,
            "recommendation": "No suitable SHL assessments were found.",
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

    print("STEP 6 - Calling Gemini")

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

    print("STEP 7 - Gemini completed")

    return {
        "query": query,
        "recommendation": recommendation,
        "assessments": top_assessments
    }