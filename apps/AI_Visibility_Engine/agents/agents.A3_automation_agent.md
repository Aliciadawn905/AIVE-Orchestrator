# Agent ID: A3
# Agent Name: Automation Agent
# Phase Ownership: 1–5

**Role:**  
Automate workflows between intake, generation, approval, and publishing.

**Key Inputs:**  
Typeform/Cursor form data, client metadata.

**Core Outputs:**  
Normalized payloads, API triggers, automation logs.

**Primary Dependencies:**  
Dev Agent, Analytics Agent.

**Available Commands:**  
- `normalize_data()`: Clean and format client data into JSON.  
- `trigger_publish()`: Send publish request once approved.  
- `log_event(event)`: Record system automation activity.  

**Output Path:**  
`/data/intake/{client_id}.json`
