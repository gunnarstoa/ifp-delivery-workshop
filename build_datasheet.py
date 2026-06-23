#!/usr/bin/env python3
"""
IFP Delivery Partner Workshop — 2-Page Datasheet PDF
Anaplan navy/orange styling, ReportLab
Goal: Convince reader to register for the workshop.
"""

from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, NextPageTemplate, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus.flowables import Flowable

W, H = LETTER  # 612 x 792 pt

# ── Brand colours ──────────────────────────────────────────────────────────────
NAVY       = colors.HexColor('#0A2F46')
NAVY2      = colors.HexColor('#0D3B57')
NAVY3      = colors.HexColor('#0F4265')
ORANGE     = colors.HexColor('#FF6100')
BLUE       = colors.HexColor('#0070D2')
LIGHT_BLUE = colors.HexColor('#E8F4FD')
CREAM      = colors.HexColor('#F8F5F0')
GREY_LIGHT = colors.HexColor('#F5F7FA')
GREY_MID   = colors.HexColor('#8C9BAA')
WHITE      = colors.white
DARK_TEXT  = colors.HexColor('#1A2B3C')
ORANGE_BG  = colors.HexColor('#FFF4ED')

MARGIN = 36


# ── Custom Flowables ───────────────────────────────────────────────────────────

class ColorRect(Flowable):
    """Solid colour rectangle."""
    def __init__(self, width, height, fill_color=GREY_LIGHT, radius=4):
        super().__init__()
        self._w = width
        self._h = height
        self._fill = fill_color
        self._r = radius

    def wrap(self, avW, avH):
        return self._w, self._h

    def draw(self):
        self.canv.setFillColor(self._fill)
        self.canv.roundRect(0, 0, self._w, self._h, self._r, fill=1, stroke=0)


def draw_cover_page(c, doc):
    """Full-bleed cover for page 1 — runs as the Cover template's onPage callback.
    Canvas is at absolute page coordinates; no flowable translation."""
    pw, ph = W, H

    # Navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, pw, ph, fill=1, stroke=0)

    # Decorative circles
    c.setFillColor(NAVY2)
    c.circle(pw * 1.05, ph * 0.72, pw * 0.56, fill=1, stroke=0)
    c.setFillColor(NAVY3)
    c.circle(pw * -0.08, ph * 0.12, pw * 0.40, fill=1, stroke=0)

    # Orange accent rule (mid page)
    c.setFillColor(ORANGE)
    c.rect(0, ph * 0.48, pw, 5, fill=1, stroke=0)

    # Orange chip top-left
    c.setFillColor(ORANGE)
    c.roundRect(MARGIN, ph - 56, 220, 24, 4, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(MARGIN + 12, ph - 56 + 8, 'PARTNER DELIVERY  ·  HANDS-ON WORKSHOP')

    # Anaplan wordmark top-right
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 18)
    c.drawRightString(pw - MARGIN, ph - 52, 'anaplan')

    # Hero title
    ty = ph * 0.62
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 46)
    c.drawString(MARGIN, ty + 48, 'Integrated')
    c.drawString(MARGIN, ty,      'Financial')
    c.setFillColor(ORANGE)
    c.drawString(MARGIN, ty - 52, 'Planning 2.1')

    # Subtitle
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 16)
    c.drawString(MARGIN, ph * 0.48 - 30, 'Delivery Partner Workshop')
    c.setFillColor(colors.HexColor('#A8C4D8'))
    c.setFont('Helvetica', 11)
    c.drawString(MARGIN, ph * 0.48 - 50, 'App Framework  ·  Model Generation  ·  Extensions')

    # Stats row (lower half — light section)
    c.setFillColor(WHITE)
    c.rect(0, 0, pw, ph * 0.47, fill=1, stroke=0)

    # Stat boxes
    stats = [
        ('1-2', 'Hrs/Day'),
        ('4', 'Hands-On Exercises'),
        ('44', 'Config Questions'),
        ('~8,000', 'Objects Generated'),
    ]
    box_w = (pw - 2 * MARGIN - 3 * 16) / 4
    bx = MARGIN
    by = ph * 0.47 - 130
    for val, lbl in stats:
        c.setFillColor(GREY_LIGHT)
        c.roundRect(bx, by, box_w, 100, 6, fill=1, stroke=0)
        c.setFillColor(ORANGE)
        c.setFont('Helvetica-Bold', 28)
        c.drawCentredString(bx + box_w / 2, by + 58, val)
        c.setFillColor(NAVY)
        c.setFont('Helvetica', 10)
        c.drawCentredString(bx + box_w / 2, by + 38, lbl)
        # Orange underline
        c.setFillColor(ORANGE)
        c.rect(bx + 12, by + 28, box_w - 24, 3, fill=1, stroke=0)
        bx += box_w + 16

    # Who should attend row
    c.setFillColor(NAVY)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(MARGIN, by - 28, 'Who Should Attend')
    c.setFillColor(GREY_MID)
    c.setFont('Helvetica', 10)
    c.drawString(MARGIN, by - 46, 'Solutions Consultants  ·  Solution Architects  ·  Technical Consultants  ·  Delivery Practitioners')

    # Footer bar
    c.setFillColor(NAVY)
    c.rect(0, 0, pw, 36, fill=1, stroke=0)
    c.setFillColor(WHITE)
    c.setFont('Helvetica', 8)
    c.drawString(MARGIN, 13, 'anaplan.com/partners')
    c.setFillColor(GREY_MID)
    c.drawRightString(pw - MARGIN, 13, '© 2026 Anaplan, Inc.  All rights reserved.')


