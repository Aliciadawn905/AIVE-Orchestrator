# Agent ID: A1
# Agent Name: Strategy Agent
# Phase Ownership: 1–5

**Role:**  
Product roadmap, pricing tiers, and feature evolution.

**Key Inputs:**  
Market research data, analytics summaries.

**Core Outputs:**  
Roadmap updates, tiered pricing model.

**Primary Dependencies:**  
Analytics Agent, Education Agent.

**Available Commands:**  
- `analyze_market()`: Review visibility trends and competitor data.  
- `update_roadmap()`: Push versioned roadmap to /config/AVE_state.yaml.  
- `define_tiers()`: Generate new tier descriptions and price matrix.  

**Output Path:**  
`/data/strategy/roadmap_{timestamp}.yaml`
