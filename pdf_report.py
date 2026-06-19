"""
pdf_report.py — AI Transformation Readiness Intelligence
100% flat platypus build. No nested lists in table cells.
No custom Flowables. Renders in all viewers including Google Drive.
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
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

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
W  = letter[0] - LM - RM   # ≈ 502 pt


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


def _styles():
    B = getSampleStyleSheet()
    def s(n, par="BodyText", **kw):
        return ParagraphStyle(n, parent=B[par], **kw)
    return {
        "eyebrow":    s("ey", fontName="Helvetica",         fontSize=7.5,  leading=9,    textColor=COBALT, spaceAfter=3,  letterSpacing=1.0),
        "title":      s("ti", fontName="Helvetica-Bold",    fontSize=21,   leading=25,   textColor=NAVY,   spaceAfter=4),
        "subtitle":   s("su", fontName="Helvetica",         fontSize=9,    leading=13,   textColor=MUTED,  spaceAfter=8),
        "sec":        s("sc", fontName="Helvetica-Bold",    fontSize=7,    leading=8.5,  textColor=COBALT, spaceAfter=2,  letterSpacing=0.7),
        "h2":         s("h2", fontName="Helvetica-Bold",    fontSize=8.5,  leading=10,   textColor=WHITE),
        "h2_dk":      s("hd", fontName="Helvetica-Bold",    fontSize=8.5,  leading=10,   textColor=NAVY),
        "lbl":        s("lb", fontName="Helvetica-Bold",    fontSize=7,    leading=8.5,  textColor=MUTED,  spaceAfter=1),
        "lbl_co":     s("lc", fontName="Helvetica-Bold",    fontSize=7,    leading=8.5,  textColor=COBALT, spaceAfter=1),
        "body":       s("bo", fontName="Helvetica",         fontSize=8.5,  leading=11.5, textColor=INK,    spaceAfter=3),
        "body_sm":    s("bs", fontName="Helvetica",         fontSize=7.8,  leading=10.5, textColor=MUTED,  spaceAfter=2),
        "disc":       s("di", fontName="Helvetica-Oblique", fontSize=7,    leading=9.5,  textColor=MUTED,  spaceAfter=2),
        "bullet":     s("bu", fontName="Helvetica",         fontSize=8.2,  leading=11,   textColor=INK,    leftIndent=8,  spaceAfter=2),
        "score_num":  s("sn", fontName="Helvetica-Bold",    fontSize=34,   leading=38,   textColor=NAVY,   spaceAfter=2),
        "score_band": s("sb", fontName="Helvetica-Bold",    fontSize=9,    leading=11,   textColor=COBALT, spaceAfter=0),
        "fail_name":  s("fn", fontName="Helvetica-Bold",    fontSize=10,   leading=12,   textColor=NAVY,   spaceAfter=3),
        "rm_hdr":     s("rm", fontName="Helvetica-Bold",    fontSize=7.8,  leading=9.5,  textColor=WHITE),
        "footer_r":   s("fr", fontName="Helvetica-Oblique", fontSize=6.8,  leading=9,    textColor=MUTED,  alignment=TA_RIGHT),
    }


def _top_rule():
    t = Table([[""]], colWidths=[W], rowHeights=[5])
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


def build_pdf(pack, report_text=None):
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=LM, rightMargin=RM,
        topMargin=0.44 * inch, bottomMargin=0.44 * inch,
    )
    ST  = _styles()
    fl  = []
    pri = pack["primary_failure_point"]
    ctx = pack.get("context", {})
    org = pack.get("organization_name", "Your organization")

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 1
    # ══════════════════════════════════════════════════════════════════════════
    fl.append(_top_rule())
    fl.append(Spacer(1, 10))
    fl.append(_p("EXECUTIVE DIAGNOSTIC  -  CONFIDENTIAL", ST["eyebrow"]))
    fl.append(_p("AI Transformation Readiness Intelligence", ST["title"]))
    fl.append(_p(
        "A structured diagnostic to identify the most likely reason AI transformation "
        "fails to create measurable value - before the organisation scales the wrong thing.",
        ST["subtitle"]))

    # Meta strip
    meta = Table([
        [_p("ORGANISATION", ST["lbl"]), _p("AI JOURNEY", ST["lbl"]),
         _p("TRANSFORMATION OWNERSHIP", ST["lbl"]), _p("GENERATED", ST["lbl"])],
        [_p(org, ST["body"]), _p(ctx.get("C1","Not specified"), ST["body"]),
         _p(ctx.get("C2","Not specified"), ST["body"]),
         _p(datetime.now().strftime("%d %b %Y  %H:%M"), ST["body"])],
    ], colWidths=[W*0.21, W*0.25, W*0.31, W*0.23], hAlign="LEFT")
    meta.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), PANEL),
        ("BACKGROUND",    (0,1),(-1,1), WHITE),
        ("BOX",           (0,0),(-1,-1), 0.3, LINE),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, LINE),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 5),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
    ]))
    fl.append(meta)
    fl.append(Spacer(1, 10))

    # Context declaration
    fl.append(_hr(COBALT, 0.8, 4, 6))
    fl.append(_p("WHAT THIS DIAGNOSTIC IS FOR", ST["sec"]))
    fl.append(_p(
        "The technology is deployed. AI is in your organisation. "
        "The question is whether your organisation is in AI.",
        ST["body"]))
    fl.append(_p(
        "Being in AI means AI is embedded in how your organisation makes decisions, designs work, "
        "measures value, and develops people. It is not a technology condition - it is an "
        "organisational one. This diagnostic measures that gap. Complete it in 10-15 minutes. "
        "Use the results to focus on what actually matters.",
        ST["body"]))

    fl.append(Spacer(1, 4))
    fl.append(_p("DATA HANDLING AND PRIVACY", ST["sec"]))
    fl.append(_p(
        "No responses, identity, or organisational data are stored, cached, or transmitted beyond "
        "the active session. This application contains no database, analytics tracker, or persistent "
        "storage layer. If an AI narrative is generated, only the structured evidence pack "
        "(scores and patterns - no personally identifying information) is sent to the configured model. "
        "All data is cleared when the browser session ends.",
        ST["disc"]))

    fl.append(_hr(LINE, 0.4, 8, 6))

    # Score block — flat two-column table, no nested structures
    score     = pack["overall_score"]
    band_lbl  = pack["overall_band"]["label"]

    if score >= 75:   bar_col = colors.HexColor("#22C55E")
    elif score >= 60: bar_col = colors.HexColor("#3B82F6")
    elif score >= 40: bar_col = colors.HexColor("#F59E0B")
    else:             bar_col = colors.HexColor("#EF4444")

    bar_w     = int(round(W * 0.50 * score / 100))
    bar_track = int(round(W * 0.50))
    bar_empty = max(1, bar_track - bar_w)

    bar_inner = Table(
        [["", ""]],
        colWidths=[bar_w, bar_empty],
        rowHeights=[9],
    )
    bar_inner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(0,0), bar_col),
        ("BACKGROUND",    (1,0),(1,0), ACCENT),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))

    score_tbl = Table([
        [_p("OVERALL READINESS", ST["lbl"]),
         _p("READINESS INDICATOR", ST["lbl"])],
        [_p(f"{score} / 100", ST["score_num"]),
         bar_inner],
        [_p(band_lbl.upper(), ST["score_band"]),
         _p(f"{score}% readiness score", ST["body_sm"])],
    ], colWidths=[W*0.38, W*0.62], hAlign="LEFT")
    score_tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SOFT),
        ("BOX",           (0,0),(-1,-1), 0.5, ACCENT),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, ACCENT),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LEFTPADDING",   (0,0),(-1,-1), 12),
        ("RIGHTPADDING",  (0,0),(-1,-1), 12),
        ("TOPPADDING",    (0,0),(-1,-1), 8),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
        ("SPAN",          (0,1),(0,2)),   # score number spans rows
    ]))
    fl.append(score_tbl)
    fl.append(Spacer(1, 10))

    # Section breakdown
    fl.append(_p("SECTION BREAKDOWN", ST["sec"]))
    band_map = [
        (75,101,"Strength",    "Conditions in place to move from pilots to sustained adoption."),
        (60, 75,"Moderate",    "Positioned to progress; specific bottlenecks could limit scale."),
        (40, 60,"Watch area",  "Foundation exists; path from activity to value not yet reliable."),
        (0,  40,"Priority gap","Material execution risk unless core conditions are strengthened."),
    ]
    def _band(sc):
        for lo,hi,lbl,desc in band_map:
            if lo <= sc < hi: return lbl, desc
        return "-", ""

    rows = [[_p("Area",ST["h2"]), _p("Score",ST["h2"]),
             _p("Signal",ST["h2"]), _p("Band description",ST["h2"])]]
    for sec, sc in pack["section_scores"].items():
        lbl, desc = _band(sc)
        rows.append([_p(sec,ST["body"]), _p(f"{sc}/100",ST["body"]),
                     _p(lbl,ST["body"]), _p(desc,ST["body_sm"])])
    t = Table(rows, colWidths=[W*0.24,W*0.10,W*0.16,W*0.50], hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
        ("BACKGROUND",    (0,1),(-1,-1), LIGHT),
        ("GRID",          (0,0),(-1,-1), 0.3, LINE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
    ]))
    fl.append(t)

    # ══════════════════════════════════════════════════════════════════════════
    # PAGE 2 — completely flat, no nested lists in cells
    # ══════════════════════════════════════════════════════════════════════════
    fl.append(PageBreak())
    fl.append(_top_rule())
    fl.append(Spacer(1, 8))
    fl.append(_p("DIAGNOSTIC OUTPUT  -  " + _c(org).upper(), ST["eyebrow"]))
    fl.append(Spacer(1, 6))

    # Primary failure banner — two plain cells
    banner = Table([
        [_p("MOST LIKELY FAILURE POINT", ST["lbl"]),
         _p("WHAT THIS IMPLIES", ST["lbl"])],
        [_p(pri["name"], ST["fail_name"]),
         _p(pri.get("implications",""), ST["body"])],
        [_p(pri["summary"], ST["body"]),
         _p("", ST["body"])],
    ], colWidths=[W*0.44, W*0.56], hAlign="LEFT")
    banner.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), SOFT),
        ("BOX",           (0,0),(-1,-1), 0.5, ACCENT),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, ACCENT),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 10),
        ("RIGHTPADDING",  (0,0),(-1,-1), 10),
        ("TOPPADDING",    (0,0),(-1,-1), 7),
        ("BOTTOMPADDING", (0,0),(-1,-1), 7),
        ("SPAN",          (1,1),(1,2)),
    ]))
    fl.append(banner)
    fl.append(Spacer(1, 10))

    # Detected failure patterns — simple flat table
    fl.append(_p("DETECTED FAILURE PATTERNS", ST["sec"]))
    pat_rows = [[_p("Pattern", ST["h2"]), _p("What it means", ST["h2"])]]
    for p in pack["patterns"][:5]:
        pat_rows.append([
            _p(p["name"], ST["body"]),
            _p(p["summary"], ST["body_sm"]),
        ])
    pt = Table(pat_rows, colWidths=[W*0.35, W*0.65], hAlign="LEFT")
    pt.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), NAVY),
        ("TEXTCOLOR",     (0,0),(-1,0), WHITE),
        ("BACKGROUND",    (0,1),(-1,-1), LIGHT),
        ("GRID",          (0,0),(-1,-1), 0.3, LINE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 5),
        ("BOTTOMPADDING", (0,0),(-1,-1), 6),
    ]))
    fl.append(pt)
    fl.append(Spacer(1, 8))

    # Evidence signals — flat paragraphs
    fl.append(_p("EVIDENCE SIGNALS", ST["sec"]))
    for e in pri.get("evidence", [])[:4]:
        fl.append(_p(f"  {_c(e)}", ST["bullet"]))
    fl.append(Spacer(1, 6))

    # Priority actions — flat paragraphs
    fl.append(_p("PRIORITY ACTIONS", ST["sec"]))
    seen = []
    for p in pack["patterns"][:3]:
        for a in p.get("actions", []):
            if a not in seen: seen.append(a)
    for a in seen[:5]:
        fl.append(_p(f"  {_c(a)}", ST["bullet"]))
    fl.append(Spacer(1, 8))

    # Roadmap — simple 2-row table, plain paragraph cells only
    fl.append(_hr(COBALT, 0.6, 4, 6))
    roadmap = pack["roadmap"]
    fl.append(_p(
        f"30 / 60 / 90 DAY ROADMAP  -  {_c(pri['name']).upper()}",
        ST["sec"]))

    def _rm(items):
        return "\n".join([f"  {_c(x)}" for x in items[:3]])

    rm = Table([
        [_p("30 DAYS - Establish baseline",   ST["rm_hdr"]),
         _p("60 DAYS - Embed and equip",      ST["rm_hdr"]),
         _p("90 DAYS - Operationalise value", ST["rm_hdr"])],
        [_p(_rm(roadmap["30"]), ST["body_sm"]),
         _p(_rm(roadmap["60"]), ST["body_sm"]),
         _p(_rm(roadmap["90"]), ST["body_sm"])],
    ], colWidths=[W/3, W/3, W/3], hAlign="LEFT")
    rm.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,0), NAVY),
        ("BACKGROUND",    (0,1),(-1,1), PANEL),
        ("BOX",           (0,0),(-1,-1), 0.3, LINE),
        ("INNERGRID",     (0,0),(-1,-1), 0.3, LINE),
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 8),
        ("RIGHTPADDING",  (0,0),(-1,-1), 8),
        ("TOPPADDING",    (0,0),(-1,-1), 6),
        ("BOTTOMPADDING", (0,0),(-1,-1), 8),
    ]))
    fl.append(rm)
    fl.append(Spacer(1, 8))

    # Footer — two plain paragraphs in a flat table
    fl.append(_hr(LINE, 0.3, 2, 4))
    ft = Table([[
        _p("Designed by Jaini Desai  -  Workforce Intelligence & AI Enablement",
           ST["disc"]),
        _p(f"AI Transformation Readiness Intelligence  -  {datetime.now().strftime('%d %b %Y')}",
           ST["footer_r"]),
    ]], colWidths=[W*0.55, W*0.45], hAlign="LEFT")
    ft.setStyle(TableStyle([
        ("VALIGN",        (0,0),(-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0),(-1,-1), 0),
        ("RIGHTPADDING",  (0,0),(-1,-1), 0),
        ("TOPPADDING",    (0,0),(-1,-1), 0),
        ("BOTTOMPADDING", (0,0),(-1,-1), 0),
    ]))
    fl.append(ft)

    doc.build(fl)
    pdf = buf.getvalue()
    buf.close()
    return pdf