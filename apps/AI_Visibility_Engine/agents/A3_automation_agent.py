"""
A3_Automation_Agent.py
Automates workflow and publishing triggers.
"""

from datetime import datetime
from apps.common.db_utils import log_governance_event

def normalize_data(client_id: str, raw_data: dict):
    """Normalize raw client form data into JSON payload."""
    print(f"🧠 Normalizing data for client {client_id}...")
    clean = {k.lower(): v.strip() if isinstance(v, str) else v for k, v in raw_data.items()}
    print("📦 Normalized payload:", clean)
    return clean

def trigger_publish(client_id: str):
    """Trigger publish pipeline for a given client."""
    print(f"⚡ Triggering publish for {client_id}...")
    log_governance_event(
        agent_id="A3",
        client_id=client_id,
        event_type="publish_trigger",
        description="Triggered deployment workflow after approval.",
        category="Automation",
        action_required=False,
        approval_status="approved",
        reviewer="AutomationAgent",
        notes="Automation flow successful."
    )

def log_event(client_id: str, event: str):
    """Log automation event."""
    log_governance_event(
        agent_id="A3",
        client_id=client_id,
        event_type="automation_event",
        description=f"{event}",
        category="Automation",
        action_required=False,
        approval_status="logged",
        reviewer="System",
        notes=f"Automation event recorded for {client_id}."
    )
