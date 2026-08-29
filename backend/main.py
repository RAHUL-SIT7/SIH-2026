from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from remedies import get_remedy
from database import get_dashboard_stats
from database import init_db, insert_report, get_all_reports
from detection import classify_leaf_image
from risk_engine import calculate_outbreak_risk
from models import RiskRequest, RiskResponse, ReportCreate

app = FastAPI(
    title="Kisan Raksha Network API",
    description="SIH26131 — Predictive crop disease & pest early-warning system (demo)",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"status": "ok", "service": "Kisan Raksha Network API"}


@app.post("/detect", tags=["Detection"])
async def detect_disease(
    crop_type: str = Form(...),
    file: UploadFile = File(...),
):
    """Upload a leaf photo -> returns disease classification + explanation."""
    image_bytes = await file.read()
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty file uploaded")
    result = classify_leaf_image(image_bytes, crop_type)
    return result


@app.get("/remedy-lookup", tags=["Detection"])
def remedy_lookup(disease: str):
    """Look up full remedy info for a disease name — used when farmer
    manually confirms a match from the candidate images."""
    remedy = get_remedy(disease)
    is_healthy = "healthy" in disease.lower()
    return {
        "needs_retake": False,
        "disease": disease,
        "confidence": 0.75,
        "is_healthy": is_healthy,
        "remedy": None if is_healthy else remedy,
        "referral": None if is_healthy else remedy.get("referral"),
        "candidates": [],
    }


@app.post("/predict-risk", response_model=RiskResponse, tags=["Risk Engine"])
def predict_risk(req: RiskRequest):
    """The core differentiator: weather + community signals -> outbreak risk score."""
    result = calculate_outbreak_risk(req.latitude, req.longitude, req.crop_type)
    return result


@app.post("/community/report", tags=["Community"])
def create_report(report: ReportCreate):
    """Farmer submits a confirmed disease report -> feeds the community early-warning layer."""
    report_id = insert_report(
        report.farmer_name,
        report.latitude,
        report.longitude,
        report.crop_type,
        report.disease,
        report.confidence,
    )
    return {"id": report_id, "message": "Report added to community network"}



@app.get("/community/heatmap", tags=["Community"])
def heatmap():
    """All reports for map visualization on the frontend."""
    return get_all_reports()

@app.get("/admin/dashboard-data", tags=["Admin Dashboard"])
def dashboard_data():
    """Aggregated statistics for the agriculture officials dashboard."""
    return get_dashboard_stats()

# Serve the demo frontend (single-page app) at /app
app.mount("/app", StaticFiles(directory="../frontend", html=True), name="frontend")