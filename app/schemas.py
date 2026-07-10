from typing import List

from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    query: str


class Assessment(BaseModel):
    name: str
    category: str
    score: float
    url: str


class RecommendationResponse(BaseModel):
    query: str
    recommendation: str
    assessments: List[Assessment]