def draw_content_page(c, doc):
    """Header + footer chrome for page 2 — runs as the Content template's onPage callback."""
    pw, ph = W, H

    # White background
    c.setFillColor(WHITE)
    c.rect(0, 0, pw, ph, fill=1, stroke=0)

    # Navy header strip
    c.setFillColor(NAVY)
    c.rect(0, ph - 72, pw, 72, fill=1, stroke=0)

    # Orange accent line below header
    c.setFillColor(ORANGE)
    c.rect(0, ph - 76, pw, 4, fill=1, stroke=0)

    # Header content
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 15)
    c.drawString(MARGIN, ph - 48, 'IFP 2.1 Delivery Partner Workshop')
    c.setFillColor(colors.HexColor('#A8C4D8'))
    c.setFont('Helvetica', 10)
    c.drawString(MARGIN, ph - 64, 'Curriculum & Exercises Overview')
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 16)
    c.drawRightString(pw - MARGIN, ph - 48, 'anaplan')

    # Footer bar
    c.setFillColor(NAVY)
    c.rect(0, 0, pw, 48, fill=1, stroke=0)
    c.setFillColor(ORANGE)
    c.rect(0, 48, pw, 3, fill=1, stroke=0)

    # Footer text
    c.setFillColor(WHITE)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(MARGIN, 28, 'Want to learn more?')
    c.setFillColor(colors.HexColor('#A8C4D8'))
    c.setFont('Helvetica', 9)
    c.drawString(MARGIN, 14, 'Contact your Anaplan Partner Success Manager for details on upcoming sessions.')
    c.setFillColor(GREY_MID)
    c.setFont('Helvetica', 8)
    c.drawRightString(pw - MARGIN, 14, '© 2026 Anaplan, Inc.  Confidential.')


# ── Document Setup ─────────────────────────────────────────────────────────────

