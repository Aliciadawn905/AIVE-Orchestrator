"""
A6 Education Agent
Purpose:
Generates marketing and educational content for client visibility enhancement.
"""

import os
from openai import OpenAI
from datetime import datetime
from apps.common.db_utils import log_content_output, log_recommendation, log_governance_event


MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

A6_PROMPT = """
You are a senior AI marketing strategist. Produce deeply-researched, *actionable* guidance for ranking in LLM search (ChatGPT/Claude/Gemini/Perplexity), contrasted with Google SEO.

Output MUST be valid JSON with these keys:
- executive_summary: string
- llm_vs_google: string  # clear, practical differences (retrieval, citation, freshness, trust signals)
- ranking_matrix: [      # weight 0–100 (sum ≈ 100), rationale, quick actions
    { "signal": "Reviews", "weight": 0-100, "rationale": "...", "quick_actions": ["...", "..."] },
    ...
  ]
- website_requirements: [ "..." ]        # concrete on-page/off-page must-haves
- examples_that_stand_out: [ { "pattern": "Case studies hub", "why_it_works": "...", "how_to_build": "..." }, ... ]
- 90_day_plan: [ { "week": 1, "focus": "...", "deliverables": ["..."] }, ... ]
- sources_and_notes: [ "..." ]           # cite known patterns/standards; do not fabricate URLs

Tailor to the business: {business_name} ({domain}) in {industry}.
Prioritize signals LLMs favor: verifiable third-party proofs, structured knowledge, FAQ/QA coverage, entity clarity, and “answerability.”
Make it specific, non-generic, with short, high-utility sentences.
"""

def a6_generate_education(business_name: str, domain: str, industry: str):
    prompt = A6_PROMPT.format(business_name=business_name, domain=domain, industry=industry)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a precise, no-fluff AI marketing strategist."},
            {"role": "user", "content": prompt}
        ],
        response_format={ "type": "json_object" }
    )
    import json
    data = json.loads(resp.choices[0].message.content)
    return data

def a6_log_outputs(client_id: str, business_name: str, domain: str, industry: str, data: dict):
    # 1) Save brochure text to content_outputs
    brochure_sections = [
        ("Executive Summary", data.get("executive_summary","")),
        ("LLM vs Google: What’s Different", data.get("llm_vs_google","")),
        ("Website Requirements", "\n".join(data.get("website_requirements",[]))),
        ("Examples That Stand Out", "\n".join([f"- {i['pattern']}: {i.get('why_it_works','')}" for i in data.get("examples_that_stand_out",[])])),
        ("90-Day Plan", "\n".join([f"Week {i.get('week')}: {i.get('focus')} — Deliverables: {', '.join(i.get('deliverables',[]))}" for i in data.get("90_day_plan",[])])),
        ("Sources & Notes", "\n".join(data.get("sources_and_notes",[]))),
    ]
    brochure_text = f"# LLM Visibility Playbook — {business_name}\n\n" + "\n\n".join(
        [f"## {t}\n{body}" for (t, body) in brochure_sections if body]
    )

    log_content_output(
        agent_id="A6",
        client_id=client_id,
        content_type="llm_visibility_brochure",
        text=brochure_text,
        keywords=["LLM SEO","AI search","entity optimization","review signals","FAQ","schema"],
        status="draft",
        meta={"domain": domain, "industry": industry}
    )

    # 2) Save ranking matrix rows to research_insights
    for row in data.get("ranking_matrix", []):
        topic = f"Ranking Signal: {row.get('signal','')}"
        insight = f"Weight {row.get('weight',0)} — {row.get('rationale','')}\nQuick actions: {', '.join(row.get('quick_actions',[]))}"
        log_research_insight(
            agent_id="A6",
            client_id=client_id,
            topic=topic,
            insight=insight,
            source="OpenAI (A6 synthesis)",
            confidence=0.85,
            notes=f"{domain}"
        )

    # 3) Governance trail
    log_governance_event(
        agent_id="A6",
        client_id=client_id,
        event_type="research_generated",
        description=f"A6 generated LLM visibility research & brochure for {business_name}",
        category="Marketing",
        action_required=False,
        approval_status="Approved",
        reviewer="System",
        notes=f"Sections: executive_summary, llm_vs_google, matrix, website_requirements, examples, 90_day_plan"
    )

def run_a6_education(client_id: str, business_name: str, domain: str, industry: str):
    data = a6_generate_education(business_name, domain, industry)
    a6_log_outputs(client_id, business_name, domain, industry, data)
    return data

def create_campaign_guide(client_id: str, campaign_type: str):
    """Generate internal marketing or educational guide."""
    text = f"📘 {campaign_type} Campaign Guide for {client_id}: Learn how to optimize visibility and engagement using AI tools."

    log_content_output(
        agent_id="A6",
        client_id=client_id,
        content_type="campaign_guide",
        text=text,
        keywords=[campaign_type, "marketing", "education"],
        status="published",
        meta={"campaign_type": campaign_type}
    )

    print(f"🎓 Created campaign guide for {client_id} ({campaign_type})")
    return text


def propose_content_strategy(client_id: str):
    """Suggest multi-channel content strategy."""
    recommendations = [
        {"channel": "Instagram", "action": "Use 15-sec Reels with trending sounds."},
        {"channel": "Blog", "action": "Publish case studies every 2 weeks."},
        {"channel": "YouTube", "action": "Post behind-the-scenes spa experiences monthly."}
    ]

    for r in recommendations:
        log_recommendation(
            agent_id="A6",
            client_id=client_id,
            recommendation_type="content_strategy",
            recommendation_text=f"{r['channel']}: {r['action']}",
            confidence=0.9,
            priority="high"
        )

    print(f"🪄 Proposed content strategy for {client_id}")
    return recommendations


def publish_learning_material(client_id: str):
    """Publish or share educational content."""
    log_governance_event(
        agent_id="A6",
        client_id=client_id,
        event_type="education_material_published",
        description="Educational PDF posted to client dashboard.",
        category="Marketing",
        action_required=False,
        approval_status="approved",
        reviewer="A6_Marketing_Agent",
        notes="Material published successfully."
    )
    print(f"🗂️ Learning material published for {client_id}")
