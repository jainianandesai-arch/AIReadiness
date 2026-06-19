"""
report_generator.py — AI Transformation Readiness Intelligence

Report generation:
  Default mode: deterministic rules-based markdown from the evidence pack.
  Optional: OpenAI-enhanced narrative if OPENAI_API_KEY is set in .env.

  The deterministic report surfaces scoring methodology and
  pattern-specific roadmap in the output.
"""

import os
import copy
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


DEFAULT_ROADMAP = {
    "30": [
        "Select 2–3 priority workflows where AI can create measurable business value.",
        "Assign accountable business owners for each workflow.",
        "Define what decisions, outputs, and success measures will change."
    ],
    "60": [
        "Run controlled pilots with clear adoption, quality, and risk checkpoints.",
        "Document decision rights, escalation paths, and human review points.",
        "Identify manager and employee capability gaps exposed during the pilots."
    ],
    "90": [
        "Scale only the workflows that show measurable value and responsible adoption.",
        "Create a repeatable AI operating rhythm for review, learning, and governance.",
        "Convert lessons from pilots into standards, playbooks, and enablement materials."
    ],
}


DEFAULT_PRIMARY_BARRIER = {
    "name": "AI value is not yet consistently connected to business execution",
    "summary": (
        "The organization appears to have AI activity, but the path from AI usage to measurable "
        "business value is not yet sufficiently defined."
    ),
    "implications": (
        "Without clearer workflow ownership, decision rights, and outcome measures, AI may remain "
        "a set of tools rather than a transformation capability."
    ),
    "actions": [
        "Identify the highest-value workflows where AI should improve speed, quality, or capacity.",
        "Assign business owners who are accountable for workflow outcomes, not just tool usage.",
        "Define success measures before scaling any AI-enabled process.",
        "Establish human review, governance, and adoption checkpoints.",
    ],
    "roadmap": DEFAULT_ROADMAP,
}


def _normalize_barrier(value):
    """
    Ensures every value barrier has the same structure:
    name, summary, implications, actions, roadmap.
    """
    default = copy.deepcopy(DEFAULT_PRIMARY_BARRIER)

    if isinstance(value, dict):
        barrier = copy.deepcopy(default)
        barrier.update(value)

        if not isinstance(barrier.get("actions"), list):
            barrier["actions"] = default["actions"]

        if not isinstance(barrier.get("roadmap"), dict):
            barrier["roadmap"] = copy.deepcopy(DEFAULT_ROADMAP)

        for key in ["30", "60", "90"]:
            if not isinstance(barrier["roadmap"].get(key), list):
                barrier["roadmap"][key] = DEFAULT_ROADMAP[key]

        return barrier

    if isinstance(value, str) and value.strip():
        default["name"] = value.strip()
        return default

    return default


def _normalize_pack(pack, organization_name="Your organization"):
    """
    Protects the report generator from missing keys in the evidence pack.
    This prevents KeyError crashes in Streamlit.
    """
    if not isinstance(pack, dict):
        pack = {}

    pack.setdefault("organization_name", organization_name)
    pack.setdefault("overall_score", 0)
    pack.setdefault("overall_band", {"label": "Not enough evidence"})
    pack.setdefault("section_scores", {})
    pack.setdefault("dimension_scores", {})

    if not isinstance(pack.get("overall_band"), dict):
        pack["overall_band"] = {"label": str(pack.get("overall_band"))}

    if not isinstance(pack.get("section_scores"), dict):
        pack["section_scores"] = {}

    if not isinstance(pack.get("dimension_scores"), dict):
        pack["dimension_scores"] = {}

    patterns = pack.get("patterns")
    if not isinstance(patterns, list):
        patterns = []

    primary_source = pack.get("primary_value_barrier")
    if primary_source is None and patterns:
        primary_source = patterns[0]

    primary = _normalize_barrier(primary_source)
    pack["primary_value_barrier"] = primary

    normalized_patterns = [_normalize_barrier(p) for p in patterns]
    if not normalized_patterns:
        normalized_patterns = [primary]

    pack["patterns"] = normalized_patterns

    roadmap = pack.get("roadmap") or primary.get("roadmap") or DEFAULT_ROADMAP
    if not isinstance(roadmap, dict):
        roadmap = copy.deepcopy(DEFAULT_ROADMAP)

    for key in ["30", "60", "90"]:
        if not isinstance(roadmap.get(key), list):
            roadmap[key] = DEFAULT_ROADMAP[key]

    pack["roadmap"] = roadmap

    dimension_scores = pack.get("dimension_scores", {})

    if not isinstance(pack.get("strongest_dimensions"), list) or not pack.get("strongest_dimensions"):
        pack["strongest_dimensions"] = sorted(
            dimension_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:2]

    if not isinstance(pack.get("weakest_dimensions"), list) or not pack.get("weakest_dimensions"):
        pack["weakest_dimensions"] = sorted(
            dimension_scores.items(),
            key=lambda x: x[1]
        )[:3]

    return pack


