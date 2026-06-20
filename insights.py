"""
insights.py — AI Transformation Readiness Intelligence

Pattern detection logic:
  Patterns fire based on relationships between dimension scores, not raw
  thresholds in isolation. The diagnostic value comes from detecting gaps
  between paired signals (e.g. leadership ahead of manager capability,
  experimentation ahead of scale discipline) rather than simply flagging
  low scores.

  Severity is calibrated so the most structurally dangerous patterns rank
  highest regardless of how many other patterns fire. Patterns that overlap
  substantially in meaning are deduplicated — "AI Theatre Risk" and
  "Value Measurement Blind Spot" cannot both be the primary pattern since
  they describe the same underlying failure from different angles.

Roadmap logic:
  The 30/60/90 roadmap is pattern-specific. Each pattern has its own
  sequenced actions. The generic library is used only as a final fallback.
  Pattern-specific roadmaps prioritise the root cause of the detected
  failure, not generic AI transformation advice.
"""

# ── Pattern-specific roadmaps ─────────────────────────────────────────────────
ROADMAP_BY_PATTERN = {
    "AI Theatre Risk": {
        "30": [
            "Audit all active AI initiatives: identify which have a defined baseline and success metric.",
            "Require each initiative to name a business owner accountable for value — not an IT owner.",
            "Pause any initiative that cannot articulate the problem it solves and how success will be measured.",
        ],
        "60": [
            "Introduce a value gate: no AI initiative advances past pilot without a confirmed measurement plan.",
            "Train leadership to distinguish activity metrics (usage, adoption) from business value metrics.",
            "Build a simple AI value dashboard — one metric per initiative, reviewed monthly.",
        ],
        "90": [
            "Publish internal results from at least two AI initiatives with before/after business impact data.",
            "Tie AI investment decisions to demonstrated value from prior initiatives.",
            "Shift leadership communication from AI enthusiasm to AI accountability.",
        ],
    },
    "Pilot Purgatory": {
        "30": [
            "Map all current AI pilots: identify which have a named post-pilot owner and a scale decision date.",
            "Kill or formally park pilots with no clear path forward — active purgatory is worse than closure.",
            "Define the criteria for a pilot to earn a scale decision: adoption threshold, quality bar, cost model.",
        ],
        "60": [
            "Build a stage-gate pathway: Explore → Pilot → Scale decision → Operate → Retire.",
            "Assign post-pilot ownership before pilots start, not after they show results.",
            "Identify the one or two pilots closest to operating practice and accelerate them as proof points.",
        ],
        "90": [
            "Convert at least one strong pilot into standard operating practice with documented ownership.",
            "Create a public internal record of what scaled, what was parked, and why — normalise both outcomes.",
            "Establish a quarterly portfolio review: pipeline health, stage distribution, value in operation.",
        ],
    },
    "Manager Bottleneck": {
        "30": [
            "Assess manager readiness: survey or interview 10-15 managers on their confidence to redesign work with AI.",
            "Identify 3-5 managers already doing work redesign well and build a peer-learning programme around them.",
            "Brief managers on the distinction between encouraging tool use and actually redesigning how work flows.",
        ],
        "60": [
            "Run manager workshops on task decomposition: which tasks can AI take, which remain human, which are redesigned.",
            "Give managers practical playbooks for their function — not generic AI training.",
            "Tie manager performance conversations to team-level AI adoption and work redesign outcomes.",
        ],
        "90": [
            "Build manager capability into the standard people leader development programme.",
            "Track the ratio of AI-enabled work redesign to AI tool deployment — close the gap.",
            "Recognise and promote managers who successfully redesign work, not just those who drive tool usage.",
        ],
    },
    "Last-Mile Workflow Failure": {
        "30": [
            "Audit the top 5 AI use cases: are they embedded in daily work or sitting beside it as optional tools?",
            "Interview 10 employees who completed AI training 60+ days ago — ask what changed in their actual work.",
            "Identify the 2-3 workflows with the highest AI potential and the lowest current integration.",
        ],
        "60": [
            "Redesign those 2-3 workflows with AI built in — not as an add-on, but as the default path.",
            "Update templates, meeting structures, and decision routines to assume AI-assisted inputs.",
            "Work with managers to set explicit expectations: what outputs now require AI assistance?",
        ],
        "90": [
            "Measure the delta between AI tool usage and workflow-level change — close the gap systematically.",
            "Stop investing in AI training programmes that are not tied to specific workflow changes.",
            "Publish workflow redesign case studies internally — make the change visible, not just the tool.",
        ],
    },
    "Trust Calibration Gap": {
        "30": [
            "Define, for the top 5 AI use cases, when AI output can be used directly vs. must be reviewed vs. must be escalated.",
            "Identify the two or three decisions where over-trust in AI creates the most organizational risk.",
            "Brief leaders on their accountability for AI output that passes through their teams without review.",
        ],
        "60": [
            "Build role-level trust calibration guidance: what does 'good enough' AI output look like in this role?",
            "Run targeted workshops on AI failure modes — not to create fear, but to build calibrated judgment.",
            "Establish an escalation path for AI outputs that conflict with expert judgment.",
        ],
        "90": [
            "Incorporate trust calibration into onboarding for AI-heavy roles.",
            "Track escalation rates and AI override decisions as leading indicators of calibration health.",
            "Review and update trust thresholds as AI capabilities and use cases evolve.",
        ],
    },
    "Governance Vacuum": {
        "30": [
            "Publish a one-page minimum: what is approved, what requires review, what is not permitted.",
            "Name a single accountable governance owner — not a committee, a person.",
            "Create a simple intake channel for employees to ask governance questions without fear of penalty.",
        ],
        "60": [
            "Expand the minimum rules into practical decision guidance by function or use case type.",
            "Define data handling requirements for AI tools — what data can go where, and under what conditions.",
            "Establish a fast-track review path for low-risk AI use cases so governance enables, not just restricts.",
        ],
        "90": [
            "Implement a lightweight AI registry: what tools are in use, by whom, for what purpose, under what controls.",
            "Tie governance to procurement: no new AI tool without a governance review as part of the approval.",
            "Publish the governance framework externally — signal maturity to clients, regulators, and talent.",
        ],
    },
    "Governance Drag": {
        "30": [
            "Survey 10-15 employees and managers: where has governance slowed or blocked productive AI use?",
            "Identify the 3 most common governance bottlenecks and classify each as: policy gap, clarity gap, or process gap.",
            "Publish a plain-language FAQ that translates existing policy into practical decisions.",
        ],
        "60": [
            "Create tiered decision rights: what can a team decide without review, what needs a business unit sign-off, what requires central review.",
            "Run a 30-day fast-track experiment: pre-approve a defined set of low-risk use cases and measure adoption lift.",
            "Reframe governance communications from restriction to enablement — what can you do safely, not what you cannot do.",
        ],
        "90": [
            "Review governance policy against the last 6 months of actual AI use — remove rules that no longer fit.",
            "Build governance into workflow design, not as a separate step but as embedded guardrails.",
            "Measure governance friction quarterly: time from use case idea to approval, rate of rejections vs approvals.",
        ],
    },
    "Shadow AI Risk": {
        "30": [
            "Conduct a confidential audit or pulse survey: which AI tools are employees using outside approved channels, and why?",
            "Identify the gap — what need is unapproved AI meeting that approved tools are not?",
            "Publish an amnesty communication: disclose what you are using, no penalty, help us understand the need.",
        ],
        "60": [
            "Fast-track approval for the most commonly used unapproved tools that meet security and data requirements.",
            "Where tools cannot be approved, provide an approved alternative that meets the same employee need.",
            "Train managers to surface shadow AI use as a signal of unmet need, not a disciplinary issue.",
        ],
        "90": [
            "Establish ongoing shadow AI monitoring with a defined response process — visibility without punitiveness.",
            "Build a feedback channel: employees flag AI tools they want evaluated for approval.",
            "Report shadow AI trends to leadership as a leading indicator of governance and adoption health.",
        ],
    },
    "Change Saturation Risk": {
        "30": [
            "Map current change initiatives against team and manager capacity — identify where AI adoption is competing with other priorities.",
            "Sequence AI rollout to avoid collision with peak change load periods in affected teams.",
            "Simplify the AI message: one clear priority, not five AI programmes running simultaneously.",
        ],
        "60": [
            "Work with change management to integrate AI adoption into the existing change portfolio — not as an additional programme.",
            "Reduce the number of active AI initiatives: focus investment on two or three with the highest value potential.",
            "Give managers explicit permission to delay AI adoption in teams under exceptional change load.",
        ],
        "90": [
            "Build AI adoption sequencing into annual planning — treat it as a capacity decision, not just a technology decision.",
            "Establish a change capacity metric: measure and publish the organizational change load quarterly.",
            "Reconnect with teams that delayed adoption — resume with updated context and lighter-touch onboarding.",
        ],
    },
    "Workforce Impact Blind Spot": {
        "30": [
            "For the top 3 AI initiatives in flight: conduct a rapid role and workload impact assessment now, before changes go live.",
            "Identify which roles are most affected and whether those employees know what is changing.",
            "Brief HR and people leaders on their accountability for workforce impact planning alongside AI implementation.",
        ],
        "60": [
            "Build a workforce impact checklist into the AI initiative intake process — required before any pilot moves to scale.",
            "Define what 'employee support' means concretely: retraining, role redesign, transition pathways, or workload relief.",
            "Involve affected employees in workflow redesign — co-design reduces resistance and improves adoption.",
        ],
        "90": [
            "Publish a workforce impact framework: how the organization plans, communicates, and supports people through AI-driven change.",
            "Connect AI implementation planning with workforce planning cycles — treat them as the same decision.",
            "Track employee experience metrics in AI-affected teams as a lagging indicator of impact planning quality.",
        ],
    },
    "Value Measurement Blind Spot": {
        "30": [
            "Identify the three AI initiatives with the most investment and confirm whether any have a pre-defined baseline.",
            "For each, establish or reconstruct a baseline now — even retrospectively — so future measurement is possible.",
            "Distinguish usage metrics (logins, prompts, time saved estimates) from business outcome metrics (error rate, cycle time, revenue, cost).",
        ],
        "60": [
            "Build a measurement template into the AI initiative process: baseline, expected outcome, measurement method, review date.",
            "Train initiative owners to isolate AI's contribution — control groups, holdout periods, or regression analysis where feasible.",
            "Establish a quarterly AI value review: what did we expect, what did we get, what explains the gap?",
        ],
        "90": [
            "Publish an internal AI value report — even if results are mixed. Credibility comes from honesty, not only success stories.",
            "Tie AI investment decisions to the quality of measurement from prior initiatives, not just their stated results.",
            "Build AI ROI attribution into the standard business case and post-implementation review process.",
        ],
    },
    "Focused Scale Opportunity": {
        "30": [
            "Identify the specific dimension holding back the next level of value and confirm it with 5-10 interviews.",
            "Prioritise one improvement that would have the highest impact on AI value realisation in the next 90 days.",
            "Build a concrete action plan for that single dimension — not a broad AI strategy refresh.",
        ],
        "60": [
            "Execute the targeted improvement with named owners and weekly check-ins.",
            "Measure progress on that dimension specifically — leading indicators, not just activity.",
            "Share progress with leadership to build momentum and identify the next constraint.",
        ],
        "90": [
            "Assess whether the improvement moved the needle — document what changed and what did not.",
            "Identify the next highest-leverage improvement and repeat the cycle.",
            "Use this focused approach to build a culture of continuous AI capability improvement.",
        ],
    },
}

