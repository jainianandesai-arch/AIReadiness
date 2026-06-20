import streamlit as st
from questions import CONTEXT_QUESTIONS, QUESTIONS, SECTION_ORDER
from scoring import calculate_scores
from report_generator import generate_report
from pdf_report import build_pdf

st.set_page_config(
    page_title="AI Transformation Readiness Intelligence",
    page_icon="◈",
    layout="wide",
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  --navy:   #0B2E4A;
  --navy2:  #123B5A;
  --cobalt: #1A56A0;
  --ink:    #111827;
  --muted:  #5B6675;
  --line:   #E2E8F0;
  --panel:  #F8FAFC;
  --soft:   #EDF4FA;
}

*, *::before, *::after { box-sizing: border-box; }

.block-container {
  padding-top: 0 !important;
  padding-bottom: 2rem;
  max-width: 1200px;
}
[data-testid="stHeader"] { background: transparent; }

/* ── Top accent bar ── */
.top-bar {
  height: 5px;
  background: var(--navy);
  margin: 0 -1rem 1.4rem -1rem;
}

/* ── Header ── */
.app-eyebrow {
  font-size: .70rem;
  font-weight: 700;
  color: var(--cobalt);
  letter-spacing: .10em;
  text-transform: uppercase;
  margin: 0 0 .35rem 0;
}
.app-title {
  font-size: 1.85rem;
  line-height: 2.2rem;
  font-weight: 780;
  color: var(--navy);
  letter-spacing: -0.03em;
  margin: 0 0 .35rem 0;
}
.app-subtitle {
  font-size: .96rem;
  line-height: 1.55rem;
  color: var(--muted);
  max-width: 860px;
  margin: 0 0 1.2rem 0;
}

/* ── Privacy banner ── */
.privacy-banner {
  background: #F0F7FF;
  border: 1px solid #BDD6F0;
  border-left: 4px solid var(--cobalt);
  border-radius: 10px;
  padding: .75rem 1rem;
  margin-bottom: 1.2rem;
  font-size: .84rem;
  line-height: 1.45rem;
  color: var(--ink);
}
.privacy-banner strong { color: var(--navy); }

/* ── Section headings ── */
.sec-label {
  font-size: .70rem;
  font-weight: 800;
  color: var(--cobalt);
  letter-spacing: .09em;
  text-transform: uppercase;
  margin: 1.2rem 0 .5rem 0;
  padding-bottom: .25rem;
  border-bottom: 1px solid var(--line);
}

/* ── Context cards ── */
.ctx-card {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1rem 1.1rem 1rem 1.1rem;
  height: 100%;
}
.ctx-card-label {
  font-size: .68rem;
  font-weight: 800;
  color: var(--cobalt);
  letter-spacing: .09em;
  text-transform: uppercase;
  margin-bottom: .3rem;
}
.ctx-card-title {
  font-size: .88rem;
  font-weight: 680;
  color: var(--ink);
  margin-bottom: .55rem;
  line-height: 1.3rem;
}
.ctx-note {
  font-size: .76rem;
  color: var(--muted);
  margin-top: .3rem;
}

/* ── Context card gap ── */
.ctx-card { margin-bottom: .5rem; }

