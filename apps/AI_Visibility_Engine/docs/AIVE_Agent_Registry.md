# 🧠 AIVE Agent Registry

This registry defines the functional scope, inputs, outputs, and dependencies of each AIVE subsystem agent.  
Used by the A8 Orchestrator for task routing and logging.

---

## Agent ID: A1
**Name:** Strategy Agent  
**Role:** Product roadmap, pricing tiers, and feature evolution.  
**Outputs:** `/data/strategy/roadmap_{timestamp}.yaml`  
**Depends On:** Analytics (A4), Education (A6)

---

## Agent ID: A2
**Name:** Dev Agent  
**Role:** Generate, test, and publish AI profile pages and deployment scripts.  
**Outputs:** `/deploy/{slug}/index.html`  
**Depends On:** Automation (A3), Governance (A7)

---

## Agent ID: A3
**Name:** Automation Agent  
**Role:** Automate workflows between intake, generation, approval, and publishing.  
**Outputs:** `/data/intake/{client_id}.json`  
**Depends On:** Dev (A2), Analytics (A4)

---

## Agent ID: A4
**Name:** Analytics Agent  
**Role:** Track visibility metrics, LLM query results, and engagement data.  
**Outputs:** `/reports/weekly_digest.md`  
**Depends On:** Automation (A3), Strategy (A1)

---

## Agent ID: A5
**Name:** Content Agent  
**Role:** Create copy, educational PDFs, and visuals for the AI Visibility Engine.  
**Outputs:** `/content/{client_slug}/materials/`  
**Depends On:** Strategy (A1), Education (A6)

---

## Agent ID: A6
**Name:** Education Agent  
**Role:** Generate research-based marketing & educational materials (OpenAI integration).  
**Outputs:** `/content_outputs`, `/research_insights`  
**Depends On:** Analytics (A4), Research (A9)

---

## Agent ID: A7
**Name:** Governance Agent  
**Role:** Manage approvals, compliance, and oversight logs.  
**Outputs:** `/governance_events`  
**Depends On:** All agents for compliance visibility.

---

## Agent ID: A8
**Name:** Orchestrator Agent  
**Role:** Execute agents sequentially, manage logs, and ensure state integrity.  
**Outputs:** `/logs/orchestrator_run_{timestamp}.log`

---

## Agent ID: A9
**Name:** Research Intelligence Agent  
**Role:** Gather external competitive intelligence and trend data.  
**Outputs:** `/research_insights`  
**Depends On:** Analytics (A4), Education (A6)