# Generic fallback (used if a pattern is not in ROADMAP_BY_PATTERN)
# Pattern-specific phase labels — what each 30/60/90 phase is called
# for this particular failure mode. Makes it clear the roadmap is
# diagnostic-driven, not generic.
ROADMAP_PHASE_LABELS = {
    "AI Theatre Risk": {
        "30": "Establish value accountability",
        "60": "Build measurement discipline",
        "90": "Shift from activity to impact",
    },
    "Pilot Purgatory": {
        "30": "Diagnose the pipeline blockage",
        "60": "Build the path from pilot to practice",
        "90": "Operationalize your strongest pilots",
    },
    "Manager Bottleneck": {
        "30": "Assess manager readiness",
        "60": "Equip managers to redesign work",
        "90": "Embed work redesign into leadership practice",
    },
    "Last-Mile Workflow Failure": {
        "30": "Audit what actually changed after training",
        "60": "Redesign workflows with AI built in",
        "90": "Measure workflow change, not tool usage",
    },
    "Trust Calibration Gap": {
        "30": "Define when to trust, challenge, or reject AI output",
        "60": "Build role-level calibration guidance",
        "90": "Institutionalize human judgment protocols",
    },
    "Governance Vacuum": {
        "30": "Establish minimum guardrails",
        "60": "Build practical decision guidance",
        "90": "Formalize governance as an enabler",
    },
    "Governance Drag": {
        "30": "Identify what governance is blocking",
        "60": "Create tiered decision rights",
        "90": "Make governance an adoption accelerator",
    },
    "Shadow AI Risk": {
        "30": "Understand what employees are actually using",
        "60": "Close the gap with approved alternatives",
        "90": "Build a non-punitive visibility culture",
    },
    "Change Saturation Risk": {
        "30": "Map AI adoption against change capacity",
        "60": "Sequence and simplify the AI agenda",
        "90": "Resume adoption with capacity in mind",
    },
    "Workforce Impact Blind Spot": {
        "30": "Assess people impact for in-flight initiatives",
        "60": "Build workforce impact into the intake process",
        "90": "Connect AI planning to workforce planning",
    },
    "Value Measurement Blind Spot": {
        "30": "Establish baselines — even retrospectively",
        "60": "Build measurement into every initiative",
        "90": "Publish results and tie investment to evidence",
    },
    "Focused Scale Opportunity": {
        "30": "Identify and confirm the highest-leverage gap",
        "60": "Execute a targeted improvement",
        "90": "Measure, learn, and identify the next constraint",
    },
}

