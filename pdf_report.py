"""
pdf_report.py — AI Transformation Readiness Intelligence
3-page executive PDF:
  Page 1: Executive Summary — score, primary value barrier, section breakdown
  Page 2: Diagnostic Detail — patterns, evidence signals, priority actions
  Page 3: Transformation Roadmap — 30/60/90 day plan
"""

from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, PageBreak, HRFlowable, KeepTogether,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

NAVY   = colors.HexColor("#0B2E4A")
COBALT = colors.HexColor("#1A56A0")
INK    = colors.HexColor("#111827")
MUTED  = colors.HexColor("#5B6675")
LINE   = colors.HexColor("#D8DEE6")
PANEL  = colors.HexColor("#F7F9FC")
SOFT   = colors.HexColor("#EDF4FA")
ACCENT = colors.HexColor("#C8D8E8")
WHITE  = colors.white
LIGHT  = colors.HexColor("#FBFCFE")

LM = 0.55 * inch
RM = 0.55 * inch
W  = letter[0] - LM - RM


def _c(t):
    return (str(t)
        .replace("\u2014", "-").replace("\u2013", "-")
        .replace("\u2122", "").replace("\u2019", "'")
        .replace("\u201c", '"').replace("\u201d", '"'))

def _p(text, style):
    return Paragraph(_c(text), style)

def _hr(color=LINE, thick=0.4, sb=4, sa=4):
    return HRFlowable(width="100%", thickness=thick,
                      color=color, spaceBefore=sb, spaceAfter=sa)

def _top_rule():
    t = Table([[""]], colWidths=[W], rowHeights=[5])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t