def deterministic_markdown(pack):
    pack = _normalize_pack(pack)

    primary = pack["primary_value_barrier"]
    patterns = pack["patterns"][:3]
    strengths = pack["strongest_dimensions"][:2]
    gaps = pack["weakest_dimensions"][:3]
    roadmap = pack["roadmap"]

    lines = []

    lines.append("# AI Transformation Readiness Intelligence")
    lines.append(f"**Organization:** {pack['organization_name']}  ")
    lines.append(f"**Generated:** {datetime.now().strftime('%d %b %Y  %H:%M')}  ")
    lines.append(
        f"**Overall readiness:** {pack['overall_score']}/100 — "
        f"{pack['overall_band'].get('label', 'Not enough evidence')}  "
    )
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
    lines.append(
        "| Critical | 1.5× | Value discipline, Leadership behavior, Execution pathway, "
        "Workflow integration, Governance usability |"
    )
    lines.append(
        "| Significant | 1.2× | Manager capability, Trust calibration, Workforce impact, "
        "Shadow AI visibility, Measurement discipline |"
    )
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
    if pack["section_scores"]:
        for section, score in pack["section_scores"].items():
            lines.append(f"- **{section}:** {score}/100")
    else:
        lines.append("- Section-level scores were not available in the evidence pack.")
    lines.append("")

    lines.append("## Dimension scores")
    if pack["dimension_scores"]:
        for dim, score in sorted(pack["dimension_scores"].items(), key=lambda x: x[1]):
            lines.append(f"- **{dim}:** {score}/100")
    else:
        lines.append("- Dimension-level scores were not available in the evidence pack.")
    lines.append("")

    lines.append("## Strongest signals")
    if strengths:
        for name, score in strengths:
            lines.append(f"- **{name}:** {score}/100")
    else:
        lines.append("- Strongest signals could not be determined from the available evidence.")
    lines.append("")

    lines.append("## Weakest signals")
    if gaps:
        for name, score in gaps:
            lines.append(f"- **{name}:** {score}/100")
    else:
        lines.append("- Weakest signals could not be determined from the available evidence.")
    lines.append("")

    lines.append("## Detected value barriers")
    for p in patterns:
        lines.append(f"- **{p['name']}:** {p['summary']} {p['implications']}")
    lines.append("")

    lines.append("## Priority actions")
    seen = []
    for p in patterns:
        for action in p.get("actions", []):
            if action not in seen:
                seen.append(action)

    if seen:
        for action in seen[:6]:
            lines.append(f"- {action}")
    else:
        for action in DEFAULT_PRIMARY_BARRIER["actions"]:
            lines.append(f"- {action}")
    lines.append("")

    lines.append(f"## 30/60/90 day roadmap — {primary['name']}")
    lines.append("*Roadmap is specific to the primary value barrier detected.*")
    lines.append("")

    lines.append("**Next 30 days**")
    for action in roadmap["30"][:3]:
        lines.append(f"- {action}")
    lines.append("")

    lines.append("**Next 60 days**")
    for action in roadmap["60"][:3]:
        lines.append(f"- {action}")
    lines.append("")

    lines.append("**Next 90 days**")
    for action in roadmap["90"][:3]:
        lines.append(f"- {action}")
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
    pack = build_evidence_pack(scores, responses, context, organization_name)
    pack = _normalize_pack(pack, organization_name)

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

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
                {"role": "user", "content": prompt},
            ],
            temperature=0.15,
        )

        content = completion.choices[0].message.content
        return content, pack, f"GPT-enhanced ({model})"

    except Exception as e:
        fallback = deterministic_markdown(pack)
        fallback += (
            "\n\n_GPT report generation failed; rules-based fallback used. "
            f"Error: {str(e)[:180]}_"
        )
        return fallback, pack, "rules-based fallback"