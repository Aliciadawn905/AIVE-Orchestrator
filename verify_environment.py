import os
import importlib
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger

# --- Setup Logging ---
LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "environment_check.log"
logger.add(LOG_FILE, rotation="1 MB", retention="10 days")

print("\n🔍 Running AIVE Environment Verification...\n")

# --- Load environment variables ---
env_path = Path(__file__).parent / ".env"
if not env_path.exists():
    logger.error("❌ Missing .env file in project root.")
    print("❌ Missing .env file in project root.")
    exit(1)

load_dotenv(env_path)

# --- Expected environment variables ---
required_envs = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY"
]

missing_envs = [key for key in required_envs if not os.getenv(key)]
if missing_envs:
    for key in missing_envs:
        logger.error(f"❌ Missing environment variable: {key}")
        print(f"❌ Missing environment variable: {key}")
else:
    logger.info("✅ All required environment variables loaded.")
    print("✅ All required environment variables loaded.\n")

# --- Check imports for 9 agents ---
agents = [
    "apps.AI_Visibility_Engine.agents.A1_strategy_agent",
    "apps.AI_Visibility_Engine.agents.A2_dev_agent",
    "apps.AI_Visibility_Engine.agents.A3_automation_agent",
    "apps.AI_Visibility_Engine.agents.A4_analytics_agent",
    "apps.AI_Visibility_Engine.agents.A5_content_agent",
    "apps.AI_Visibility_Engine.agents.A6_education_agent",
    "apps.AI_Visibility_Engine.agents.A7_governance_agent",
    "apps.AI_Visibility_Engine.agents.A8_orchestrator_agent",
    "apps.AI_Visibility_Engine.agents.A9_research_intelligence_agent",
]


success = 0
for agent in agents:
    try:
        importlib.import_module(agent)
        logger.info(f"✅ Imported: {agent}")
        print(f"✅ {agent}")
        success += 1
    except Exception as e:
        logger.error(f"❌ Failed to import {agent}: {e}")
        print(f"❌ {agent}: {e}")

print(f"\n🧩 {success}/{len(agents)} agents imported successfully.\n")

# --- Check core dependencies ---
libs = ["supabase", "openai", "anthropic", "pandas", "requests", "httpx"]
for lib in libs:
    try:
        importlib.import_module(lib)
        logger.info(f"✅ Library loaded: {lib}")
        print(f"✅ {lib}")
    except Exception as e:
        logger.error(f"❌ Library failed: {lib} - {e}")
        print(f"❌ {lib} - {e}")

# --- Check Supabase connectivity ---
try:
    from supabase import create_client, Client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    data = supabase.table("clients").select("*").limit(1).execute()
    print("✅ Supabase connection successful.")
    logger.info("✅ Supabase connection successful.")
except Exception as e:
    print(f"⚠️ Supabase connection failed: {e}")
    logger.warning(f"⚠️ Supabase connection failed: {e}")

# --- Final Summary ---
print("\n🧠 Environment check complete.")
logger.info(f"Environment verification completed at {datetime.now()}.\n")
