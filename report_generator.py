"""
report_generator.py — AI Transformation Readiness Intelligence

Generates a clean executive narrative — no scoring methodology,
no dimension score lists. Reads like a briefing, not a data dump.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from insights import build_evidence_pack

load_dotenv()

SYSTEM_GUARDRAIL = """
You are an AI Transformation Readiness analyst preparing an executive narrative
for anyone accountable for making AI work — not just deploying it.
Use only the provided evidence pack.

Do not invent company facts, employee sentiment, financial projections, ROI figures,
vendor names, implementation history, or headcount decisions.
Do not recommend surveillance, punitive monitoring, or layoffs.
Do not include scoring methodology, dimension weights, or technical scoring details.

Write in a direct, evidence-based strategy consulting style — 4 short paragraphs maximum.
Your job: what is the primary value barrier, why it matters, and what to do first.
""".strip()


def deterministic_markdown(pack):
    primary  = pack["primary_failure_point"]
    patterns = pack["patterns"][:3]
    roadmap  = pack["roadmap"]

    lines = []
    lines.append("## Executive Narrative")
    lines.append(
        f"**{pack['organization_name']}** scores **{pack['overall_score']}/100** "
        f"({pack['overall_band']['label']}). "
        f"{pack['overall_band']['description']}"
    )
    lines.append("")
    lines.append(
        f"**The most likely value barrier is {primary['name']}.** "
        f"{primary['summary']} {primary.get('implications', '')}"
    )
    lines.append("")
    lines.append("**What the results suggest**")
    for p in patterns:
        lines.append(f"- **{p['name']}:** {p['summary']}")
    lines.append("")
    lines.append("**Priority actions**")
    seen = []
    for p in patterns:
        for a in p.get("actions", []):
            if a not in seen:
                seen.append(a)
    for a in seen[:5]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append(f"**30/60/90 day roadmap — {primary['name']}**")
    lines.append("")
    lines.append("*Next 30 days*")
    for a in roadmap["30"][:3]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("*Next 60 days*")
    for a in roadmap["60"][:3]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("*Next 90 days*")
    for a in roadmap["90"][:3]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("---")
    lines.append(
        "*This diagnostic uses submitted responses, dimension-weighted scoring logic, "
        "and approved value-barrier detection rules. It is an executive readiness diagnostic — "
        "not an audit, legal review, or financial forecast. "
        "No personally identifying information is stored beyond the active session.*"
    )
    return "\n".join(lines)


def generate_report(scores, responses, context, organization_name="Your organization"):
    pack    = build_evidence_pack(scores, responses, context, organization_name)
    api_key = os.getenv("OPENAI_API_KEY")
    model   = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        return deterministic_markdown(pack), pack, "rules-based"

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        primary = pack["primary_failure_point"]
        prompt = f"""
Write a 4-paragraph executive narrative for {organization_name}.
Use ONLY the evidence pack below. No scoring tables. No dimension weights.
No methodology section. Write like a trusted advisor briefing a leadership team.

Paragraph 1: Overall readiness in one sentence. Primary value barrier in one sentence. Why it matters.
Paragraph 2: What the detected patterns reveal about the organization's specific situation.
Paragraph 3: The 2-3 most important actions to take in the next 30 days.
Paragraph 4: What success looks like at 90 days if the organization acts on this.

End with one sentence diagnostic boundary note.

EVIDENCE PACK:
Organization: {organization_name}
Overall score: {pack['overall_score']}/100 — {pack['overall_band']['label']}
{pack['overall_band']['description']}

Primary value barrier: {primary['name']}
{primary['summary']}
{primary.get('implications', '')}

Detected patterns: {[p['name'] for p in pack['patterns'][:3]]}

Priority actions: {[a for p in pack['patterns'][:2] for a in p.get('actions', [])[:2]]}

30-day roadmap: {pack['roadmap']['30']}
"""
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_GUARDRAIL},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.2,
        )
        content = completion.choices[0].message.content
        return content, pack, f"GPT-enhanced ({model})"
    except Exception as e:
        fallback  = deterministic_markdown(pack)
        fallback += f"\n\n*GPT narrative unavailable; rules-based fallback used.*"
        return fallback, pack, "rules-based fallback"