ROADMAP_GENERIC = {
    "30": [
        "Name the accountable business owner for AI adoption and value realisation.",
        "Prioritise 3-5 AI use cases using business value, workflow fit, risk, and scale potential.",
        "Define baseline metrics before expanding any active pilot.",
    ],
    "60": [
        "Build a pilot-to-scale review rhythm covering adoption, quality, risk, and business outcomes.",
        "Equip managers to redesign tasks and workflows rather than only encourage tool usage.",
        "Embed AI support into existing workflows, meetings, templates, and decision routines.",
    ],
    "90": [
        "Convert the strongest use cases into standard operating practice with named ownership.",
        "Tie AI training to real work changes, performance expectations, and manager routines.",
        "Establish a quarterly AI value dashboard across adoption, quality, risk, and impact.",
    ],
}

ACTIONS_BY_PATTERN = {
    "AI Theatre Risk": [
        "Audit all AI initiatives: which have a defined baseline and a business owner accountable for value?",
        "Require each initiative to define the problem it solves, expected outcome, and success metric before any tool is selected.",
    ],
    "Pilot Purgatory": [
        "Build a stage-gate pipeline: Explore → Pilot → Scale decision → Operate → Retire — with owners at each gate.",
        "Assign post-pilot ownership before pilots start, not after they succeed.",
    ],
    "Manager Bottleneck": [
        "Train managers on task decomposition and work redesign — not just AI tool awareness.",
        "Give managers function-specific playbooks showing how AI changes work, roles, and performance expectations.",
    ],
    "Last-Mile Workflow Failure": [
        "Redesign the top 2-3 workflows with AI built in — not as an optional add-on, but as the default path.",
        "Update templates, meeting structures, and decision routines to assume AI-assisted inputs.",
    ],
    "Trust Calibration Gap": [
        "Define, per use case, when AI output can be used directly, when it must be reviewed, and when it must be escalated.",
        "Provide role-specific examples of high-risk and low-risk AI use with worked scenarios.",
    ],
    "Governance Drag": [
        "Create tiered decision rights so teams can act on low-risk AI use cases without central review.",
        "Reframe governance from restriction to enablement — publish what you can do safely, not only what you cannot.",
    ],
    "Governance Vacuum": [
        "Publish a one-page minimum: what is approved, what requires review, what is not permitted.",
        "Name a single governance owner — not a committee — accountable for practical guidance.",
    ],
    "Shadow AI Risk": [
        "Conduct a confidential audit: which tools are employees using outside approved channels, and what need are they meeting?",
        "Fast-track approval for commonly used unapproved tools that meet security and data requirements.",
    ],
    "Change Saturation Risk": [
        "Sequence AI adoption around current change load — treat it as a capacity decision, not only a technology one.",
        "Reduce the number of active AI initiatives: concentrate investment on two or three with the highest value potential.",
    ],
    "Workforce Impact Blind Spot": [
        "Conduct a rapid role and workload impact assessment for all AI initiatives currently in flight.",
        "Build a workforce impact checklist into the AI initiative intake process — required before any pilot moves to scale.",
    ],
    "Value Measurement Blind Spot": [
        "Establish or reconstruct a baseline for the three most-invested AI initiatives — even retrospectively.",
        "Build a measurement template into every AI initiative: baseline, expected outcome, method, review date.",
    ],
    "Focused Scale Opportunity": [
        "Identify the single dimension holding back the next level of value and build a targeted 90-day improvement plan.",
        "Measure progress on that dimension specifically — not broad AI activity.",
    ],
}


