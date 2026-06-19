"""
report_generator.py — AI Transformation Readiness Intelligence

Report generation:
  Default mode: deterministic rules-based markdown from the evidence pack.
  Optional: OpenAI-enhanced narrative if OPENAI_API_KEY is set in .env.

  The deterministic report now surfaces the scoring methodology and
  pattern-specific roadmap in the output, so a sophisticated reader can
  understand how the diagnostic reaches its conclusions.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from insights import build_evidence_pack

load_dotenv()

SYSTEM_GUARDRAIL = """
You are an AI Transformation Readiness analyst preparing an executive diagnostic report
for anyone accountable for making AI work — not just deploying it.
Use only the provided evidence pack.

Do not invent company facts, employee sentiment, financial projections, ROI figures,
vendor names, implementation history, or headcount decisions.
Do not recommend surveillance, punitive monitoring, or layoffs.

Write in a direct, evidence-based strategy consulting style.
Your job is to explain the most likely value barrier and what the organization should do first.
Keep the report concise enough for a 2-page PDF.
""".strip()


def deterministic_markdown(pack):
    primary  = pack["primary_value_barrier"]
    patterns = pack["patterns"][:3]
    strengths = pack["strongest_dimensions"][:2]
    gaps      = pack["weakest_dimensions"][:3]
    roadmap   = pack["roadmap"]

    lines = []
    lines.append("# AI Transformation Readiness Intelligence")
    lines.append(f"**Organization:** {pack['organization_name']}  ")
    lines.append(f"**Generated:** {datetime.now().strftime('%d %b %Y  %H:%M')}  ")
    lines.append(f"**Overall readiness:** {pack['overall_score']}/100 — {pack['overall_band']['label']}  ")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Scoring methodology")
    lines.append(
        "The overall score is a **dimension-weighted average**, not a flat question average. "
        "Dimensions are grouped into three tiers based on their structural importance to AI transformation success:"
    )
    lines.append("")
    lines.append("| Tier | Weight | Dimensions |")
    lines.append("|------|--------|------------|")
    lines.append("| Critical | 1.5× | Value discipline, Leadership behavior, Execution pathway, Workflow integration, Governance usability |")
    lines.append("| Significant | 1.2× | Manager capability, Trust calibration, Workforce impact, Shadow AI visibility, Measurement discipline |")
    lines.append("| Contextual | 1.0× | Human judgment, Skills transfer, Change capacity |")
    lines.append("")
    lines.append(
        "Tier 1 dimensions represent structural conditions without which AI transformation cannot succeed "
        "regardless of other factors. A weak Tier 1 dimension is not diluted by strong peripheral ones."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Executive headline")
    lines.append(
        f"The most likely AI transformation value barrier is **{primary['name']}**. "
        f"{primary['summary']} {primary['implications']}"
    )
    lines.append("")
    lines.append("## Readiness profile")
    for section, score in pack["section_scores"].items():
        lines.append(f"- **{section}:** {score}/100")
    lines.append("")
    lines.append("## Dimension scores")
    for dim, score in sorted(pack["dimension_scores"].items(), key=lambda x: x[1]):
        lines.append(f"- **{dim}:** {score}/100")
    lines.append("")
    lines.append("## Strongest signals")
    for name, score in strengths:
        lines.append(f"- **{name}:** {score}/100")
    lines.append("")
    lines.append("## Weakest signals")
    for name, score in gaps:
        lines.append(f"- **{name}:** {score}/100")
    lines.append("")
    lines.append("## Detected value barriers")
    for p in patterns:
        lines.append(f"- **{p['name']}:** {p['summary']} {p['implications']}")
    lines.append("")
    lines.append("## Priority actions")
    seen = []
    for p in patterns:
        for a in p["actions"]:
            if a not in seen:
                seen.append(a)
    for a in seen[:6]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append(f"## 30/60/90 day roadmap — {primary['name']}")
    lines.append("*Roadmap is specific to the primary value barrier detected.*")
    lines.append("")
    lines.append("**Next 30 days**")
    for a in roadmap["30"][:3]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("**Next 60 days**")
    for a in roadmap["60"][:3]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("**Next 90 days**")
    for a in roadmap["90"][:3]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Diagnostic boundaries")
    lines.append(
        "This diagnostic uses submitted assessment responses, dimension-weighted scoring logic, "
        "and approved value-barrier detection rules. It should be treated as an executive "
        "readiness diagnostic, not a full audit, legal review, or financial forecast. "
        "No personally identifying information or organizational data is stored beyond the active session."
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
        prompt = f"""
Create a concise executive diagnostic report for {organization_name}.
Use ONLY the evidence pack below. Do not repeat every score.
Focus on interpretation, the root cause of the primary value barrier, and concrete next steps.
Keep it short enough for a 2-page PDF.

Required sections:
1. Executive headline — the one thing the leadership team needs to understand
2. What the results suggest — interpretation, not score recitation
3. Primary value barrier — root cause analysis
4. Evidence signals — what in the responses points to this
5. Priority actions — concrete, sequenced, owned
6. 30/60/90 day roadmap — use the pattern-specific roadmap from the evidence pack
7. Diagnostic boundaries — one paragraph

EVIDENCE PACK:
{pack}
"""
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_GUARDRAIL},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.15,
        )
        content = completion.choices[0].message.content
        return content, pack, f"GPT-enhanced ({model})"
    except Exception as e:
        fallback  = deterministic_markdown(pack)
        fallback += f"\n\n_GPT report generation failed; rules-based fallback used. Error: {str(e)[:180]}_"
        return fallback, pack, "rules-based fallback"