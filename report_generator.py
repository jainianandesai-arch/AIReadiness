"""
report_generator.py — AI Transformation Readiness Intelligence

Returns a structured narrative dict for clean HTML rendering.
Roadmap phases are pattern-specific — labels and content both driven
by the user's actual diagnostic responses, not hardcoded defaults.

When OpenAI is connected, GPT is tightly constrained to work only
from the diagnostic data — no invented advice, no generic AI guidance.
"""

import os
from dotenv import load_dotenv
from insights import build_evidence_pack

load_dotenv()

SYSTEM_GUARDRAIL = """
You are an AI Transformation Readiness analyst. You have been given a structured
evidence pack from a diagnostic assessment completed by a specific organization.

Your job is to write a concise executive narrative — 4 short paragraphs — that
explains what THIS organization's results mean and what they should do first.

STRICT RULES:
- Use only the data in the evidence pack. Do not invent facts, benchmarks, or examples.
- Do not write generic AI transformation advice. Every sentence must connect directly
  to the specific value barrier, patterns, and scores in the evidence pack.
- Do not include scoring methodology, dimension weights, or technical scoring details.
- Do not recommend surveillance, punitive monitoring, or layoffs.
- The 30/60/90 roadmap must use the exact phase labels and actions from the evidence pack.
  Do not substitute or paraphrase them with generic advice.
- Write like a trusted advisor briefing a leadership team — direct, specific, honest.
""".strip()


def build_narrative(pack):
    """Build structured narrative dict from evidence pack."""
    primary = pack["primary_failure_point"]
    patterns = pack["patterns"][:3]
    roadmap = pack["roadmap"]
    phase_labels = pack.get("roadmap_phase_labels", {
        "30": "Establish baseline",
        "60": "Embed and equip",
        "90": "Operationalize value",
    })

    seen = []
    for p in patterns:
        for a in p.get("actions", []):
            if a not in seen:
                seen.append(a)

    return {
        "score_line":     f"{pack['overall_score']}/100 — {pack['overall_band']['label']}",
        "score_desc":     pack["overall_band"]["description"],
        "barrier_name":   primary["name"],
        "barrier_body":   f"{primary['summary']} {primary.get('implications', '')}",
        "patterns":       [{"name": p["name"], "summary": p["summary"]} for p in patterns],
        "actions":        seen[:5],
        "roadmap_label":  primary["name"],
        "phase_30_label": f"30 days — {phase_labels.get('30', 'Establish baseline')}",
        "phase_60_label": f"60 days — {phase_labels.get('60', 'Embed and equip')}",
        "phase_90_label": f"90 days — {phase_labels.get('90', 'Operationalize value')}",
        "roadmap_30":     roadmap["30"][:3],
        "roadmap_60":     roadmap["60"][:3],
        "roadmap_90":     roadmap["90"][:3],
        "boundary": (
            "This diagnostic uses submitted responses, dimension-weighted scoring logic, "
            "and approved value-barrier detection rules. It is an executive readiness diagnostic — "
            "not an audit, legal review, or financial forecast. "
            "No personally identifying information is stored beyond the active session."
        ),
    }


def generate_report(scores, responses, context, organization_name="Your organization"):
    pack      = build_evidence_pack(scores, responses, context, organization_name)
    api_key   = os.getenv("OPENAI_API_KEY")
    model     = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Always build the structured narrative from the evidence pack
    narrative = build_narrative(pack)

    if not api_key:
        return narrative, pack, "rules-based"

    # If OpenAI is connected, enhance only the opening 2 paragraphs
    # (score interpretation + pattern reading) — roadmap stays from evidence pack
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        primary  = pack["primary_failure_point"]
        patterns = pack["patterns"][:3]

        prompt = f"""
Write exactly 2 short paragraphs for {organization_name}. Use ONLY the data below.

Paragraph 1: What the overall score means for THIS organization. Name the primary value barrier.
Explain why it is the most important thing to address based on the specific pattern signals below.

Paragraph 2: What the combination of detected patterns reveals about where this organization
is getting stuck. Be specific to these patterns — do not write generic AI advice.

DATA (use only this):
- Organization: {organization_name}
- Overall score: {pack['overall_score']}/100 — {pack['overall_band']['label']}
- Band description: {pack['overall_band']['description']}
- Primary value barrier: {primary['name']}
  Summary: {primary['summary']}
  Implication: {primary.get('implications', '')}
- Detected patterns: {[p['name'] for p in patterns]}
- Pattern summaries: {[p['summary'] for p in patterns]}
- Section scores: {dict(pack['section_scores'])}
"""
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_GUARDRAIL},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.15,
        )
        gpt_text = completion.choices[0].message.content.strip()
        # Replace the score line and barrier body with GPT interpretation
        # but keep all structured data (actions, roadmap) from evidence pack
        narrative["gpt_narrative"] = gpt_text
        return narrative, pack, f"GPT-enhanced ({model})"
    except Exception as e:
        narrative["gpt_narrative"] = None
        return narrative, pack, "rules-based fallback"