# Agent ID: A8
# Agent Name: Orchestrator Agent
# Phase Ownership: 1–5

**Role:**  
Coordinate all other agents, manage dependencies, and oversee phase transitions.

**Key Inputs:**  
AVE_state.yaml, task events, logs.

**Core Outputs:**  
Alerts, progress summaries, dispatch commands, phase transitions.

**Primary Dependencies:**  
All Agents.

**Available Commands:**  
- `manage_agents()`: Activate/suspend agents by phase.  
- `update_state()`: Write to /config/AVE_state.yaml.  
- `dispatch_alerts()`: Notify owner or governance of issues.  
- `transition_phase()`: Move workflow to next lifecycle stage.  

**Output Path:**  
`/reports/orchestrator_status.log`

| Step | Function                   | Description                                                    |
| ---- | -------------------------- | -------------------------------------------------------------- |
| 1️⃣  | `fetch_client_list()`      | Pulls your active client list from Supabase.                   |
| 2️⃣  | `run_analysis()`           | Calls your A4 Analytics Agent for each client site.            |
| 3️⃣  | `log_visibility_metrics()` | Inserts metrics into your Supabase `visibility_metrics` table. |
| 4️⃣  | `log_recommendation()`     | Logs AI-generated suggestions to `recommendations`.            |
| 5️⃣  | `propose_aive_updates()`   | Calls the A9 Research Agent for periodic learning cycles.      |
