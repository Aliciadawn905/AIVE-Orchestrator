# 🚀 AI Visibility Engine (AVE) — Quickstart Guide

> **Author:** Alicia Sorensen, AI Design Solutions  
> **System:** AI Visibility Engine (AVE)  
> **Purpose:** Enable small & local businesses to become visible and cited in AI model search (ChatGPT, Claude, Perplexity, Gemini, etc.)

---

## 🧩 1. Folder Structure Overview

```
ai-visibility-engine/
├── agents/
│   ├── agents.A1_strategy_agent.md
│   ├── agents.A2_dev_agent.md
│   ├── agents.A3_automation_agent.md
│   ├── agents.A4_analytics_agent.md
│   ├── agents.A5_content_agent.md
│   ├── agents.A6_education_agent.md
│   ├── agents.A7_governance_agent.md
│   └── agents.A8_orchestrator_agent.md
│
├── config/
│   └── AVE_state.yaml
│
├── data/
│   ├── intake/
│   ├── reports/
│   ├── logs/
│   └── metrics/
│
└── docs/
    ├── AI_Visibility_Engine_PRD.md
    ├── Orchestrator_Brief.md
    ├── Proof_Metric_Framework.md
    └── Agent_Role_Overview.md
```

✅ *If you don’t see `/data/` folders yet, you can create them manually.*

---

## ⚙️ 2. Configuration File

Your `config/AVE_state.yaml` defines which agents are active, what phase the system is in, and whether human approval is required before publishing.

```yaml
phase: 1
human_approval_flag: true
active_agents:
  - dev
  - automation
  - analytics
owner: alicia@aidesignsolutions.net
cron:
  weekly_digest: true
  monthly_summary: true
```

---

## 🧠 3. Agent System Overview

Each agent in `/agents/` is a modular markdown file containing:
- **Role** — the agent’s purpose  
- **Inputs/Outputs** — expected data and deliverables  
- **Commands** — executable functions (`generate()`, `publish()`, etc.)  
- **Output Path** — where results are written  

The **Orchestrator Agent (A8)** reads the `.md` files and coordinates all others using events and shared files.

---

## ▶️ 4. First Test Run (MVP Mode)

1. Create your first client intake file:

   **`/data/intake/lotus_health.json`**
   ```json
   {
     "client_id": "lotus001",
     "business_name": "Lotus Health & Wellness",
     "services": ["Massage Therapy", "Acupuncture", "Skin Care"],
     "faqs": ["What should I expect during my first visit?", "Can I combine services?"],
     "why_choose": ["Award-winning care", "Integrative wellness"],
     "cta_url": "https://lotus-healthandwellness.square.site/"
   }
   ```

2. Open your Cursor console and trigger the first workflow:
   ```bash
   cursor.api.trigger('intake_received', client='lotus001')
   ```

3. The following sequence will begin automatically:
   - A3 Automation Agent normalizes data → writes `/data/intake/lotus001.json`
   - A2 Dev Agent generates landing page HTML in `/deploy/lotus-health-wellness/`
   - A4 Analytics Agent attaches GA4 + LLM tracking scripts
   - A8 Orchestrator notifies you when it’s ready for approval

4. Review the preview HTML file and toggle approval in your config:
   ```yaml
   human_approval_flag: false
   ```
   Then re-run:
   ```bash
   cursor.api.trigger('publish_success', client='lotus001')
   ```

---

## 📊 5. Metrics & Tracking

- All analytics logs go to `/data/metrics/metrics_summary.csv`
- Weekly reports are saved to `/data/reports/weekly_digest.md`
- GA4 or Sheets integration can be configured through `agents.A4_analytics_agent.md`
- LLM visibility checkers are defined in the **Proof Metric Framework** document

---

## 🔁 6. Workflow Cycle

1. **Intake received** → client profile generated  
2. **Approval granted** → publish + tracking setup  
3. **Weekly report** → visibility, engagement, conversions  
4. **Monthly optimization** → automatic updates or schema refresh  
5. **Quarterly review** → tiered pricing, educational updates

---

## 🛠 7. Common Commands

| Command | Description |
|----------|--------------|
| `cursor.api.trigger('intake_received', client='ID')` | Starts the build cycle |
| `cursor.api.trigger('publish_success', client='ID')` | Confirms live deployment |
| `cursor.api.trigger('generate_report', phase='weekly')` | Forces weekly digest generation |
| `cursor.api.trigger('phase_complete', phase='1')` | Moves system to next PRD phase |

---

## 📬 8. Reporting Flow

| Output | Location | Frequency |
|---------|-----------|-----------|
| Weekly Digest | `/data/reports/weekly_digest.md` | Every Friday |
| Monthly Summary | `/data/reports/monthly_summary.csv` | 1st of month |
| Audit Log | `/data/logs/audit/` | End of each phase |

---

## 🔒 9. Governance Notes

- Only business name, email, and public URLs are stored.  
- All API keys (GA4, Sheets, Cloudflare) are referenced from `.env` or config, never embedded.  
- All reports anonymize client data before analytics upload.

---

## 🌐 10. Next Steps

1. ✅ Verify folder cleanup and ensure all agents are in `/agents/`.
2. ✅ Keep `AVE_state.yaml` current (phase tracking + approval status).
3. ✅ Run your first client test using `lotus_health.json`.
4. 🧩 After validation, onboard **Rivera Electric** and **Zach Taylor HVAC** using the same pattern.
5. 📈 Use weekly digests to track performance improvements.

---

**AI Design Solutions © 2025 — Internal Build Documentation**

> “Build once. Automate forever. Stay visible in the age of AI.”  
> — Alicia Sorensen
