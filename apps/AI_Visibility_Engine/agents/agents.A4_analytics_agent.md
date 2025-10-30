# Agent ID: A4
# Agent Name: Analytics Agent
# Phase Ownership: 1–5

**Role:**  
Track visibility metrics, LLM query results, and engagement data.

**Key Inputs:**  
GA4 data, LLM query logs, baseline test results.

**Core Outputs:**  
Weekly and monthly reports, proof metric data, visibility deltas.

**Primary Dependencies:**  
Automation Agent, Strategy Agent.

**Available Commands:**  
- `track_metrics()`: Aggregate GA4 + query log data.  
- `calculate_visibility()`: Compute visibility delta vs baseline.  
- `generate_report()`: Write weekly_digest.md and monthly_summary.csv.  

**Output Path:**  
`/reports/weekly_digest.md`
