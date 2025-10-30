import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# --- Load .env file robustly no matter where the script is run ---
base_dir = Path(__file__).resolve().parents[3]  # go up to project root
dotenv_path = base_dir / ".env"
load_dotenv(dotenv_path=dotenv_path)

print(f"✅ Loaded environment from: {dotenv_path}")
print(f"🌐 MCP_BASE_URL = {os.getenv('MCP_BASE_URL')}")


def run_analysis(target_url):
    headers = {"Authorization": f"Bearer {os.getenv('MCP_TOKEN')}"}
    body = {"url": target_url}
    r = requests.post(f"{os.getenv('MCP_BASE_URL')}/tools/analyzeSEO", json=body, headers=headers)
    data = r.json()

    if r.status_code == 200:
        print("✅ Analysis complete.")
        print(data)
        return data
    else:
        print("❌ Error:", data)
        return None

# Example test
if __name__ == "__main__":
    run_analysis("https://lotushealthandwellness.net")
