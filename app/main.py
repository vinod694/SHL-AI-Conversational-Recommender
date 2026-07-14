from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.recommend import recommend
from app.schemas import RecommendationRequest, RecommendationResponse

app = FastAPI(
    title="SHL Assessment Recommendation API",
    version="1.0.0",
    description="AI-powered SHL Assessment Recommendation System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "status": "running",
        "message": "SHL AI Recommendation API"
    }


@app.post(
    "/recommend",
    response_model=RecommendationResponse
)
def recommend_endpoint(request: RecommendationRequest):

    result = recommend(request.query)

    return RecommendationResponse(
        query=result["query"],
        recommendation=result["recommendation"],
        assessments=result["assessments"]
    )