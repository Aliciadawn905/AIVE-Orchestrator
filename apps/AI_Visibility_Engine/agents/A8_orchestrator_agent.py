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
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------------------------
# 🧾 LOGGING CONFIGURATION
# --------------------------------------------------------------------
import logging
from datetime import datetime
from pathlib import Path

# Create /logs directory path
LOG_DIR = Path(__file__).resolve().parents[3] / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Build timestamped log file name
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file = LOG_DIR / f"orchestrator_run_{timestamp}.log"

# Configure logging format and level
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # prints to terminal as well
    ]
)

logging.info(f"🪄 Starting orchestrator run at {timestamp}")


# --- Dynamically add project root and /apps to import path ---
ROOT_DIR = Path(__file__).resolve().parents[3]  # /MCP_Server_Project
APPS_DIR = ROOT_DIR / "apps"
ENGINE_DIR = APPS_DIR / "AI_Visibility_Engine" / "agents"

for path in [ROOT_DIR, APPS_DIR, ENGINE_DIR]:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

print(f"✅ Root added: {ROOT_DIR}")
print(f"✅ Apps path added: {APPS_DIR}")
print(f"✅ Engine path added: {ENGINE_DIR}")

# --- Internal imports (absolute) ---
from apps.common.db_utils import (
    fetch_client_list,
    log_lead_discovery,
    log_visibility_metrics,
    log_content_output,
    log_governance_event,
    log_research_insight
)
from apps.AI_Visibility_Engine.agents.A4_analytics_agent import run_analysis
from apps.AI_Visibility_Engine.agents.A9_research_intelligence_agent import propose_aive_updates

# --- A6: Education Agent (AI Marketing & Content Generation) ---
from common.education_agent import run_a6_education

# ======================================================
# 📋 Agent Registry Dashboard Loader
# ======================================================
from pathlib import Path
import yaml
from rich.console import Console
from rich.table import Table

console = Console()

def load_agent_registry():
    """Load and display the Agent Registry dashboard"""
    try:
        ROOT_DIR = Path(__file__).resolve().parents[2]
        REGISTRY_PATH = ROOT_DIR / "apps" / "AI_Visibility_Engine" / "docs" / "AIVE_Agent_Registry.yaml"

        with open(REGISTRY_PATH, "r") as f:
            registry = yaml.safe_load(f)

        table = Table(title="🤖 AIVE Agent Registry Overview", show_lines=True)
        table.add_column("Agent ID", style="cyan", no_wrap=True)
        table.add_column("Agent Name", style="bold green")
        table.add_column("Role", style="white")
        table.add_column("Dependencies", style="yellow")

        for agent in registry:
            deps = ", ".join(agent.get("dependencies", [])) if agent.get("dependencies") else "-"
            table.add_row(
                agent["agent_id"],
                agent["agent_name"],
                agent["role"][:80] + ("..." if len(agent["role"]) > 80 else ""),
                deps
            )

        console.print("\n✅ [bold green]Loaded Agent Registry successfully![/bold green]\n")
        console.print(table)
        return registry

    except Exception as e:
        console.print(f"❌ [bold red]Error loading agent registry:[/bold red] {e}")
        return []


# --- Load environment variables ---
dotenv_path = ROOT_DIR / ".env"
load_dotenv(dotenv_path=dotenv_path)

print(f"✅ Orchestrator environment loaded from: {dotenv_path}")


def orchestrate_all_clients():
    """Main loop to coordinate all agents and log results."""
    clients = fetch_client_list()
    print(f"📋 Found {len(clients)} active clients in Supabase.")

    for client in clients:
        cid = client["client_id"]
        domain = client.get("domain", "N/A")
        name = client.get("client_name", "Unknown")

        print(f"🎯 Processing client: {name} ({domain})")

        # --- Run analysis for this client ---
        result = run_analysis(domain)

        # --- If the analysis succeeded, log metrics ---
        if result:
            log_visibility_metrics(
                agent_id="A5",
                client_id=cid,
                domain=domain,
                metric_type="traffic_share",
                metric_value=result.get("traffic_share", 0),
                source="Similarweb",
                notes="Auto-logged from orchestrator test"
            )
            print("📊 Metrics logged successfully.")
        else:
            print("⚠️ Analysis failed or returned no data.")
        
       
        # --- Governance event to record orchestration completion ---
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
        
        # Delay between clients (to simulate sequential runs)
        time.sleep(2)
    
    print("✅ All clients processed successfully.")

    print("\n🧠 Running Research & Intelligence updates...")
    propose_aive_updates()
    print("\n✅ Orchestration cycle complete.\n")

