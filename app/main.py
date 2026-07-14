from fastapi import FastAPI
print("STEP 1 - FastAPI imported")

from fastapi.middleware.cors import CORSMiddleware
print("STEP 2 - CORSMiddleware imported")

from app.recommend import recommend
print("STEP 3 - recommend imported")

from app.schemas import RecommendationRequest, RecommendationResponse
print("STEP 4 - schemas imported")

print("Loaded schema:", RecommendationResponse.model_json_schema())

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0",
    description="AI-powered SHL Assessment Recommendation System"
)

print("STEP 5 - FastAPI app created")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("STEP 6 - Middleware added")


@app.get("/")
def home():
    print("GET / called")
    return {
        "status": "running",
        "message": "SHL AI Recommendation API"
    }


@app.post(
    "/recommend",
    response_model=RecommendationResponse
)
def recommend_endpoint(request: RecommendationRequest):

    print("STEP 7 - /recommend endpoint called")

    result = recommend(request.query)

    print("Recommendation Result:")
    print(result)

    return RecommendationResponse(
        query=result["query"],
        recommendation=result["recommendation"],
        assessments=result["assessments"]
    )


print("STEP 8 - main.py loaded successfully")