def _flat_tbl(rows, widths, hdr=True):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    cmds = [
        ("GRID",          (0,0),(-1,-1), 0.3,  LINE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
        ("BACKGROUND",    (0,1),(-1,-1), LIGHT),
    ]
    if hdr:
        cmds += [("BACKGROUND",(0,0),(-1,0), NAVY),
                 ("TEXTCOLOR", (0,0),(-1,0), WHITE)]
    t.setStyle(TableStyle(cmds))
    return t

def _no_grid(rows, widths):
    t = Table(rows, colWidths=widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    return t

def _styles():
    B = getSampleStyleSheet()
    def s(n, par="BodyText", **kw):
        return ParagraphStyle(n, parent=B[par], **kw)
    return {
        "eyebrow":    s("ey", fontName="Helvetica",         fontSize=7.5,  leading=9,    textColor=COBALT, spaceAfter=3,  letterSpacing=1.0),
        "title":      s("ti", fontName="Helvetica-Bold",    fontSize=21,   leading=25,   textColor=NAVY,   spaceAfter=4),
        "subtitle":   s("su", fontName="Helvetica",         fontSize=9,    leading=13,   textColor=MUTED,  spaceAfter=6),
        "sec":        s("sc", fontName="Helvetica-Bold",    fontSize=7,    leading=8.5,  textColor=COBALT, spaceAfter=2,  letterSpacing=0.7),
        "h2":         s("h2", fontName="Helvetica-Bold",    fontSize=8.5,  leading=10,   textColor=WHITE),
        "h2_dk":      s("hd", fontName="Helvetica-Bold",    fontSize=8.5,  leading=10,   textColor=NAVY),
        "lbl":        s("lb", fontName="Helvetica-Bold",    fontSize=7,    leading=8.5,  textColor=MUTED,  spaceAfter=1),
        "body":       s("bo", fontName="Helvetica",         fontSize=8.5,  leading=11.5, textColor=INK,    spaceAfter=3),
        "body_sm":    s("bs", fontName="Helvetica",         fontSize=7.8,  leading=10.5, textColor=MUTED,  spaceAfter=2),
        "disc":       s("di", fontName="Helvetica-Oblique", fontSize=7,    leading=9.5,  textColor=MUTED,  spaceAfter=2),
        "bullet":     s("bu", fontName="Helvetica",         fontSize=8.2,  leading=11.5, textColor=INK,    leftIndent=8,  spaceAfter=3),
        "score_num":  s("sn", fontName="Helvetica-Bold",    fontSize=34,   leading=38,   textColor=NAVY,   spaceAfter=1),
        "score_band": s("sb", fontName="Helvetica-Bold",    fontSize=13,   leading=16,   textColor=COBALT, spaceAfter=2),
        "score_desc": s("sd", fontName="Helvetica",         fontSize=8,    leading=10,   textColor=MUTED,  spaceAfter=0),
        "fail_name":  s("fn", fontName="Helvetica-Bold",    fontSize=10,   leading=12,   textColor=NAVY,   spaceAfter=3),
        "fail_lg":    s("fl", fontName="Helvetica-Bold",    fontSize=13,   leading=16,   textColor=NAVY,   spaceAfter=4),
        "rm_hdr":     s("rm", fontName="Helvetica-Bold",    fontSize=8,    leading=10,   textColor=WHITE),
        "footer_r":   s("fr", fontName="Helvetica-Oblique", fontSize=6.8,  leading=9,    textColor=MUTED,  alignment=TA_RIGHT),
    }


def _footer(fl, ST):
    fl.append(_hr(LINE, 0.3, 2, 4))
    ft = _no_grid([[
        _p("Designed by Jaini Desai  -  Workforce Intelligence & AI Enablement  -  linkedin.com/in/jainidesai", ST["disc"]),
        _p(f"AI Transformation Readiness Intelligence  -  {datetime.now().strftime('%d %b %Y')}", ST["footer_r"]),
    ]], [W*0.55, W*0.45])
    fl.append(ft)


def build_pdf(pack, narrative=None):
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter,
                            leftMargin=LM, rightMargin=RM,
                            topMargin=0.44*inch, bottomMargin=0.44*inch)
    ST  = _styles()
    fl  = []
    pri = pack["primary_failure_point"]
    ctx = pack.get("context", {})
    org = pack.get("organization_name", "Your organization")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1 — EXECUTIVE SUMMARY (cover + score + section breakdown)
    # ══════════════════════════════════════════════════════════════════════════
    fl.append(_top_rule())
    fl.append(Spacer(1, 10))
    fl.append(_p("EXECUTIVE SUMMARY  -  FOR DISCUSSION PURPOSES", ST["eyebrow"]))
    fl.append(_p("AI Transformation Readiness Intelligence", ST["title"]))
    fl.append(_p(
        "A structured diagnostic to identify where AI transformation may struggle to create "
        "measurable value - before the organization scales the wrong thing.",
        ST["subtitle"]))

    # Meta strip
    meta = Table([
        [_p("ORGANIZATION", ST["lbl"]), _p("AI JOURNEY", ST["lbl"]),
         _p("TRANSFORMATION OWNERSHIP", ST["lbl"]), _p("GENERATED", ST["lbl"])],
        [_p(org, ST["body"]), _p(ctx.get("C1","Not specified"), ST["body"]),
         _p(ctx.get("C2","Not specified"), ST["body"]),
         _p(datetime.now().strftime("%d %b %Y"), ST["body"])],
    ], colWidths=[W*0.21, W*0.25, W*0.31, W*0.23], hAlign="LEFT")
    meta.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), PANEL),
        ("BACKGROUND",    (0,1),(-1,1), WHITE),
        ("BOX",           (0,0),(-1,-1), 0.3, LINE),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, LINE),
        ("LEFTPADDING",   (0,0),(-1,-1), 8), ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5), ("BOTTOMPADDING",(0,0),(-1,-1), 5),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    fl.append(meta)
    fl.append(Spacer(1, 12))
    fl.append(_hr(LINE, 0.4, 2, 8))

    # Score + Primary Value Barrier — side by side
    score    = pack["overall_score"]
    band_lbl = pack["overall_band"]["label"]

    if score >= 75:   bar_col = colors.HexColor("#22C55E")
    elif score >= 60: bar_col = colors.HexColor("#3B82F6")
    elif score >= 40: bar_col = colors.HexColor("#F59E0B")
    else:             bar_col = colors.HexColor("#EF4444")

    bar_w     = int(round(W * 0.26 * score / 100))
    bar_track = int(round(W * 0.26))
    bar_empty = max(1, bar_track - bar_w)

    bar_inner = Table([["", ""]], colWidths=[bar_w, bar_empty], rowHeights=[8])
    bar_inner.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), bar_col),
        ("BACKGROUND",(1,0),(1,0), ACCENT),
        ("LEFTPADDING",(0,0),(-1,-1),0), ("RIGHTPADDING",(0,0),(-1,-1),0),
        ("TOPPADDING",(0,0),(-1,-1),0),  ("BOTTOMPADDING",(0,0),(-1,-1),0),
    ]))

    score_col = [
        _p("OVERALL READINESS", ST["lbl"]),
        _p(f"{score} / 100", ST["score_num"]),
        _p(band_lbl, ST["score_band"]),
        bar_inner,
        Spacer(1, 3),
        _p(pack["overall_band"]["description"], ST["score_desc"]),
    ]

    barrier_col = [
        _p("MOST LIKELY VALUE BARRIER", ST["lbl"]),
        _p(pri["name"], ST["fail_lg"]),
        _p(pri["summary"], ST["body"]),
        Spacer(1, 6),
        _p("WHAT THIS IMPLIES", ST["lbl"]),
        _p(pri.get("implications", ""), ST["body"]),
    ]

    kpi_tbl = Table([[score_col, barrier_col]],
                    colWidths=[W*0.36, W*0.64], hAlign="LEFT")
    kpi_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SOFT),
        ("BOX",           (0,0),(-1,-1), 0.5, ACCENT),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, ACCENT),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
    ]))
    fl.append(kpi_tbl)
    fl.append(Spacer(1, 12))

    # Section breakdown
    fl.append(_p("SECTION BREAKDOWN", ST["sec"]))
    # Section-specific band descriptions — each speaks to what that section measures
    SECTION_BANDS = {
        "Direction & Value": {
            (75,101): ("Strength",     "Strategy, leadership, and value discipline are aligned. This is a foundation to build from."),
            (60, 75): ("Moderate",     "Direction is set but value accountability is uneven. Some initiatives lack clear owners and outcomes."),
            (40, 60): ("Watch area",   "Strategy and intent exist. The gap is in how AI investment connects to measurable outcomes."),
            (0,  40): ("Priority gap", "AI investment is happening without clear accountability for where value lands."),
        },
        "Adoption & Work": {
            (75,101): ("Strength",     "AI is changing how work gets done — not just what tools people use. This is genuine adoption."),
            (60, 75): ("Moderate",     "Adoption is underway but uneven. Tools are being used; work design is lagging behind."),
            (40, 60): ("Watch area",   "People are engaging with AI. The gap is in whether it is changing how work actually gets done."),
            (0,  40): ("Priority gap", "The conditions for adoption are not in place. Scaling now will accelerate resistance, not results."),
        },
        "Risk & Scale": {
            (75,101): ("Strength",     "Governance, visibility, and change capacity are enabling responsible scale — not blocking it."),
            (60, 75): ("Moderate",     "Some guardrails exist but are inconsistently applied. Shadow AI and change load need attention."),
            (40, 60): ("Watch area",   "Some guardrails are in place. The gap is in whether governance enables scale or quietly blocks it."),
            (0,  40): ("Priority gap", "Governance and change capacity gaps are creating compounding risk as AI activity increases."),
        },
    }

    def _band(sc, section):
        bands = SECTION_BANDS.get(section, {})
        for (lo, hi), (lbl, desc) in bands.items():
            if lo <= sc < hi:
                return lbl, desc
        return "-", ""


    rows = [[_p("Area",ST["h2"]), _p("Score",ST["h2"]),
             _p("Signal",ST["h2"]), _p("Band description",ST["h2"])]]
    for sec, sc in pack["section_scores"].items():
        lbl, desc = _band(sc, sec)
        rows.append([_p(sec,ST["body"]), _p(f"{sc}/100",ST["body"]),
                     _p(lbl,ST["body"]), _p(desc,ST["body_sm"])])
    fl.append(_flat_tbl(rows, [W*0.24, W*0.10, W*0.16, W*0.50]))
    fl.append(Spacer(1, 12))

    # Privacy note on page 1
    fl.append(_hr(LINE, 0.3, 4, 4))
    fl.append(_p(
        "Privacy: This application does not use a database, analytics tracker, or persistent storage layer. "
        "Responses are used only during the active browser session. "
        "Do not enter personal or regulated information.",
        ST["disc"]))

    _footer(fl, ST)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — DIAGNOSTIC DETAIL
    # ══════════════════════════════════════════════════════════════════════════
    fl.append(PageBreak())
    fl.append(_top_rule())
    fl.append(Spacer(1, 8))
    fl.append(_p("DIAGNOSTIC DETAIL  -  " + _c(org).upper(), ST["eyebrow"]))
    fl.append(Spacer(1, 8))

    # Detected value barriers table
    fl.append(_p("DETECTED VALUE BARRIERS", ST["sec"]))
    pat_rows = [[_p("Value barrier", ST["h2"]), _p("What it means", ST["h2"])]]
    for p in pack["patterns"][:5]:
        pat_rows.append([_p(p["name"], ST["body"]), _p(p["summary"], ST["body_sm"])])
    fl.append(_flat_tbl(pat_rows, [W*0.35, W*0.65]))
    fl.append(Spacer(1, 12))

    # Evidence signals
    fl.append(_p("EVIDENCE SIGNALS", ST["sec"]))
    for e in pri.get("evidence", [])[:4]:
        fl.append(_p(f"  {_c(e)}", ST["bullet"]))
    fl.append(Spacer(1, 12))

    # Priority actions
    fl.append(_p("PRIORITY ACTIONS", ST["sec"]))
    seen = []
    for p in pack["patterns"][:3]:
        for a in p.get("actions", []):
            if a not in seen: seen.append(a)
    for a in seen[:6]:
        fl.append(_p(f"  {_c(a)}", ST["bullet"]))

    _footer(fl, ST)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 3 — TRANSFORMATION ROADMAP
    # ══════════════════════════════════════════════════════════════════════════
    fl.append(PageBreak())
    fl.append(_top_rule())
    fl.append(Spacer(1, 8))
    fl.append(_p("TRANSFORMATION ROADMAP  -  " + _c(org).upper(), ST["eyebrow"]))
    fl.append(Spacer(1, 6))

    # Roadmap title banner
    roadmap = pack["roadmap"]
    title_banner = Table([[
        _p("30 / 60 / 90 Day Action Roadmap", ST["fail_name"]),
        _p(f"Primary value barrier: {_c(pri['name'])}", ST["lbl"]),
    ]], colWidths=[W*0.58, W*0.42], hAlign="LEFT")
    title_banner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SOFT),
        ("BOX",           (0,0),(-1,-1), 0.5, ACCENT),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",    (0,0),(-1,-1), 10),
        ("BOTTOMPADDING", (0,0),(-1,-1), 10),
    ]))
    fl.append(title_banner)
    fl.append(Spacer(1, 14))

    # Each phase — full width, one row per action
    # Phase labels come from narrative dict (pattern-specific)
    phase_labels = {}
    if narrative:
        phase_labels = {
            "30": narrative.get("phase_30_label", "30 days — Establish baseline").split(" — ", 1)[-1],
            "60": narrative.get("phase_60_label", "60 days — Embed and equip").split(" — ", 1)[-1],
            "90": narrative.get("phase_90_label", "90 days — Operationalize value").split(" — ", 1)[-1],
        }
    else:
        phase_labels = {
            "30": "Establish baseline",
            "60": "Embed and equip",
            "90": "Operationalize value",
        }

    phases = [
        ("30 DAYS", phase_labels["30"], roadmap["30"]),
        ("60 DAYS", phase_labels["60"], roadmap["60"]),
        ("90 DAYS", phase_labels["90"], roadmap["90"]),
    ]
    for phase_label, phase_sub, items in phases:
        hdr = Table([[
            _p(phase_label, ST["rm_hdr"]),
            _p(phase_sub.upper(), ST["rm_hdr"]),
        ]], colWidths=[W*0.18, W*0.82], hAlign="LEFT")
        hdr.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), NAVY),
            ("LEFTPADDING",   (0,0),(-1,-1), 10),
            ("RIGHTPADDING",  (0,0),(-1,-1), 10),
            ("TOPPADDING",    (0,0),(-1,-1), 7),
            ("BOTTOMPADDING", (0,0),(-1,-1), 7),
            ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ]))
        fl.append(hdr)
        for item in items[:3]:
            row = Table([[_p("-", ST["body"]), _p(_c(item), ST["body"])]],
                        colWidths=[W*0.04, W*0.96], hAlign="LEFT")
            row.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), LIGHT),
                ("LEFTPADDING",   (0,0),(-1,-1), 10),
                ("RIGHTPADDING",  (0,0),(-1,-1), 10),
                ("TOPPADDING",    (0,0),(-1,-1), 6),
                ("BOTTOMPADDING", (0,0),(-1,-1), 6),
                ("VALIGN",        (0,0),(-1,-1), "TOP"),
                ("BOX",           (0,0),(-1,-1), 0.3, LINE),
            ]))
            fl.append(row)
        fl.append(Spacer(1, 12))

    fl.append(_hr(LINE, 0.3, 4, 4))
    fl.append(_p(
        "Diagnostic boundaries: This is an executive readiness diagnostic - not an audit, legal review, "
        "financial forecast, or technical architecture assessment. Analysis is constrained to submitted "
        "responses, dimension-weighted scoring logic, and approved value-barrier detection rules.",
        ST["disc"]))

    _footer(fl, ST)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 4 — EXECUTIVE NARRATIVE (agent-generated, appended at the end)
    # ══════════════════════════════════════════════════════════════════════════
    if narrative:
        fl.append(PageBreak())
        fl.append(_top_rule())
        fl.append(Spacer(1, 10))
        fl.append(_p("EXECUTIVE NARRATIVE  -  " + _c(org).upper(), ST["eyebrow"]))
        fl.append(Spacer(1, 6))

        # Score + barrier banner
        top = Table([[
            [_p("OVERALL READINESS", ST["lbl"]),
             _p(narrative["score_line"], ST["score_band"]),
             _p(narrative["score_desc"], ST["score_desc"])],
            [_p("MOST LIKELY VALUE BARRIER", ST["lbl"]),
             _p(narrative["barrier_name"], ST["fail_lg"]),
             _p(narrative["barrier_body"], ST["body"])],
        ]], colWidths=[W*0.36, W*0.64], hAlign="LEFT")
        top.setStyle(TableStyle([
            ("BACKGROUND",    (0,0),(-1,-1), SOFT),
            ("BOX",           (0,0),(-1,-1), 0.5, ACCENT),
            ("INNERGRID",     (0,0),(-1,-1), 0.3, ACCENT),
            ("VALIGN",        (0,0),(-1,-1), "TOP"),
            ("LEFTPADDING",   (0,0),(-1,-1), 12),
            ("RIGHTPADDING",  (0,0),(-1,-1), 12),
            ("TOPPADDING",    (0,0),(-1,-1), 10),
            ("BOTTOMPADDING", (0,0),(-1,-1), 10),
        ]))
        fl.append(top)
        fl.append(Spacer(1, 12))

        # GPT narrative paragraphs if available
        if narrative.get("gpt_narrative"):
            fl.append(_p("WHAT THE RESULTS MEAN", ST["sec"]))
            for para in narrative["gpt_narrative"].split("\n\n"):
                if para.strip():
                    fl.append(_p(para.strip(), ST["body"]))
            fl.append(Spacer(1, 8))

        # Detected patterns
        fl.append(_p("WHAT THE RESULTS SUGGEST", ST["sec"]))
        for p in narrative["patterns"]:
            fl.append(_p(f"  {_c(p['name'])}  —  {_c(p['summary'])}", ST["bullet"]))
        fl.append(Spacer(1, 10))

        # Priority actions
        fl.append(_p("PRIORITY ACTIONS", ST["sec"]))
        for a in narrative["actions"]:
            fl.append(_p(f"  {_c(a)}", ST["bullet"]))

        _footer(fl, ST)

    doc.build(fl)
    pdf = buf.getvalue()
    buf.close()
    return pdf