def q(scores, qid):
    return scores["question_scores"][qid]["score"]


def detect_failure_patterns(scores):
    patterns = []
    fired_names = set()

    def add(name, severity, summary, evidence, implications):
        if name not in fired_names:
            fired_names.add(name)
            patterns.append({
                "name":        name,
                "severity":    severity,
                "score":       severity,
                "summary":     summary,
                "evidence":    evidence,
                "implications": implications,
                "actions":     ACTIONS_BY_PATTERN.get(name, []),
                "roadmap":     ROADMAP_BY_PATTERN.get(name, ROADMAP_GENERIC),
                "phase_labels": ROADMAP_PHASE_LABELS.get(name, {
                    "30": "Establish baseline",
                    "60": "Embed and equip",
                    "90": "Operationalize value",
                }),
            })

    # Dimension signals
    leadership       = round((q(scores,"Q2") + q(scores,"Q3")) / 2)
    value_disc       = q(scores,"Q1")
    measurement      = round((q(scores,"Q5") + q(scores,"Q6")) / 2)
    value            = round((value_disc + measurement) / 2)
    execution        = q(scores,"Q4")          # Q4 is now the unified execution pathway
    workflow         = q(scores,"Q7")
    manager          = q(scores,"Q8")
    trust            = round((q(scores,"Q9") + q(scores,"Q10")) / 2)
    skills           = q(scores,"Q11")
    workforce_impact = q(scores,"Q12")
    governance       = q(scores,"Q13")
    shadow           = q(scores,"Q14")
    change           = q(scores,"Q15")

    # ── Pattern rules ──────────────────────────────────────────────────────────
    # AI Theatre: strong leadership signal, weak value discipline
    if leadership >= 65 and value < 55:
        add("AI Theatre Risk", 90 - value,
            "Leadership messaging appears stronger than the discipline used to prove value.",
            ["Leadership signals are relatively strong",
             "Business value definition and measurement are both weaker than leadership readiness"],
            "The organization may look active on AI while struggling to show measurable business outcomes.")

    # Pilot Purgatory: execution pathway weak (replaces old Q4+Q5 split)
    if execution < 55:
        add("Pilot Purgatory", 88 - execution,
            "The path from AI idea to operating practice is weak or missing.",
            ["Idea-to-scale pipeline is below the threshold needed for reliable execution",
             "Pilots may surface but lack a governed path to ownership and scale"],
            "Promising AI work may remain local, temporary, or dependent on individual champions.")

    # Manager Bottleneck: leadership ahead of manager capability
    if leadership >= 60 and manager < 60:
        add("Manager Bottleneck", 90 - manager,
            "Executive support is ahead of the manager capability needed to actually redesign work.",
            ["Leadership readiness is stronger than manager work-redesign capability"],
            "AI adoption may stall in the layer responsible for changing daily work, routines, and performance expectations.")

    # Last-Mile Workflow Failure: skills/training exist but workflow doesn't change
    if skills >= 50 and workflow < 55:
        add("Last-Mile Workflow Failure", 90 - workflow,
            "AI learning or activity is not translating into how work actually gets done.",
            ["Skills-to-work signals are stronger than workflow integration",
             "Training may be happening without corresponding workflow redesign"],
            "Employees may develop AI awareness without meaningful changes to work design, decision routines, or productivity.")

    # Trust Calibration Gap
    if trust < 60:
        add("Trust Calibration Gap", 90 - trust,
            "The organization lacks a shared framework for when to trust, challenge, or reject AI output.",
            ["Human judgment protocol and trust calibration are both below strong readiness"],
            "Adoption may become inconsistent, risky, or dependent on individual judgment rather than defined criteria.")

    # Governance Vacuum vs Drag (mutually exclusive)
    # Vacuum: governance is critically absent (score < 25 — no rules exist at all)
    # Drag:   governance exists but blocks progress (25-59) AND execution is also weak
    if governance < 25:
        add("Governance Vacuum", 95 - governance,
            "AI governance is too weak to support safe experimentation or scale.",
            ["Governance usability is critically low — no effective rules or guardrails exist"],
            "Teams may avoid AI because they are unsure what is allowed — or use it without any guardrails.")
    elif governance < 60 and execution < 60:
        add("Governance Drag", 88 - governance,
            "Governance exists but may not be clear or usable enough to enable progress.",
            ["Governance usability and execution pathway are both below strong readiness",
             "Policy may exist but people cannot translate it into practical decisions"],
            "AI adoption may slow because people cannot translate policy into practical decisions.")

    # Shadow AI Risk
    if shadow < 60:
        add("Shadow AI Risk", 90 - shadow,
            "The organization has limited visibility into unapproved AI use.",
            ["Shadow AI visibility is below strong readiness"],
            "Employees may already be using AI outside approved tools, data controls, or validation guidance.")

    # Change Saturation Risk
    if change < 50:
        add("Change Saturation Risk", 90 - change,
            "AI adoption is competing with a heavy organizational change load.",
            ["Change capacity is below the threshold needed for reliable adoption"],
            "Adoption risk may be driven less by resistance to AI and more by limited organizational capacity.")

    # Workforce Impact Blind Spot
    if workforce_impact < 55:
        add("Workforce Impact Blind Spot", 90 - workforce_impact,
            "The organization may be changing processes before understanding the people impact.",
            ["Workforce impact planning is below strong readiness"],
            "Resistance may emerge after implementation because role, skill, and workload impacts were not designed upfront.")

    # Value Measurement Blind Spot — only if AI Theatre hasn't already fired
    # (they describe the same failure from different angles; avoid redundancy)
    if value < 55 and execution >= 45 and "AI Theatre Risk" not in fired_names:
        add("Value Measurement Blind Spot", 90 - value,
            "AI activity may be moving forward without rigorous baseline and outcome measurement.",
            ["Value discipline and measurement are weaker than execution activity"],
            "The organization may be confusing usage, interest, or anecdote with business impact.")

    # Fallback
    if not patterns:
        weakest = scores["weakest_dimensions"][0]
        add("Focused Scale Opportunity", 35,
            f"Readiness is broadly solid — the most actionable improvement area is {weakest[0].lower()}.",
            [f"Lowest readiness dimension: {weakest[0]} ({weakest[1]}/100)"],
            "The organization has a working foundation; targeted improvement in this dimension would strengthen AI value realisation.")

    return sorted(patterns, key=lambda p: p["severity"], reverse=True)[:5]


def build_evidence_pack(scores, responses, context, organization_name):
    patterns = detect_failure_patterns(scores)
    primary  = patterns[0]
    return {
        "organization_name":    organization_name,
        "context":              context,
        "overall_score":        scores["overall_score"],
        "overall_band":         scores["overall_band"],
        "section_scores":       scores["section_scores"],
        "dimension_scores":     scores["dimension_scores"],
        "strongest_dimensions": scores["strongest_dimensions"],
        "weakest_dimensions":   scores["weakest_dimensions"],
        "patterns":             patterns,
        "primary_failure_point": primary,
        "roadmap":              primary["roadmap"],
        "roadmap_phase_labels": primary["phase_labels"],
        "responses":            responses,
    }