"""
db_utils.py
Handles all database logging for AIVE Agents.
Updated to match Supabase schema (client_id = int8).
"""

from dotenv import load_dotenv
from pathlib import Path
import os
from datetime import datetime
from supabase import create_client, Client

# --- Load environment variables ---
# Go up two directories from /apps/common/ to reach project root
env_path = Path(__file__).resolve().parents[2] / ".env"
print(f"🔍 Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path)

# --- Verify env variables loaded ---
if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
    raise ValueError("❌ Could not load SUPABASE_URL or SUPABASE_KEY from .env")

# --- Initialize Supabase client ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def _timestamp():
    """UTC timestamp helper"""
    return datetime.utcnow().isoformat()


# --------------------------------------------------------------------
# 🧠 AGENT 1: Lead Discovery Agent
# --------------------------------------------------------------------
def log_lead_discovery(agent_id, client_id, lead_name, source, relevance_score, contact_info, notes):
    """Logs discovered leads to Supabase."""
    try:
        data = {
            "timestamp": _timestamp(),
            "agent_id": agent_id,
            "client_id": client_id,
            "lead_name": lead_name,
            "source": source,
            "relevance_score": relevance_score,
            "contact_info": contact_info,
            "notes": notes,
        }
        result = supabase.table("lead_data").insert(data).execute()
        print("📩 Supabase insert result:", result)
        return result
    except Exception as e:
        print("❌ Error logging lead:", e)
        return None

# --------------------------------------------------------------------
# 🌐 AGENT 4: Analytics Agent
# --------------------------------------------------------------------
def log_visibility_metrics(agent_id, client_id, domain, metric_type, metric_value, source, notes=None):
    """Tracks SEO, domain authority, or LLM search visibility data."""
    payload = {
        "timestamp": _timestamp(),
        "agent_id": agent_id,
        "client_id": client_id,   # int8 FK → clients(id)
        "domain": domain,
        "metric_type": metric_type,
        "metric_value": metric_value,
        "source": source,
        "notes": notes or "",
    }
    try:
        supabase.table("visibility_metrics").insert(payload).execute()
        print(f"📈 Metric logged: {metric_type}={metric_value} for {domain}")
    except Exception as e:
        print(f"❌ Error logging metric: {e}")

# --------------------------------------------------------------------
# ✍️ AGENT 5: Content Engine Agent
# --------------------------------------------------------------------
def log_content_output(agent_id, client_id, content_type, text, keywords, status, meta):
    """Logs generated content or social posts."""
    try:
        data = {
            "timestamp": _timestamp(),
            "agent_id": agent_id,
            "client_id": client_id,
            "content_type": content_type,
            "text": text,
            "keywords": keywords,
            "status": status,
            "meta": meta,
        }
        result = supabase.table("content_outputs").insert(data).execute()
        print(f"📝 Content logged: {content_type}")
        return result
    except Exception as e:
        print(f"❌ Error logging content: {e}")
        return None
# --------------------------------------------------------------------
# ✍️ AGENT 7: Governance Agent
# --------------------------------------------------------------------

def log_governance_event(agent_id, client_id, event_type, description, category, action_required, approval_status, reviewer, notes):
    """Logs governance or oversight actions (Agent A7)."""
    try:
        data = {
            "timestamp": _timestamp(),
            "agent_id": agent_id,
            "client_id": client_id,
            "event_type": event_type,
            "description": description,
            "category": category,
            "action_required": action_required,
            "approval_status": approval_status,
            "reviewer": reviewer,
            "notes": notes,
        }
        result = supabase.table("governance_events").insert(data).execute()
        print(f"🏛️ Governance event logged: {event_type} ({approval_status})")
        return result
    except Exception as e:
        print(f"❌ Error logging governance event: {e}")
        return None

# --------------------------------------------------------------------
# ✍️ AGENT 9: Research Intelligence Agent
# --------------------------------------------------------------------
def log_research_insight(agent_id, client_id, topic, insight, source, confidence, notes):
    """Logs AI-driven research or market insights."""
    try:
        data = {
            "timestamp": _timestamp(),
            "agent_id": agent_id,
            "client_id": client_id,
            "topic": topic,
            "insight": insight,
            "source": source,
            "confidence": confidence,
            "notes": notes,
        }
        result = supabase.table("research_insights").insert(data).execute()
        print(f"🔬 Research insight logged: {topic}")
        return result
    except Exception as e:
        print(f"❌ Error logging research insight: {e}")
        return None

# --------------------------------------------------------------------
# 📋 CLIENT FETCH UTILITY
# --------------------------------------------------------------------
def fetch_client_list():
    """Fetch all clients from the Supabase 'clients' table."""
    try:
        response = supabase.table("clients").select("*").execute()
        clients = response.data or []
        print(f"📋 Retrieved {len(clients)} clients from Supabase.")
        return clients
    except Exception as e:
        print(f"❌ Error fetching clients: {e}")
        return []


def log_recommendation(client_id: str, domain: str, recommendation: str, source: str = "A6", notes: str = ""):
    """
    Logs content or educational recommendations into the Supabase recommendations table.
    """
    print(f"📝 [DB] Logging recommendation for {domain}: {recommendation}")

    try:
        from common.supabase_client import supabase  # or adjust if you import differently
        data = {
            "client_id": client_id,
            "domain": domain,
            "recommendation": recommendation,
            "source": source,
            "notes": notes
        }
        supabase.table("recommendations").insert(data).execute()
        print("✅ Recommendation logged successfully.")
        return True
    except Exception as e:
        print(f"⚠️ Failed to log recommendation: {e}")
        return False
