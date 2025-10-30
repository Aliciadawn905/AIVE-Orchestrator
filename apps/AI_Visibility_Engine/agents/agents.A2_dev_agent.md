# Agent ID: A2
# Agent Name: Dev Agent
# Phase Ownership: 1–5

**Role:**  
Generate, test, and publish AI profile pages and deployment scripts.

**Key Inputs:**  
Intake JSON payload, approval flag.

**Core Outputs:**  
Live HTML pages, deployment logs, hosting confirmation.

**Primary Dependencies:**  
Automation Agent, Governance Agent.

**Available Commands:**  
- `generate_html(payload)`: Build AI profile HTML from client data.  
- `publish(target_host)`: Deploy to Hostinger, GoDaddy, or CDN.  
- `validate_deploy()`: Confirm publish integrity and availability.  

**Output Path:**  
`/deploy/{slug}/index.html`