/* ── Question cards — remove blank top space ── */
.q-card {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: .75rem 1rem .85rem 1rem;
  margin-bottom: .75rem;
  transition: border-color .15s;
}
.q-card:hover { border-color: #B8CDE8; }
.q-card > div:empty { display: none !important; }
[data-testid="stVerticalBlock"] > div:empty { display: none !important; }
.q-meta {
  font-size: .67rem;
  font-weight: 800;
  color: var(--cobalt);
  letter-spacing: .09em;
  text-transform: uppercase;
  margin-bottom: .22rem;
}
.q-text {
  font-size: .92rem;
  font-weight: 640;
  color: var(--ink);
  line-height: 1.35rem;
  margin-bottom: .55rem;
}

/* ── Tab nudge ── */
.tab-nudge {
  background: #F0F7FF;
  border: 1px solid #BDD6F0;
  border-radius: 8px;
  padding: .5rem .85rem;
  font-size: .80rem;
  color: var(--cobalt);
  margin-bottom: .75rem;
}

/* ── App footer attribution ── */
.app-footer {
  margin-top: 2.5rem;
  padding-top: .75rem;
  border-top: 1px solid var(--line);
  font-size: .72rem;
  color: var(--muted);
  letter-spacing: .03em;
}
.app-footer span { color: var(--cobalt); font-weight: 700; }

/* ── Executive narrative card ── */
.narr-card {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1.4rem 1.6rem;
  margin-bottom: 1.2rem;
}
.narr-score-line {
  font-size: 1.15rem;
  font-weight: 780;
  color: var(--navy);
  margin-bottom: .2rem;
}
.narr-score-desc {
  font-size: .88rem;
  color: var(--muted);
  margin-bottom: 0;
}
.narr-divider {
  border-top: 1px solid var(--line);
  margin: .9rem 0;
}
.narr-sec-label {
  font-size: .67rem;
  font-weight: 800;
  color: var(--cobalt);
  letter-spacing: .09em;
  text-transform: uppercase;
  margin-bottom: .4rem;
}
.narr-barrier-name {
  font-size: 1.05rem;
  font-weight: 740;
  color: var(--navy);
  margin-bottom: .3rem;
}
.narr-barrier-body {
  font-size: .88rem;
  color: var(--ink);
  line-height: 1.5rem;
}
.narr-pattern {
  font-size: .86rem;
  color: var(--ink);
  line-height: 1.45rem;
  margin-bottom: .3rem;
  padding-left: .5rem;
  border-left: 2px solid var(--cobalt);
}
.narr-action {
  font-size: .86rem;
  color: var(--ink);
  line-height: 1.45rem;
  margin-bottom: .3rem;
}
.narr-rm-phase {
  font-size: .80rem;
  font-weight: 700;
  color: var(--navy);
  margin: .6rem 0 .2rem 0;
  text-transform: uppercase;
  letter-spacing: .04em;
}
.narr-rm-item {
  font-size: .85rem;
  color: var(--ink);
  line-height: 1.45rem;
  margin-bottom: .2rem;
  padding-left: .5rem;
}
.narr-boundary {
  font-size: .74rem;
  color: var(--muted);
  font-style: italic;
  margin-top: .9rem;
  padding-top: .7rem;
  border-top: 1px solid var(--line);
  line-height: 1.4rem;
}

/* ── Radio overrides ── */
div[role="radiogroup"] label {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 9px;
  padding: .36rem .52rem;
  margin-bottom: .22rem;
  font-size: .84rem !important;
  line-height: 1.2rem !important;
  transition: background .12s, border-color .12s;
}
div[role="radiogroup"] label:hover {
  border-color: #A0BCE0;
  background: #EDF4FA;
}
[data-testid="stRadio"] { margin-top: -.15rem; }
[data-testid="stRadio"] p { font-size: .84rem; line-height: 1.18rem; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
.stTabs [data-baseweb="tab"] {
  border-radius: 8px 8px 0 0;
  padding: .5rem .85rem;
  background: var(--panel);
  color: var(--navy);
  font-size: .86rem;
  font-weight: 650;
  border: 1px solid transparent;
  border-bottom: none;
}
.stTabs [aria-selected="true"] {
  background: #fff !important;
  border-color: var(--line) var(--line) #fff !important;
  color: var(--cobalt) !important;
}

/* ── Buttons ── */
.stButton > button {
  background: var(--navy);
  color: #fff;
  border-radius: 10px;
  padding: .7rem 1.1rem;
  font-weight: 700;
  font-size: .9rem;
  border: 0;
  letter-spacing: .01em;
}
.stButton > button:hover { background: var(--navy2); color: #fff; border: 0; }
.stDownloadButton > button {
  border-radius: 10px;
  font-weight: 640;
}

/* ── KPI cards ── */
.kpi-card {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 1rem 1.1rem;
}
.kpi-label {
  font-size: .67rem;
  font-weight: 800;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: .09em;
  margin-bottom: .28rem;
}
.kpi-value {
  font-size: 1.45rem;
  line-height: 1.7rem;
  font-weight: 780;
  color: var(--navy);
  letter-spacing: -.02em;
}
.kpi-caption { color: var(--muted); font-size: .82rem; margin-top: .3rem; }
.kpi-band { color: var(--cobalt); font-size: 1.0rem; font-weight: 700; margin-top: .2rem; letter-spacing: -.01em; }

/* ── Signal box ── */
.signal-box {
  background: #fff;
  border: 1px solid var(--line);
  border-left: 3px solid var(--cobalt);
  border-radius: 10px;
  padding: .7rem .9rem;
  margin-bottom: .55rem;
  font-size: .85rem;
  color: var(--ink);
  line-height: 1.3rem;
}

hr { border: none; border-top: 1px solid var(--line); margin: 1.0rem 0; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Session defaults ─────────────────────────────────────────────────────────
for q in QUESTIONS:
    st.session_state.setdefault(q["id"], 3)
for cq in CONTEXT_QUESTIONS:
    st.session_state.setdefault(cq["id"], cq["options"][1])
st.session_state.setdefault("organization_name", "")

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown('<div class="top-bar"></div>', unsafe_allow_html=True)
st.markdown('<div class="app-eyebrow">Executive diagnostic</div>', unsafe_allow_html=True)
st.markdown('<div class="app-title">AI Transformation Readiness Intelligence</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">'
    'Most organizations have AI tools. Few have AI transformation.<br/><br/>'
    'The technology is deployed. AI is in your organization. The question is whether your organization is in AI.<br/><br/>'
    'Being in AI means AI is embedded in how your organization makes decisions, designs work, measures value, '
    'and develops people. It is not a technology condition — it is an organizational one. '
    'This diagnostic helps identify where AI value may get stuck — across leadership, workflow, governance, '
    'measurement, manager capability, and the path from pilot to scale.'
    '</div>',
    unsafe_allow_html=True,
)

# ── Privacy banner ───────────────────────────────────────────────────────────
st.markdown(
    '<div class="privacy-banner">'
    '<strong>Privacy &amp; data handling:</strong> This application does not use a database, '
    'analytics tracker, or persistent storage layer. Responses are used only during the active '
    'browser session to generate the diagnostic. If an AI narrative is generated, only a structured '
    'evidence pack containing scores and detected patterns is sent to the configured model. '
    'Do not enter confidential, personal, or regulated information.'
    '</div>',
    unsafe_allow_html=True,
)

# ── Organization context ─────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Organization context</div>', unsafe_allow_html=True)

ctx1, ctx2, ctx3 = st.columns([1.0, 1.4, 1.4], gap="medium")

with ctx1:
    st.markdown('<div class="ctx-card"><div class="ctx-card-label">Organization</div>'
                '<div class="ctx-card-title">Name or placeholder</div>', unsafe_allow_html=True)
    org = st.text_input(
        "org_name",
        value=st.session_state.organization_name,
        placeholder="e.g. Acme Financial Group",
        key="organization_name_input",
        label_visibility="collapsed",
    )
    st.session_state.organization_name = org.strip() if org and org.strip() else "Your organization"
    st.markdown('<div class="ctx-note">Use a placeholder for demos. Do not enter confidential names.</div>'
                '</div>', unsafe_allow_html=True)

for idx, cq in enumerate(CONTEXT_QUESTIONS):
    with [ctx2, ctx3][idx]:
        st.markdown(
            f'<div class="ctx-card"><div class="ctx-card-label">{cq["label"]}</div>'
            f'<div class="ctx-card-title">{cq["question"]}</div>',
            unsafe_allow_html=True,
        )
        current = st.session_state.get(cq["id"], cq["options"][1])
        st.radio(
            cq["question"],
            cq["options"],
            key=cq["id"],
            index=cq["options"].index(current),
            label_visibility="collapsed",
        )
        st.markdown('</div>', unsafe_allow_html=True)

# ── Diagnostic questions ──────────────────────────────────────────────────────
st.markdown('<div class="sec-label">Diagnostic questions</div>', unsafe_allow_html=True)
st.caption("Work through each section. All five answer options stay visible — no dropdowns.")

tabs = st.tabs([f"{i+1}. {sec}" for i, sec in enumerate(SECTION_ORDER)])

for idx, section in enumerate(SECTION_ORDER):
    with tabs[idx]:
        qs = [q for q in QUESTIONS if q["section"] == section]
        total_sections = len(SECTION_ORDER)
        if idx < total_sections - 1:
            next_sec = SECTION_ORDER[idx + 1]
            st.markdown(
                f'<div class="tab-nudge">&#9654;&nbsp; '
                f'<strong>Section {idx+1} of {total_sections}</strong> — '
                f'complete all questions below, then move to <strong>{next_sec}</strong> before generating your report.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="tab-nudge">&#10003;&nbsp; '
                '<strong>Final section</strong> — complete these questions, then click '
                '<strong>Generate executive diagnostic</strong> below.</div>',
                unsafe_allow_html=True,
            )
        left, right = st.columns(2, gap="large")
        for qi, q in enumerate(qs):
            with [left, right][qi % 2]:
                st.markdown('<div class="q-card">', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="q-meta">{q["id"]} · {q["short"]}</div>'
                    f'<div class="q-text">{q["question"]}</div>',
                    unsafe_allow_html=True,
                )
                st.radio(
                    q["question"],
                    options=[1, 2, 3, 4, 5],
                    index=st.session_state.get(q["id"], 3) - 1,
                    format_func=lambda x, q=q: q["options"][x - 1],
                    key=q["id"],
                    label_visibility="collapsed",
                )
                st.markdown('</div>', unsafe_allow_html=True)

# ── Generate ──────────────────────────────────────────────────────────────────
st.markdown("---")
run_col, note_col = st.columns([1.2, 1.8], gap="large")
with run_col:
    run = st.button("Generate executive diagnostic", use_container_width=True)
with note_col:
    st.caption(
        "Demo guidance: do not enter confidential, personal, or regulated information. "
        "The report is constrained to submitted responses, scoring logic, and approved pattern rules."
    )

if run:
    responses = {q["id"]: st.session_state[q["id"]] for q in QUESTIONS}
    context   = {cq["id"]: st.session_state[cq["id"]] for cq in CONTEXT_QUESTIONS}
    scores    = calculate_scores(responses)
    report_md, pack, mode = generate_report(
        scores, responses, context, st.session_state.organization_name
    )
    st.session_state["last_report_md"] = report_md
    st.session_state["last_pack"]      = pack
    st.session_state["last_mode"]      = mode

# ── Output ────────────────────────────────────────────────────────────────────
if "last_pack" in st.session_state:
    pack      = st.session_state["last_pack"]
    narrative = st.session_state["last_report_md"]
    mode      = st.session_state["last_mode"]
    primary   = pack["primary_failure_point"]

    st.markdown("---")
    st.markdown('<div class="sec-label">Executive diagnostic output</div>', unsafe_allow_html=True)

    # ── Executive narrative — clean HTML, no markdown ─────────────────────────
    # Opening — use GPT interpretation if available, otherwise structured data
    if narrative.get("gpt_narrative"):
        opening_html = f'<div class="narr-barrier-body">{narrative["gpt_narrative"]}</div>'
    else:
        opening_html = (
            f'<div class="narr-barrier-name">{narrative["barrier_name"]}</div>'
            f'<div class="narr-barrier-body">{narrative["barrier_body"]}</div>'
        )

    patterns_html = "".join(
        f'<div class="narr-pattern"><strong>{p["name"]}</strong> — {p["summary"]}</div>'
        for p in narrative["patterns"]
    )
    actions_html = "".join(
        f'<div class="narr-action">&#9654;&nbsp; {a}</div>'
        for a in narrative["actions"]
    )
    def rm_items(items):
        return "".join(f'<div class="narr-rm-item">&#8212;&nbsp; {x}</div>' for x in items)

    st.markdown(f"""
<div class="narr-card">
  <div class="narr-score-line">{narrative["score_line"]}</div>
  <div class="narr-score-desc">{narrative["score_desc"]}</div>

  <div class="narr-divider"></div>

  <div class="narr-sec-label">MOST LIKELY VALUE BARRIER</div>
  {opening_html}

  <div class="narr-divider"></div>

  <div class="narr-sec-label">WHAT THE RESULTS SUGGEST</div>
  {patterns_html}

  <div class="narr-divider"></div>

  <div class="narr-sec-label">PRIORITY ACTIONS</div>
  {actions_html}

  <div class="narr-divider"></div>

  <div class="narr-sec-label">30 / 60 / 90 DAY ROADMAP — {narrative["roadmap_label"].upper()}</div>
  <div class="narr-rm-phase">{narrative["phase_30_label"]}</div>
  {rm_items(narrative["roadmap_30"])}
  <div class="narr-rm-phase">{narrative["phase_60_label"]}</div>
  {rm_items(narrative["roadmap_60"])}
  <div class="narr-rm-phase">{narrative["phase_90_label"]}</div>
  {rm_items(narrative["roadmap_90"])}

  <div class="narr-boundary">{narrative["boundary"]}</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("---")

    # ── KPI cards ─────────────────────────────────────────────────────────────
    k1, k2, k3 = st.columns([.9, 1.35, 1.1], gap="medium")
    with k1:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Overall readiness</div>'
            f'<div class="kpi-value">{pack["overall_score"]}/100</div>'
            f'<div class="kpi-band">{pack["overall_band"]["label"]}</div>'
            f'<div class="kpi-caption">{pack["overall_band"]["description"]}</div></div>',
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Most likely value barrier</div>'
            f'<div class="kpi-value">{primary["name"]}</div>'
            f'<div class="kpi-caption">{primary["summary"]}</div></div>',
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            f'<div class="kpi-card"><div class="kpi-label">Diagnostic mode</div>'
            f'<div class="kpi-value">{mode}</div>'
            f'<div class="kpi-caption">Constrained to submitted responses and approved pattern rules.</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:.9rem"></div>', unsafe_allow_html=True)
    p1, p2 = st.columns([1.1, 1], gap="large")

    with p1:
        st.markdown('<div class="sec-label" style="margin-top:0">Readiness profile</div>',
                    unsafe_allow_html=True)
        for section, score in pack["section_scores"].items():
            st.caption(f"{section}: {score}/100")
            st.progress(score / 100)

        st.markdown('<div class="sec-label">Evidence signals</div>', unsafe_allow_html=True)
        for e in primary.get("evidence", [])[:3]:
            st.markdown(f'<div class="signal-box">{e}</div>', unsafe_allow_html=True)

    with p2:
        st.markdown('<div class="sec-label" style="margin-top:0">Priority actions</div>',
                    unsafe_allow_html=True)
        seen = []
        for p in pack["patterns"][:3]:
            for a in p.get("actions", []):
                if a not in seen:
                    seen.append(a)
        for a in seen[:5]:
            st.write(f"- {a}")

        with st.expander("Detected value barriers", expanded=False):
            for p in pack["patterns"][:5]:
                st.markdown(f"**{p['name']}**")
                st.caption(p["summary"])

    pdf_bytes = build_pdf(pack, narrative)
    st.download_button(
        "Download executive PDF",
        data=pdf_bytes,
        file_name="ai_transformation_readiness_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )
else:
    st.info("Complete the diagnostic and click **Generate executive diagnostic**.")

# ── Attribution footer ────────────────────────────────────────────────────────
st.markdown(
    '<div class="app-footer">'
    'Designed by <span>Jaini Desai</span> &nbsp;·&nbsp; Workforce Intelligence &amp; AI Enablement'
    ' &nbsp;·&nbsp; <a href="https://www.linkedin.com/in/jainidesai" target="_blank" '
    'style="color:var(--cobalt);text-decoration:none;font-weight:600;">LinkedIn Profile</a>'
    '</div>',
    unsafe_allow_html=True,
)