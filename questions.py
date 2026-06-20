"""
questions.py — AI Transformation Readiness Intelligence
15 questions across 3 sections, 13 dimensions.

Dimension weighting (applied in scoring.py):
  Tier 1 — Critical (weight 1.5): Value discipline, Leadership behavior,
            Execution pathway, Workflow integration, Governance usability
  Tier 2 — Significant (weight 1.2): Manager capability, Trust calibration,
            Workforce impact, Shadow AI visibility
  Tier 3 — Contextual (weight 1.0): Measurement discipline, Skills transfer,
            Human judgment, Change capacity

Rationale: Tier 1 dimensions are the structural conditions without which
AI transformation cannot succeed regardless of other factors. Tier 2 dimensions
are strong multipliers or risk factors. Tier 3 dimensions matter but are more
recoverable or situation-dependent.

Q4 and Q5 (previously "Experimentation pathway" and "Scale discipline") are
now unified under "Execution pathway" — they measure the same underlying
construct (does the organization have a functioning pipeline from idea to
operating practice?) and scored separately they double-counted that weakness.
The new Q5 replaces "Scale discipline" with "Value attribution discipline" —
measuring whether the organization can distinguish AI causation from
correlation in its outcomes, which is the most common measurement failure
at mid-to-late maturity.
"""

CONTEXT_QUESTIONS = [
    {
        "id": "C1",
        "label": "AI journey stage",
        "question": "Where is your organization today in its AI journey?",
        "options": [
            "Mostly exploring",
            "Running small pilots",
            "Scaling selected use cases",
            "Using AI across multiple functions",
            "AI is embedded in core workflows",
        ],
    },
    {
        "id": "C2",
        "label": "Transformation ownership",
        "question": "Who currently owns AI transformation?",
        "options": [
            "No clear owner",
            "Mostly IT / technology",
            "Mostly individual business functions",
            "Shared business and technology ownership",
            "Dedicated cross-functional AI transformation owner",
        ],
    },
]