def build_doc():
    out = 'IFP-Delivery-Workshop-Datasheet.pdf'

    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    p2_frame    = Frame(MARGIN, 56, W - 2*MARGIN, H - 56 - 80,
                        leftPadding=0, rightPadding=0,
                        topPadding=12, bottomPadding=12, id='p2_body')

    cover_tmpl = PageTemplate(id='Cover',   frames=[cover_frame], onPage=draw_cover_page)
    p2_tmpl    = PageTemplate(id='Content', frames=[p2_frame],    onPage=draw_content_page)

    doc = BaseDocTemplate(
        out,
        pagesize=LETTER,
        pageTemplates=[cover_tmpl, p2_tmpl],
        leftMargin=0, rightMargin=0,
        topMargin=0, bottomMargin=0,
    )

    # ── Styles ──────────────────────────────────────────────────────────────────
    h1 = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=16, textColor=NAVY,
                        spaceBefore=12, spaceAfter=4)
    h2 = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=11, textColor=NAVY,
                        spaceBefore=10, spaceAfter=3)
    h3 = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=9.5, textColor=ORANGE,
                        spaceBefore=6, spaceAfter=2)
    body = ParagraphStyle('body', fontName='Helvetica', fontSize=9, leading=13,
                          textColor=DARK_TEXT, spaceAfter=4)
    bullet = ParagraphStyle('bullet', fontName='Helvetica', fontSize=9, leading=12,
                            textColor=DARK_TEXT, leftIndent=12, spaceAfter=2,
                            bulletIndent=0)
    small = ParagraphStyle('small', fontName='Helvetica', fontSize=8.5,
                           textColor=GREY_MID, leading=11)
    cta = ParagraphStyle('cta', fontName='Helvetica-Bold', fontSize=11,
                         textColor=WHITE, leading=14, spaceAfter=0)
    tag_style = ParagraphStyle('tag', fontName='Helvetica-Bold', fontSize=8,
                               textColor=WHITE, leading=10)

    story = []

    # ── PAGE 1 (cover — fully painted by draw_cover_page onPage callback) ──
    # A zero-height Spacer gives the Cover frame a flowable so the page renders.
    story.append(Spacer(1, 1))
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())

    # ── PAGE 2 (chrome painted by draw_content_page; flowables fill the body frame) ──

    CONTENT_W = W - 2 * MARGIN
    COL_GAP   = 14
    COL_W     = (CONTENT_W - COL_GAP) / 2

    # ── Left column content ──
    left = []

    left.append(Paragraph('Workshop Overview', h2))
    left.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=6))
    left.append(Paragraph(
        '<b>A practitioner workshop, not a product overview.</b> '
        'Hands-on, self-paced coverage of the complete IFP 2.1 delivery '
        'workflow — Application Framework configuration, model generation, '
        'error log resolution, and building customer-specific extensions '
        'from scratch.',
        body))
    left.append(Paragraph(
        'If you\'ve ever generated an IFP model, hit an error log, and '
        'weren\'t sure whether to escalate or fix it yourself — this '
        'workshop closes that gap. Every exercise uses real planning scenarios: '
        'OpEx/Headcount, Insurance 3-Statement, and Nuclear Plant OpEx.',
        body))

    left.append(Spacer(1, 4))
    left.append(Paragraph('Objectives & Outcomes', h2))
    left.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=6))

    outcomes = [
        'Configure the Application Framework end-to-end and generate a functional IFP model',
        'Triage generation error logs without escalating basics',
        'Build production-grade extensions: direct input + headcount × rate',
        'Apply Configure-vs-Extend-vs-Modify discipline (Anaplan Way for Applications)',
    ]
    for o in outcomes:
        left.append(Paragraph(f'<font color="#FF6100">▶</font>  {o}', bullet))

    left.append(Spacer(1, 4))
    # Prerequisites callout
    prereq_data = [[
        Paragraph('<b>Prerequisites</b>', ParagraphStyle('ph', fontName='Helvetica-Bold',
            fontSize=9, textColor=NAVY, spaceAfter=4)),
        Paragraph(
            'MB, SA, or Master Anaplanner certification · Prior Anaplan model-building '
            'experience · Financial planning literacy (P&L, balance sheet, headcount).',
            ParagraphStyle('pb', fontName='Helvetica', fontSize=8.5,
                textColor=DARK_TEXT, leading=12))
    ]]
    prereq_tbl = Table(prereq_data, colWidths=[80, COL_W - 80])
    prereq_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    left.append(prereq_tbl)

    # ── Right column content ──
    right = []

    right.append(Paragraph('Format & Pace', h2))
    right.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=6))

    pace_data = [[
        Paragraph('<b>Self-paced</b>', ParagraphStyle('ph', fontName='Helvetica-Bold',
            fontSize=9, textColor=NAVY, spaceAfter=4)),
        Paragraph(
            '1-2 hours per day on your own schedule, in any order. <b>Dedicated '
            'training tenant for the week of your registered session</b> — '
            'pre-staged with IFP models, refreshed over the weekend, no extensions. '
            'Plan to start on day 1 of your week.',
            ParagraphStyle('pb', fontName='Helvetica', fontSize=8.5,
                textColor=DARK_TEXT, leading=12))
    ]]
    pace_tbl = Table(pace_data, colWidths=[64, COL_W - 64])
    pace_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BLUE),
        ('ROUNDEDCORNERS', [6]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    right.append(pace_tbl)

    right.append(Spacer(1, 10))
    right.append(Paragraph('Exercises', h2))
    right.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=8))

    labs = [
        {
            'tag': 'EXERCISE:  APPLICATION FRAMEWORK',
            'title': 'Configurator — end-to-end',
            'desc': (
                'All 44 Application Framework questions: entities, currency, '
                'dimensionality, max-level rules, generation. No answer key; '
                'verifies against the post-generation checklist.'
            ),
            'tags': ['Hands-On', 'Core'],
        },
        {
            'tag': 'EXERCISE:  DIRECT INPUT EXTENSION',
            'title': 'Direct Input with two adjustment layers',
            'desc': (
                'Production-grade Direct Input for OpEx + Headcount — drivers, '
                'period locks, audit trails, end-to-end flow through ADO into '
                'the P&L. Data-tagged for version upgrades.'
            ),
            'tags': ['Hands-On', 'Extensions'],
        },
        {
            'tag': 'EXERCISE:  HEADCOUNT × RATE METHOD',
            'title': 'Rate-based headcount planning extension',
            'desc': (
                'Extend Headcount with rate cards — grade-to-rate mapping, '
                'period-by-period comp, validation without touching core. '
                'Practice Extend-vs-Modify + data tagging.'
            ),
            'tags': ['Hands-On', 'Extensions'],
        },
        {
            'tag': 'EXERCISE:  ERROR LOG TRIAGE',
            'title': 'Read, categorize, resolve generation errors',
            'desc': (
                'Realistic generation error logs from production-style mistakes. '
                'Common formula + dependency errors, the fix-regenerate-verify '
                'loop. Resolve independently instead of escalating basics.'
            ),
            'tags': ['Practical Skills'],
        },
    ]

    for lab in labs:
        # Lab card
        tag_cell = Paragraph(
            f'<font color="white"><b>{lab["tag"]}</b></font>',
            ParagraphStyle('lt', fontName='Helvetica-Bold', fontSize=7.5,
                           textColor=WHITE, leading=10)
        )
        title_cell = Paragraph(f'<b>{lab["title"]}</b>',
            ParagraphStyle('ltitle', fontName='Helvetica-Bold', fontSize=10,
                           textColor=NAVY, leading=13, spaceAfter=2))
        desc_cell = Paragraph(lab['desc'],
            ParagraphStyle('ldesc', fontName='Helvetica', fontSize=8.2,
                           textColor=DARK_TEXT, leading=12, spaceAfter=0))

        tags_str = '  ·  '.join(lab['tags'])
        tags_cell = Paragraph(
            f'<font color="#8C9BAA">{tags_str}</font>',
            ParagraphStyle('ltags', fontName='Helvetica', fontSize=7.5,
                           textColor=GREY_MID, leading=10)
        )

        inner = Table(
            [[tag_cell], [title_cell], [desc_cell], [tags_cell]],
            colWidths=[COL_W - 20]
        )
        inner.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (0,0), NAVY),
            ('BACKGROUND',    (0,1), (0,-1), WHITE),
            ('LEFTPADDING',   (0,0), (-1,-1), 10),
            ('RIGHTPADDING',  (0,0), (-1,-1), 10),
            ('TOPPADDING',    (0,0), (0,0), 5),
            ('BOTTOMPADDING', (0,0), (0,0), 5),
            ('TOPPADDING',    (0,1), (-1,-1), 5),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 7),
        ]))

        outer = Table([[inner]], colWidths=[COL_W])
        outer.setStyle(TableStyle([
            ('BOX',           (0,0), (-1,-1), 0.8, colors.HexColor('#C8D4DE')),
            ('ROUNDEDCORNERS', [5]),
            ('TOPPADDING',    (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING',   (0,0), (-1,-1), 0),
            ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ]))

        right.append(outer)
        right.append(Spacer(1, 6))

    # Why IFP 2.1 — full width banner at bottom
    why_text = (
        '<b><font color="#FF6100">Why IFP 2.1?</font></b>  '
        'IFP is delivered through the Application Framework — not built from '
        'scratch. Configuration, generation, and error log triage ARE the '
        'delivery method, not custom modeling. Partners who complete this '
        'workshop generate ~8,000 IFP objects with confidence, resolve '
        'generation errors without escalating, and data-tag every extension '
        'so it survives IFP version upgrades.'
    )

    # ── Assemble two-column layout ─────────────────────────────────────────────
    left_tbl  = Table([[cell] for cell in left],  colWidths=[COL_W])
    right_tbl = Table([[cell] for cell in right], colWidths=[COL_W])

    left_tbl.setStyle(TableStyle([
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    right_tbl.setStyle(TableStyle([
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    two_col = Table([[left_tbl, Spacer(COL_GAP, 1), right_tbl]],
                    colWidths=[COL_W, COL_GAP, COL_W])
    two_col.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(two_col)

    doc.build(story)
    print(f'PDF written → {out}')
    return out


if __name__ == '__main__':
    build_doc()
