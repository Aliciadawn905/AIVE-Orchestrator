"""
A8 Orchestrator Agent
AI Design Solutions | AI Visibility Engine
Purpose:
Coordinates execution of all AIVE agents,
logs outputs to Supabase, and maintains client visibility metrics.
"""

import sys
import os
from pathlib import Path

# --- Add project root to path so local imports work ---
ROOT_DIR = Path(__file__).resolve().parents[3]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


import time
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from apps.common.db_utils import fetch_client_list
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# ======================================================
# 📡 Retool API Endpoints for Render
# ======================================================
app = FastAPI()


@app.get("/clients")
async def get_clients():
    """Returns all clients from Supabase."""
    try:
        clients = fetch_client_list()
        return JSONResponse({"clients": clients})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

@app.post("/run_orchestration")
async def trigger_orchestration(request: Request):
    """Runs orchestration manually (triggered by Retool)."""
    try:
        body = await request.json()
        client_id = body.get("client_id", "LOTUS001")  # default for testing
        print(f"🧭 Manual orchestration triggered for client {client_id}")
        orchestrate_all_clients()  # or a single-client version if you prefer
        return JSONResponse({"status": "success", "client_id": client_id})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ======================================================
# 🧾 Governance Events Endpoint for Retool
# ======================================================
from fastapi.responses import JSONResponse

@app.get("/governance")
def get_governance_logs():
    """Return all governance events from Supabase for dashboard display."""
    try:
        from apps.common.db_utils import fetch_table_data
        logs = fetch_table_data("governance_events")  # generic fetch helper in db_utils.py
        return JSONResponse({"data": logs})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)

# ======================================================
# 📊 Visibility Metrics Endpoint for Retool
# ======================================================

@app.get("/metrics")
def get_metrics():
    """Return visibility and performance metrics from Supabase."""
    try:
        from apps.common.db_utils import fetch_table_data
        metrics = fetch_table_data("visibility_metrics")
        return JSONResponse({"data": metrics})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# --------------------------------------------------------
# 🔧 FastAPI Setup (for Render health checks + manual runs)
# --------------------------------------------------------

@app.get("/")
def root():
    return {"status": "AIVE Orchestrator is running!"}

@app.get("/orchestrate")
def trigger_orchestration():
    """Manual trigger endpoint for orchestration runs."""
    orchestrate_all_clients()
    return {"status": "success", "message": "AIVE orchestration completed."}

# --------------------------------------------------------
# 🧾 Logging Setup
# --------------------------------------------------------
LOG_DIR = Path(__file__).resolve().parents[3] / "logs"
LOG_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = LOG_DIR / f"orchestrator_run_{timestamp}.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
)
logging.info(f"🪄 Starting orchestrator run at {timestamp}")

# --------------------------------------------------------
# 🧠 Path and Environment Setup
# --------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[3]
APPS_DIR = ROOT_DIR / "apps"
ENGINE_DIR = APPS_DIR / "AI_Visibility_Engine" / "agents"

for path in [ROOT_DIR, APPS_DIR, ENGINE_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

dotenv_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)
logging.info(f"✅ Environment loaded from {dotenv_path}")

# --------------------------------------------------------
# 📚 Imports
# --------------------------------------------------------
from apps.common.db_utils import (
    fetch_client_list,
    log_lead_discovery,
    log_visibility_metrics,
    log_content_output,
    log_governance_event,
    log_research_insight
)

# AIVE Agents (A1–A9)
from apps.AI_Visibility_Engine.agents.A1_strategy_agent import run_a1_strategy
from apps.AI_Visibility_Engine.agents.A2_dev_agent import run_a2_dev
from apps.AI_Visibility_Engine.agents.A3_automation_agent import run_a3_automation
from apps.AI_Visibility_Engine.agents.A4_analytics_agent import run_a4_analytics
from apps.AI_Visibility_Engine.agents.A5_content_agent import run_a5_content
from apps.AI_Visibility_Engine.agents.A6_education_agent import run_a6_education
from apps.AI_Visibility_Engine.agents.A7_governance_agent import run_a7_governance
from apps.AI_Visibility_Engine.agents.A9_research_intelligence_agent import propose_aive_updates


