from pydantic import BaseModel
from typing import Optional


class DetectionResult(BaseModel):
    disease: str
    confidence: float
    crop: str
    is_healthy: bool
    explanation: str


class RiskRequest(BaseModel):
    latitude: float
    longitude: float
    crop_type: str


class RiskResponse(BaseModel):
    risk_score: int
    risk_level: str
    reasons: list
    recommendation: str
    forecast_days: int


class ReportCreate(BaseModel):
    farmer_name: str
    latitude: float
    longitude: float
    crop_type: str
    disease: str
    confidence: float


class ReportOut(BaseModel):
    id: int
    farmer_name: str
    latitude: float
    longitude: float
    crop_type: str
    disease: str
    confidence: float
    created_at: str