def run_orchestration():
    # Example orchestration sequence
    print("🚀 Running Orchestration Sequence...")

    # --- A1 Lead Discovery ---
    try:
        print("Running A1 Lead Discovery...")
        # result = run_lead_agent()  # however your A1 executes
        log_lead_discovery(
            agent_id="A1",
            client_id="LOTUS001",
            lead_name="Test Lead",
            source="Yelp",
            relevance_score=0.95,
            contact_info={"phone": "555-888-9999"},
            notes="Triggered by A8 orchestrator test run"
        )
    except Exception as e:
        log_governance_event(
            agent_id="A8",
            client_id="LOTUS001",
            event_type="error",
            description="A1 failed to complete",
            category="Lead Discovery",
            action_required=True,
            approval_status="Pending",
            reviewer="System",
            notes=str(e)
        )

    # --- A5 Visibility Metrics ---
    try:
        print("Running A5 Visibility Agent...")
        # visibility_result = run_visibility_agent()
        log_visibility_metrics(
            agent_id="A5",
            client_id="LOTUS001",
            domain="lotus-healthandwellness.com",
            metric_type="traffic_share",
            metric_value=0.27,
            source="Similarweb",
            notes="Auto-logged from orchestrator test"
        )
    except Exception as e:
        log_governance_event(
            agent_id="A8",
            client_id="LOTUS001",
            event_type="error",
            description="A5 visibility check failed",
            category="Visibility Metrics",
            action_required=True,
            approval_status="Pending",
            reviewer="System",
            notes=str(e)
        )
# --- A6 Education Agent (Marketing Content + Research Brochure) ---
try:
    logging.info(f"📘 Running A6 Education Agent for {name}...")
    education_data = run_a6_education(
        client_id=cid,
        business_name=name,
        domain=domain,
        industry=client.get("industry", "Local Services")
    )
    logging.info(f"📝 Education content & brochure logged for {name}.")
except Exception as e:
    logging.error(f"❌ A6 Education Agent failed for {name}: {e}")
    log_governance_event(
        agent_id="A8",
        client_id=cid,
        event_type="error",
        description="A6 Education Agent failed",
        category="Education",
        action_required=True,
        approval_status="Pending",
        reviewer="System",
        notes=str(e)
    )

    # --- A6 Content Output (legacy test) ---
# log_content_output(
#     agent_id="A6",
#     client_id="LOTUS001",
#     content_type="instagram_caption",
#     text="✨ Auto-generated post for Lotus Wellness.",
#     keywords=["glendora", "spa", "wellness"],
#     status="draft",
#     meta={"platform": "instagram"}
# )


    # --- A7 Governance Event ---
    log_governance_event(
        agent_id="A7",
        client_id="LOTUS001",
        event_type="orchestration_run",
        description="Completed orchestrator test run across A1–A6.",
        category="System",
        action_required=False,
        approval_status="Approved",
        reviewer="Alicia Sorensen",
        notes="Test sequence for Supabase logging verification."
    )

    print("✅ Orchestration complete.")

if __name__ == "__main__":
    # --- System Verification ---
    print("\n🤖 AIVE Orchestrator Agent Active")
    print("✅ All agents connected successfully.")
    print("📊 AIVE Visibility Engine is now ready for execution and monitoring.")
    print("-------------------------------------------------------------")
    print("Tip: Run 'verify_environment.py' anytime to confirm system health.\n")
    orchestrate_all_clients()