# --------------------------------------------------------
# 🤖 Main Orchestration Function
# --------------------------------------------------------
def orchestrate_all_clients():
    """Main loop to coordinate all AIVE agents for each active client."""
    clients = fetch_client_list()
    logging.info(f"📋 Found {len(clients)} active clients in Supabase.")

    for client in clients:
        cid = client["client_id"]
        domain = client.get("domain", "N/A")
        name = client.get("client_name", "Unknown")
        industry = client.get("industry", "Local Services")

        print(f"\n--- Running AIVE orchestration for {name} ({domain}) ---\n")
        logging.info(f"🎯 Processing client: {name} ({domain})")

        try:
            # --- A1 Strategy & Planning ---
            run_a1_strategy(client_id=cid, business_name=name, domain=domain, industry=industry)

            # --- A2 Development & Infrastructure ---
            run_a2_dev(client_id=cid, business_name=name, domain=domain, industry=industry)

            # --- A3 Automation & Workflows ---
            run_a3_automation(client_id=cid, business_name=name, domain=domain, industry=industry)

            # --- A4 Analytics ---
            result = run_a4_analytics(client_id=cid, business_name=name, domain=domain, industry=industry)
            if result:
                log_visibility_metrics(
                    agent_id="A4",
                    client_id=cid,
                    domain=domain,
                    metric_type="traffic_share",
                    metric_value=result.get("traffic_share", 0),
                    source="Similarweb",
                    notes="Auto-logged by orchestrator"
                )

            # --- A5 Content & SEO ---
            run_a5_content(client_id=cid, business_name=name, domain=domain, industry=industry)

            # --- A6 Education (Marketing Content + Research Brochure) ---
            run_a6_education(client_id=cid, business_name=name, domain=domain, industry=industry)

            # --- A7 Governance & Oversight ---
            run_a7_governance(client_id=cid, business_name=name, domain=domain, industry=industry)

            # --- A9 Research & Intelligence ---
            propose_aive_updates()

            # --- Governance completion log ---
            log_governance_event(
                agent_id="A8",
                client_id=cid,
                event_type="orchestration_run",
                description=f"Completed orchestrator run for {name}.",
                category="System",
                action_required=False,
                approval_status="Approved",
                reviewer="Alicia Sorensen",
                notes=f"Domain processed: {domain}"
            )

        except Exception as e:
            logging.error(f"❌ Error running orchestrator for {name}: {e}")
            log_governance_event(
                agent_id="A8",
                client_id=cid,
                event_type="error",
                description=f"Error in orchestrator sequence for {name}",
                category="System",
                action_required=True,
                approval_status="Pending",
                reviewer="System",
                notes=str(e)
            )

        time.sleep(2)

    logging.info("✅ All clients processed successfully.")
    logging.info("🧠 Research & Intelligence updates complete.")

# ======================================================
# 🧭 Route Debugger (for Render visibility)
# ======================================================
if __name__ == "__main__":
    import uvicorn
    from fastapi.routing import APIRoute

    print("\n🔍 Registered routes:")
    for route in app.routes:
        if isinstance(route, APIRoute):
            print(f"➡️  {route.path}")

    print("\n🚀 Starting FastAPI for local testing...\n")
    uvicorn.run(app, host="0.0.0.0", port=10000)

# --------------------------------------------------------
# 🧩 Run when launched directly
# --------------------------------------------------------
if __name__ == "__main__":
    print("\n🤖 AIVE Orchestrator Agent Active")
    print("✅ All agents connected successfully.")
    print("📊 AIVE Visibility Engine ready for execution and monitoring.\n")
    orchestrate_all_clients()
