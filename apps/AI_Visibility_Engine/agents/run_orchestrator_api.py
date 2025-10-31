"""
run_orchestrator_api.py
Launches the AIVE Orchestrator as a FastAPI service for Render + Retool integration.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.common.db_utils import log_visibility_metrics, log_research_insight

from datetime import datetime

app = FastAPI(title="AIVE Orchestrator API", version="1.0")

# --- Allow Retool and your local dev environment ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For testing; restrict later to Retool domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "✅ AIVE Orchestrator API is running", "timestamp": datetime.utcnow()}

@app.get("/health")
def health_check():
    return {"status": "ok", "time": datetime.utcnow()}

@app.post("/log/visibility")
def log_visibility(agent_id: str, client_id: str, domain: str, metric_type: str, metric_value: float, source: str):
    """Test endpoint for logging visibility metrics"""
    result = log_visibility_metrics(agent_id, client_id, domain, metric_type, metric_value, source, notes="Test log via Render API")
    return {"status": "success", "details": str(result)}

@app.post("/log/research")
def log_research(agent_id: str, client_id: str, topic: str, insight: str, source: str):
    """Test endpoint for research insights"""
    result = log_research_insight(agent_id, client_id, topic, insight, source, confidence=0.95, notes="Logged via Render API")
    return {"status": "success", "details": str(result)}
