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
    c.drawString(MARGIN, ty - 52, 'Planning 2.0')

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
        ('2', 'Full Days'),
        ('4', 'Hands-On Labs'),
        ('3', 'Core Modules'),
        ('~1,200', 'Objects Generated'),
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
    c.drawString(MARGIN, ph - 48, 'IFP 2.0 Delivery Partner Workshop')
    c.setFillColor(colors.HexColor('#A8C4D8'))
    c.setFont('Helvetica', 10)
    c.drawString(MARGIN, ph - 64, 'Curriculum & Labs Overview')
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
        'The IFP 2.0 Delivery Partner Workshop is the hands-on technical program '
        'for Anaplan delivery practitioners. Over two intensive days, participants '
        'master the full IFP 2.0 delivery workflow — from the App Framework '
        'interview-style configurator to model generation, error log review, and '
        'building customer-specific extensions.',
        body))
    left.append(Paragraph(
        'Originally delivered with Elite EPM, this program reflects '
        'real delivery experience — including live questions, instructor commentary, '
        'and the judgment calls that define production readiness.',
        body))

    left.append(Spacer(1, 4))
    left.append(Paragraph('Objectives & Outcomes', h2))
    left.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=6))

    outcomes = [
        'Configure the IFP App Framework for a real customer scenario',
        'Trigger model generation and monitor the 8,000+ object build process',
        'Review and resolve generation error logs with confidence',
        'Build customer extensions without breaking upgrade paths',
        'Apply the Anaplan Way methodology to IFP delivery engagements',
        'Load and validate data through the ADO pipeline',
    ]
    for o in outcomes:
        left.append(Paragraph(f'<font color="#FF6100">▶</font>  {o}', bullet))

    left.append(Spacer(1, 6))
    left.append(Paragraph('Intended Audience', h2))
    left.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=6))

    roles = [
        ('Solutions Consultants', 'Pre-sales and solutioning for IFP opportunities'),
        ('Solution Architects',   'Technical leads for IFP design and delivery'),
        ('Technical Consultants', 'Practitioners configuring and extending IFP'),
        ('Delivery Practitioners','Anyone on a team deploying IFP v2.0'),
    ]
    for role, desc in roles:
        left.append(Paragraph(f'<b>{role}</b>', ParagraphStyle('rh', fontName='Helvetica-Bold',
            fontSize=9.5, textColor=NAVY, leading=13, spaceAfter=0)))
        left.append(Paragraph(desc, ParagraphStyle('rd', fontName='Helvetica', fontSize=8.5,
            textColor=GREY_MID, leading=12, spaceAfter=5, leftIndent=8)))

    left.append(Spacer(1, 4))
    # Prerequisites callout
    prereq_data = [[
        Paragraph('<b>Prerequisites</b>', ParagraphStyle('ph', fontName='Helvetica-Bold',
            fontSize=9, textColor=NAVY, spaceAfter=4)),
        Paragraph(
            'Anaplan platform experience (module building, formulas, lists) · '
            'Basic financial planning knowledge (P&L, balance sheet) · '
            'IFP v2.0 workspace access required for exercises.',
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

    right.append(Paragraph('Time Commitment', h2))
    right.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=6))

    sched_data = [
        ['Day 1', '~8 hours', 'App Framework & Model Generation'],
        ['Day 2', '~8 hours', 'Extensions & Advanced Topics'],
    ]
    sched_tbl = Table(
        [['Day', 'Duration', 'Focus']] + sched_data,
        colWidths=[40, 56, COL_W - 96 - 8]
    )
    sched_tbl.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1,0),  NAVY),
        ('TEXTCOLOR',    (0,0), (-1,0),  WHITE),
        ('FONTNAME',     (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,0),  8),
        ('BACKGROUND',   (0,1), (-1,-1), GREY_LIGHT),
        ('FONTNAME',     (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE',     (0,1), (-1,-1), 8.5),
        ('TEXTCOLOR',    (0,1), (-1,-1), DARK_TEXT),
        ('FONTNAME',     (0,1), (0,-1),  'Helvetica-Bold'),
        ('TEXTCOLOR',    (0,1), (0,-1),  ORANGE),
        ('TOPPADDING',   (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('LEFTPADDING',  (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, GREY_LIGHT]),
        ('BOX',          (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('GRID',         (0,0), (-1,-1), 0.3, colors.HexColor('#E0E5EA')),
    ]))
    right.append(sched_tbl)

    right.append(Spacer(1, 10))
    right.append(Paragraph('Labs & Exercises', h2))
    right.append(HRFlowable(width=COL_W, thickness=2, color=ORANGE, spaceAfter=8))

    labs = [
        {
            'tag': 'LAB A  ·  60 MIN  ·  DAY 1',
            'title': 'App Framework Configurator',
            'desc': (
                'Configure IFP for FintechCo — 3 legal entities, multi-currency, '
                '4 functional areas. Answer all 43 questions, set hierarchy levels, '
                'and trigger model generation. A real judgment exercise — no answer guide.'
            ),
            'tags': ['Hands-On', 'Core'],
        },
        {
            'tag': 'LAB B  ·  45 MIN  ·  DAY 2',
            'title': 'Direct Input & Adjustments',
            'desc': (
                'Build a Direct Input method with two adjustment layers for '
                'FintechCo\'s OpEx module. Configure drivers, lock periods, '
                'and validate data flow through the ADO pipeline to the P&L.'
            ),
            'tags': ['Hands-On', 'Extensions'],
        },
        {
            'tag': 'LAB C  ·  45 MIN  ·  DAY 2',
            'title': 'Headcount × Rate Method',
            'desc': (
                'Extend Headcount with a rate-based planning method. Map employee '
                'grades to rate cards and validate outputs — without touching the base app.'
            ),
            'tags': ['Hands-On', 'Extensions'],
        },
        {
            'tag': 'EXERCISE  ·  DAY 1',
            'title': 'Error Log Review & Resolution',
            'desc': (
                'Read, categorize, and resolve generation error logs. Covers the '
                '5 most common error types and the fix-regenerate-verify loop.'
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

    # Why IFP 2.0 Now — full width banner at bottom
    why_text = (
        '<b><font color="#FF6100">Why IFP 2.0?</font></b>  '
        'The App Framework replaces the legacy numbered configurator pages with an '
        'interview-driven wizard that generates ~8,000 Anaplan objects automatically. '
        'Partners who complete this workshop reduce delivery risk, increase first-run '
        'generation success, and build extensions that survive version upgrades.'
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
