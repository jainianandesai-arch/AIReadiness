"""
report_generator.py — AI Transformation Readiness Intelligence

Uses the Anthropic API (Claude) to write the full executive narrative.
Claude is given the complete diagnostic evidence pack and writes a
concise, specific, advisory-quality summary — constrained strictly
to the user's actual responses. No generic AI advice.

Structured data (roadmap, phase labels, actions, patterns) always
comes from the rules engine. Claude interprets and narrates.
If the API call fails, a clean rules-based fallback is used.
"""

import os
from dotenv import load_dotenv
from insights import build_evidence_pack

load_dotenv()

SYSTEM_PROMPT = """
You are an AI Transformation Readiness analyst preparing an executive narrative
for a leadership team. You have been given structured diagnostic data from a
specific organization's assessment.

Your job: write a concise, direct, advisory-quality executive summary.

STRICT RULES:
- Use only the diagnostic data provided. Do not invent facts, benchmarks, or examples.
- Every sentence must connect to the specific scores, value barrier, and patterns detected.
- Do not write generic AI transformation advice. This must read as specific to this organization.
- Do not include scoring methodology, dimension weights, or technical details.
- Do not recommend surveillance, punitive monitoring, or layoffs.
- Write like a trusted senior advisor briefing a CHRO or CEO — direct, honest, specific.
- Write exactly 2 short paragraphs. Maximum 3 sentences per paragraph.
- Do not use bullet points or headers. Flowing prose only.
- Be concise. A leader should be able to read this in under 30 seconds.
""".strip()


def build_narrative(pack):
    """Build structured narrative dict from evidence pack — always runs."""
    primary     = pack["primary_failure_point"]
    patterns    = pack["patterns"][:3]
    roadmap     = pack["roadmap"]
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
        "gpt_narrative":  None,
        "boundary": (
            "This diagnostic uses submitted responses, dimension-weighted scoring logic, "
            "and approved value-barrier detection rules. It is an executive readiness diagnostic — "
            "not an audit, legal review, or financial forecast. "
            "No personally identifying information is stored beyond the active session."
        ),
    }


def _build_prompt(pack, organization_name):
    primary  = pack["primary_failure_point"]
    patterns = pack["patterns"][:3]
    return f"""
Write a concise executive narrative for {organization_name}. Exactly 2 short paragraphs, 3 sentences max each.

Paragraph 1: What the overall score means for this organization. Name the primary value barrier and why it is the most critical thing to address right now.

Paragraph 2: What the combination of detected value barriers reveals about where this organization is getting stuck. End with one concrete thing leadership should do in the next 30 days.

DIAGNOSTIC DATA — use only this:
Organization: {organization_name}
Overall score: {pack['overall_score']}/100 — {pack['overall_band']['label']}
{pack['overall_band']['description']}

Section scores:
{chr(10).join(f"  {sec}: {sc}/100" for sec, sc in pack['section_scores'].items())}

Primary value barrier: {primary['name']}
  {primary['summary']}
  {primary.get('implications', '')}

Detected value barriers: {[p['name'] for p in patterns]}
Weakest dimensions: {[f"{d}: {s}/100" for d, s in pack['weakest_dimensions'][:3]]}
""".strip()


def generate_report(scores, responses, context, organization_name="Your organization"):
    pack      = build_evidence_pack(scores, responses, context, organization_name)
    narrative = build_narrative(pack)
    api_key   = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        return narrative, pack, "rules-based"

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": _build_prompt(pack, organization_name)}
            ],
        )
        narrative["gpt_narrative"] = message.content[0].text.strip()
        return narrative, pack, "AI-enhanced"

    except Exception as e:
        narrative["gpt_narrative"] = None
        return narrative, pack, f"rules-based (API unavailable)"