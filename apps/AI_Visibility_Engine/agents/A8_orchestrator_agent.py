"""
A8 Orchestrator Agent
AI Design Solutions | AI Visibility Engine
Purpose:
Coordinates execution of all AIVE agents,
logs outputs to Supabase, and maintains client visibility metrics.
"""

import sys
import os
import time
import logging
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI

# --------------------------------------------------------
# 🔧 FastAPI Setup (for Render health checks)
# --------------------------------------------------------
app = FastAPI()

@app.get("/")
def root():
    return {"status": "AIVE Orchestrator is running!"}

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
from apps.AI_Visibility_Engine.agents.A4_analytics_agent import run_analysis
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

        logging.info(f"🎯 Processing client: {name} ({domain})")

        try:
            # --- A1 Strategy & Planning ---
            run_a1_strategy(client_id=cid, domain=domain, industry=industry)

            # --- A2 Development & Infrastructure ---
            run_a2_dev(client_id=cid, domain=domain)

            # --- A3 Automation & Workflows ---
            run_a3_automation(client_id=cid, domain=domain)

            # --- A4 Analytics ---
            result = run_analysis(domain)
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
            run_a5_content(client_id=cid, domain=domain)

            # --- A6 Education (Marketing Content + Research Brochure) ---
            run_a6_education(
                client_id=cid,
                business_name=name,
                domain=domain,
                industry=industry
            )

            # --- A7 Governance & Oversight ---
            run_a7_governance(client_id=cid, domain=domain)

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


# --------------------------------------------------------
# 🧩 Run when launched directly
# --------------------------------------------------------
if __name__ == "__main__":
    print("\n🤖 AIVE Orchestrator Agent Active")
    print("✅ All agents connected successfully.")
    print("📊 AIVE Visibility Engine ready for execution and monitoring.\n")
    orchestrate_all_clients()
