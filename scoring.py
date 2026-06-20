"""
scoring.py — AI Transformation Readiness Intelligence

Scoring model:
  Raw response: 1-5 Likert scale
  Normalised: (raw-1)/4 × 100 → 0, 25, 50, 75, 100

  Overall score: dimension-weighted average (not question-weighted)
  Each dimension score = average of its constituent question scores
  Dimension scores are then weighted by tier before computing the overall.

  Weighting rationale: Tier 1 dimensions (Critical) carry 1.5× weight
  because they represent structural conditions without which AI transformation
  cannot succeed regardless of other factors. Tier 2 (Significant) carry 1.2×
  as strong multipliers or risk factors. Tier 3 (Contextual) carry 1.0× —
  they matter but are more recoverable or situation-dependent. This avoids
  the flat-average problem where a weak foundational dimension is diluted by
  strong peripheral ones.

  Section scores remain unweighted averages of their constituent questions
  for readability — they are diagnostic, not part of the composite.
"""

from collections import defaultdict
from questions import QUESTIONS, SECTION_ORDER, DIMENSION_WEIGHTS

BANDS = [
    (0,  39, "High exposure",
     "AI ambition is likely to face material execution risk unless core structural conditions are strengthened."),
    (40, 59, "Emerging readiness",
     "Some foundations exist, but the path from AI activity to scaled, measurable value is not yet reliable."),
    (60, 74, "Moderate readiness",
     "The organization is positioned to progress, but specific bottlenecks could limit scale and value realization."),
    (75, 89, "Strong readiness",
     "Several conditions needed to move from pilots toward sustained adoption and measurable outcomes are in place."),
    (90, 100, "Scale-ready",
     "Strong readiness signals across value discipline, work redesign, governance, and adoption."),
]


def score_to_100(value: int) -> int:
    return int(round((value - 1) / 4 * 100))


def get_band(score: int) -> dict:
    for low, high, label, description in BANDS:
        if low <= score <= high:
            return {"label": label, "description": description}
    return {"label": "Unscored", "description": "Score is outside expected range."}


def calculate_scores(responses: dict) -> dict:
    q_scores = {}
    section_values   = defaultdict(list)
    dimension_values = defaultdict(list)

    for q in QUESTIONS:
        raw        = int(responses.get(q["id"], 3))
        normalised = score_to_100(raw)
        q_scores[q["id"]] = {
            "raw":             raw,
            "score":           normalised,
            "section":         q["section"],
            "dimension":       q["dimension"],
            "weight_tier":     q.get("weight_tier", 3),
            "short":           q["short"],
            "selected_option": q["options"][raw - 1],
        }
        section_values[q["section"]].append(normalised)
        dimension_values[q["dimension"]].append(normalised)

    # Section scores — unweighted, for display
    section_scores = {
        s: int(round(sum(section_values[s]) / len(section_values[s])))
        for s in SECTION_ORDER
    }

    # Dimension scores — unweighted average within each dimension
    dimension_scores = {
        d: int(round(sum(vals) / len(vals)))
        for d, vals in dimension_values.items()
    }

    # Overall score — weighted by dimension tier
    weighted_sum   = 0.0
    total_weight   = 0.0
    for dim, score in dimension_scores.items():
        w = DIMENSION_WEIGHTS.get(dim, 1.0)
        weighted_sum += score * w
        total_weight += w
    overall = int(round(weighted_sum / total_weight)) if total_weight else 50

    weakest   = sorted(dimension_scores.items(), key=lambda x: x[1])[:4]
    strongest = sorted(dimension_scores.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        "overall_score":       overall,
        "overall_band":        get_band(overall),
        "section_scores":      section_scores,
        "dimension_scores":    dimension_scores,
        "question_scores":     q_scores,
        "weakest_dimensions":  weakest,
        "strongest_dimensions": strongest,
    }