QUESTIONS = [
    # ── SECTION 1: Direction & Value ─────────────────────────────────────────
    {
        "id": "Q1",
        "section": "Direction & Value",
        "dimension": "Value discipline",
        "weight_tier": 1,
        "short": "Business problem discipline",
        "question": "Before starting an AI initiative, how clearly does your organization define the business problem it is trying to solve?",
        "options": [
            "The problem is rarely defined — tools are chosen first",
            "The problem is usually defined after the tool is selected",
            "Broad problem areas are defined, but expected outcomes are unclear",
            "Specific problems and expected outcomes are defined before starting",
            "Problem, baseline, owner, success metric, and expected value are defined before any tool is selected",
        ],
    },
    {
        "id": "Q2",
        "section": "Direction & Value",
        "dimension": "Leadership behavior",
        "weight_tier": 1,
        "short": "Executive role modeling",
        "question": "How often do senior leaders personally use AI to improve their own decisions, communication, or work — not just endorse it?",
        "options": [
            "Almost never — endorsement is verbal only",
            "Occasionally, mostly for simple or visible tasks",
            "Some leaders use AI regularly in their own work",
            "Most leaders use AI in meaningful, substantive work",
            "Leaders visibly model AI-enabled ways of working and set expectations for others",
        ],
    },
    {
        "id": "Q3",
        "section": "Direction & Value",
        "dimension": "Leadership behavior",
        "weight_tier": 1,
        "short": "Leadership signal clarity",
        "question": "How clearly do leaders communicate what AI is meant to improve — and what decisions will remain human?",
        "options": [
            "There is no consistent message from leadership",
            "Messaging is mostly tool-focused or enthusiasm-driven",
            "Messaging is positive but vague on outcomes and boundaries",
            "Messaging connects AI to specific business priorities and responsible use",
            "Messaging clearly links AI to strategy, work redesign, human judgment boundaries, and measurable value",
        ],
    },
    {
        "id": "Q4",
        "section": "Direction & Value",
        "dimension": "Execution pathway",
        "weight_tier": 1,
        "short": "Idea-to-scale pipeline",
        "question": "When an employee identifies a promising AI use case, how clear and functional is the path from idea to operating practice?",
        "options": [
            "No clear path — ideas go nowhere or are blocked",
            "Ideas can be raised but there is no defined process or owner",
            "There is a loose intake process but no consistent follow-through",
            "There is a defined pathway: intake, review, pilot, and scale decision",
            "A fast, governed pipeline exists: intake, test, measure, scale, and retire — with named owners at each stage",
        ],
    },
    {
        "id": "Q5",
        "section": "Direction & Value",
        "dimension": "Measurement discipline",
        "weight_tier": 2,
        "short": "Value attribution discipline",
        "question": "When AI initiatives show positive results, how confident is the organization that AI caused the improvement — rather than other factors?",
        "options": [
            "No measurement exists — results are assumed or asserted",
            "Results are tracked but attribution to AI is not examined",
            "Some initiatives use before/after comparisons as evidence",
            "Most initiatives use controlled comparisons or holdout groups to attribute impact",
            "AI value attribution uses rigorous baselines, control conditions, and isolation of AI's contribution from confounding factors",
        ],
    },
    {
        "id": "Q6",
        "section": "Direction & Value",
        "dimension": "Measurement discipline",
        "weight_tier": 2,
        "short": "Outcome measurement consistency",
        "question": "How consistently are AI initiatives measured after deployment — beyond usage and adoption metrics?",
        "options": [
            "They are not measured after deployment",
            "Measurement is mostly anecdotal or based on satisfaction",
            "Some initiatives track basic usage or activity metrics",
            "Most initiatives track business or workforce outcomes over time",
            "Each initiative tracks baseline, adoption quality, risk indicators, and business value — reviewed on a defined cadence",
        ],
    },

    # ── SECTION 2: Adoption & Work ────────────────────────────────────────────
    {
        "id": "Q7",
        "section": "Adoption & Work",
        "dimension": "Workflow integration",
        "weight_tier": 1,
        "short": "Workflow integration",
        "question": "How often is AI embedded into the actual flow of work — rather than offered as a separate optional tool employees may or may not use?",
        "options": [
            "Almost never — AI tools sit outside normal work processes",
            "Mostly added as optional tools alongside existing workflows",
            "Sometimes connected to specific workflows in a few teams",
            "Often integrated into redesigned workflows across multiple functions",
            "AI is intentionally designed into how work gets done — not bolted on",
        ],
    },
    {
        "id": "Q8",
        "section": "Adoption & Work",
        "dimension": "Manager capability",
        "weight_tier": 2,
        "short": "Manager work redesign capability",
        "question": "How prepared are managers to redesign work — not just encourage tool use — when AI changes how tasks are performed?",
        "options": [
            "Not prepared — managers have not been equipped for this",
            "Some awareness of the issue, but limited practical capability",
            "Moderate capability in select teams or functions",
            "Many managers can identify tasks to redesign and support their teams through it",
            "Managers are equipped to redesign work, redefine roles, reset performance expectations, and coach adoption",
        ],
    },
    {
        "id": "Q9",
        "section": "Adoption & Work",
        "dimension": "Human judgment",
        "weight_tier": 3,
        "short": "Human judgment protocol",
        "question": "When AI output conflicts with human judgment, what typically happens — and is there a defined process for it?",
        "options": [
            "There is no guidance — individuals decide on their own",
            "People ignore AI or accept it inconsistently depending on who is involved",
            "It depends on the individual leader or team culture",
            "There is informal review and discussion within teams",
            "There is a defined escalation process with clear validation steps and decision ownership",
        ],
    },
    {
        "id": "Q10",
        "section": "Adoption & Work",
        "dimension": "Trust calibration",
        "weight_tier": 2,
        "short": "Trust calibration",
        "question": "How well do employees understand when to trust, challenge, or reject AI-generated output — based on risk and decision stakes?",
        "options": [
            "They do not understand this — AI output is accepted or ignored randomly",
            "They mostly rely on personal judgment with no shared framework",
            "Some employees have developed their own calibration approach",
            "Most employees have role-level guidance and worked examples",
            "Employees are trained to validate AI output based on risk level, decision impact, and defined escalation criteria",
        ],
    },
    {
        "id": "Q11",
        "section": "Adoption & Work",
        "dimension": "Skills transfer",
        "weight_tier": 3,
        "short": "Skills-to-work translation",
        "question": "How often does AI training translate into visible, measurable changes in how work is actually performed — not just awareness?",
        "options": [
            "Almost never — training happens but work does not change",
            "Training increases awareness but does not change behaviour or output",
            "Some individuals apply AI in their work after training",
            "Many teams show measurable changes in how work is done after training",
            "Training is tied directly to workflow changes, manager expectations, and adoption metrics",
        ],
    },
    {
        "id": "Q12",
        "section": "Adoption & Work",
        "dimension": "Workforce impact",
        "weight_tier": 2,
        "short": "Workforce impact planning",
        "question": "Before AI changes a process, how proactively does the organization assess impact on roles, skills, workload, and employee experience?",
        "options": [
            "It does not assess this — changes are made without people impact analysis",
            "It reacts to concerns after they surface",
            "It considers impact informally or case by case",
            "It formally assesses role and skill impact for major initiatives",
            "It proactively plans role redesign, targeted upskilling, workload rebalancing, and employee support before changes go live",
        ],
    },

    # ── SECTION 3: Risk & Scale ───────────────────────────────────────────────
    {
        "id": "Q13",
        "section": "Risk & Scale",
        "dimension": "Governance usability",
        "weight_tier": 1,
        "short": "Governance usability",
        "question": "Which statement best describes AI governance in your organization — focusing on whether people can actually use it to make decisions?",
        "options": [
            "Governance does not exist — there are no rules or guardrails",
            "Governance exists as policy but is not accessible or used in practice",
            "Governance is policy-oriented and clarifies what is not allowed",
            "Governance actively helps teams use AI responsibly and make faster decisions",
            "Governance enables safe experimentation, fast decision rights, and scalable adoption — it accelerates rather than blocks",
        ],
    },
    {
        "id": "Q14",
        "section": "Risk & Scale",
        "dimension": "Shadow AI visibility",
        "weight_tier": 2,
        "short": "Shadow AI visibility",
        "question": "How much visibility does the organization have into employees using unapproved or consumer AI tools for work — and what is the response?",
        "options": [
            "No visibility — the organization does not know what is being used",
            "Very limited visibility with no structured response",
            "Some awareness, but no consistent policy or safer alternatives offered",
            "Reasonable visibility, guidance in place, and approved alternatives available",
            "Clear visibility, proactive communication of approved tools, practical guardrails, and a non-punitive response culture",
        ],
    },
    {
        "id": "Q15",
        "section": "Risk & Scale",
        "dimension": "Change capacity",
        "weight_tier": 3,
        "short": "Change capacity",
        "question": "How much organizational change is currently competing for employee and manager attention — and has AI adoption been sequenced with this in mind?",
        "options": [
            "Too many initiatives — people cannot absorb more change",
            "Heavy change load with visible fatigue affecting AI adoption",
            "Moderate change load — AI competes with other priorities",
            "Manageable change load — AI adoption has reasonable runway",
            "AI adoption has been deliberately sequenced with change capacity, timing, and communication in mind",
        ],
    },
]

SECTION_ORDER = ["Direction & Value", "Adoption & Work", "Risk & Scale"]

# Dimension weight map — used by scoring.py
DIMENSION_WEIGHTS = {
    # Tier 1 — Critical (1.5x)
    "Value discipline":       1.5,
    "Leadership behavior":    1.5,
    "Execution pathway":      1.5,
    "Workflow integration":   1.5,
    "Governance usability":   1.5,
    # Tier 2 — Significant (1.2x)
    "Manager capability":     1.2,
    "Trust calibration":      1.2,
    "Workforce impact":       1.2,
    "Shadow AI visibility":   1.2,
    "Measurement discipline": 1.2,
    # Tier 3 — Contextual (1.0x)
    "Human judgment":         1.0,
    "Skills transfer":        1.0,
    "Change capacity":        1.0,
}