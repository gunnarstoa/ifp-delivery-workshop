#!/usr/bin/env python3
"""
IFP Delivery Partner Workshop — Partner Brief PDF
Anaplan navy/orange styling, ReportLab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame,
    Paragraph, Spacer, Table, TableStyle,
    HRFlowable, NextPageTemplate, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.platypus.flowables import Flowable

W, H = A4  # 595.3 x 841.9 pt

# ── Brand colours ──────────────────────────────────────────────────────────────
NAVY       = colors.HexColor('#0A2F46')
NAVY2      = colors.HexColor('#0D3B57')
NAVY3      = colors.HexColor('#0F4265')
ORANGE     = colors.HexColor('#FF6100')
BLUE       = colors.HexColor('#0070D2')
LIGHT_BLUE = colors.HexColor('#E8F4FD')
CREAM      = colors.HexColor('#F8F5F0')
GREY_LIGHT = colors.HexColor('#F0F2F5')
GREY_MID   = colors.HexColor('#8C9BAA')
WHITE      = colors.white
DARK_TEXT  = colors.HexColor('#1A2B3C')

MARGIN = 40
CONTENT_W = W - 2 * MARGIN  # 515 pt


# ── Styles ─────────────────────────────────────────────────────────────────────
def make_styles():
    body   = ParagraphStyle('body',   fontName='Helvetica',      fontSize=10, leading=15, textColor=DARK_TEXT, spaceAfter=6)
    h2     = ParagraphStyle('h2',     fontName='Helvetica-Bold', fontSize=13, textColor=NAVY, spaceBefore=14, spaceAfter=6)
    small  = ParagraphStyle('small',  fontName='Helvetica',      fontSize=8.5, textColor=GREY_MID, leading=12)
    return body, h2, small


# ── Custom flowables ───────────────────────────────────────────────────────────

class FullPageCover(Flowable):
    """Draws the cover art using the full page canvas — must be placed in a full-page frame."""
    def wrap(self, avW, avH):
        return avW, avH

    def draw(self):
        c = self.canv
        pw, ph = W, H

        # ---- Background ----
        c.setFillColor(NAVY)
        c.rect(0, 0, pw, ph, fill=1, stroke=0)

        # ---- Decorative circles ----
        c.setFillColor(NAVY2)
        c.circle(pw * 1.05, ph * 0.74, pw * 0.58, fill=1, stroke=0)
        c.setFillColor(NAVY3)
        c.circle(pw * -0.08, ph * 0.10, pw * 0.43, fill=1, stroke=0)

        # ---- Orange accent rule ----
        c.setFillColor(ORANGE)
        c.rect(0, ph * 0.45, pw, 5, fill=1, stroke=0)

        # ---- "PARTNER DELIVERY" chip ----
        c.setFillColor(ORANGE)
        c.roundRect(MARGIN, ph - 62, 210, 26, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 10)
        c.drawString(MARGIN + 14, ph - 62 + 8, 'PARTNER DELIVERY WORKSHOP')

        # ---- Anaplan wordmark ----
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 20)
        c.drawRightString(pw - MARGIN, ph - 56, 'anaplan')

        # ---- Main title ----
        ty = ph * 0.59
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 42)
        c.drawString(MARGIN, ty + 44, 'Integrated')
        c.drawString(MARGIN, ty,      'Financial')
        c.setFillColor(ORANGE)
        c.drawString(MARGIN, ty - 48, 'Planning 2.0')

        # ---- Subtitle ----
        c.setFillColor(WHITE)
        c.setFont('Helvetica', 17)
        c.drawString(MARGIN, ph * 0.45 - 32, 'Delivery Partner Workshop')
        c.setFillColor(colors.HexColor('#A8C4D8'))
        c.setFont('Helvetica', 12)
        c.drawString(MARGIN, ph * 0.45 - 54, 'App Framework  ·  Model Generation  ·  Extensions')

        # ---- Stats row ----
        stats = [('2', 'Days'), ('3', 'Hands-On Labs'), ('6', 'Delivery Phases'), ('43', 'Config Questions')]
        sx = MARGIN
        sy = ph * 0.16
        bw = (pw - 2 * MARGIN) / 4
        for num, label in stats:
            c.setFillColor(colors.HexColor('#0C3450'))
            c.roundRect(sx + 4, sy, bw - 8, 68, 6, fill=1, stroke=0)
            c.setFillColor(ORANGE)
            c.setFont('Helvetica-Bold', 30)
            c.drawCentredString(sx + bw / 2, sy + 34, num)
            c.setFillColor(colors.HexColor('#A8C4D8'))
            c.setFont('Helvetica', 10)
            c.drawCentredString(sx + bw / 2, sy + 18, label)
            sx += bw

        # ---- Bottom bar ----
        c.setFillColor(colors.HexColor('#051C2C'))
        c.rect(0, 0, pw, 52, fill=1, stroke=0)
        c.setFillColor(GREY_MID)
        c.setFont('Helvetica', 9)
        c.drawString(MARGIN, 19, 'Anaplan Partner Enablement  ·  IFP Delivery Certification Track')
        c.drawRightString(pw - MARGIN, 19, 'Confidential — Partner Use Only')


class SectionBanner(Flowable):
    def __init__(self, text, w=CONTENT_W):
        super().__init__()
        self.text = text
        self.bw = w

    def wrap(self, avW, avH):
        return self.bw, 38

    def draw(self):
        c = self.canv
        c.setFillColor(NAVY)
        c.rect(0, 0, self.bw, 38, fill=1, stroke=0)
        c.setFillColor(ORANGE)
        c.rect(0, 0, 5, 38, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 14)
        c.drawString(18, 13, self.text)


class OutcomeCard(Flowable):
    def __init__(self, num, text, w):
        super().__init__()
        self.num = num
        self.text = text
        self.cw = w
        self.ch = 64

    def wrap(self, avW, avH):
        return self.cw, self.ch

    def draw(self):
        c = self.canv
        c.setFillColor(LIGHT_BLUE)
        c.roundRect(0, 0, self.cw, self.ch, 6, fill=1, stroke=0)
        # orange circle
        c.setFillColor(ORANGE)
        c.circle(28, self.ch / 2, 17, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 15)
        c.drawCentredString(28, self.ch / 2 - 5, str(self.num))
        # text
        c.setFillColor(DARK_TEXT)
        c.setFont('Helvetica', 9)
        words = self.text.split()
        lines, line = [], ''
        max_w = self.cw - 58
        for w_ in words:
            test = (line + ' ' + w_).strip()
            if c.stringWidth(test, 'Helvetica', 9) < max_w:
                line = test
            else:
                lines.append(line)
                line = w_
        if line:
            lines.append(line)
        total_h = len(lines) * 12
        ty = self.ch / 2 + total_h / 2 - 4
        for ln in lines:
            c.drawString(52, ty, ln)
            ty -= 12


class DayBlock(Flowable):
    def __init__(self, label, hdr_color, rows, w):
        super().__init__()
        self.label = label
        self.hdr_color = hdr_color
        self.rows = rows
        self.bw = w
        self.row_h = 22
        self.bh = 48 + len(rows) * self.row_h + 10

    def wrap(self, avW, avH):
        return self.bw, self.bh

    def draw(self):
        c = self.canv
        # card bg
        c.setFillColor(GREY_LIGHT)
        c.roundRect(0, 0, self.bw, self.bh, 6, fill=1, stroke=0)
        # header
        c.setFillColor(self.hdr_color)
        c.roundRect(0, self.bh - 46, self.bw, 46, 6, fill=1, stroke=0)
        c.rect(0, self.bh - 46, self.bw, 20, fill=1, stroke=0)  # flatten bottom half
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 13)
        c.drawString(14, self.bh - 28, self.label)
        # rows
        y = self.bh - 46 - self.row_h
        alt = False
        fmt_x = self.bw - 8
        fmt_col_w = 56  # reserved width for format label
        topic_max_x = fmt_x - fmt_col_w - 4
        for time, topic, fmt in self.rows:
            if alt:
                c.setFillColor(colors.HexColor('#E4E8ED'))
                c.rect(0, y, self.bw, self.row_h, fill=1, stroke=0)
            c.setFillColor(DARK_TEXT)
            c.setFont('Helvetica-Bold', 8)
            c.drawString(10, y + 7, time)
            # Clip topic text to available width
            c.setFont('Helvetica', 8)
            topic_str = topic
            while c.stringWidth(topic_str, 'Helvetica', 8) > (topic_max_x - 76) and len(topic_str) > 8:
                topic_str = topic_str[:-4] + '\u2026'
            c.drawString(76, y + 7, topic_str)
            c.setFillColor(GREY_MID)
            c.setFont('Helvetica-Oblique', 7.5)
            c.drawRightString(fmt_x, y + 7, fmt)
            y -= self.row_h
            alt = not alt


# ── Build ──────────────────────────────────────────────────────────────────────

def build():
    out = ('/home/gstoa/.openclaw/workspace/projects/work/workshops/'
           'ifp-delivery-workshop/IFP-Delivery-Partner-Brief.pdf')

    doc = BaseDocTemplate(out, pagesize=A4)

    # Cover template — zero margins, full-page frame
    cover_frame = Frame(0, 0, W, H, leftPadding=0, rightPadding=0,
                        topPadding=0, bottomPadding=0, id='cover')
    cover_tpl = PageTemplate(id='Cover', frames=[cover_frame])

    # Content template — normal margins
    content_frame = Frame(MARGIN, MARGIN, CONTENT_W, H - 2 * MARGIN,
                          leftPadding=0, rightPadding=0,
                          topPadding=0, bottomPadding=0, id='content')
    content_tpl = PageTemplate(id='Content', frames=[content_frame],
                                onPage=_draw_content_footer)

    doc.addPageTemplates([cover_tpl, content_tpl])

    body, h2, small = make_styles()

    story = []

    # ── COVER ──────────────────────────────────────────────────────────────────
    story.append(FullPageCover())
    story.append(NextPageTemplate('Content'))
    story.append(PageBreak())

    # ── PAGE 2: About + Who + Format ──────────────────────────────────────────
    story.append(SectionBanner('About This Workshop'))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        'The <b>IFP Delivery Partner Workshop</b> is a two-day, hands-on practitioner '
        'programme for Anaplan partner consultants implementing — or preparing to implement — '
        '<b>Integrated Financial Planning 2.0</b> for customers.',
        body))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Built on the <b>App Framework</b>, IFP 2.0 replaces hand-crafted model builds with a '
        'configuration-driven approach: 43 guided questions determine your model\'s complete '
        'architecture — hierarchies, financial modules, planning methods, and data structure. '
        'The workshop walks you through every step: configurator walkthrough, model generation, '
        'error-log review, post-generation verification, and two hands-on extension labs.',
        body))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'This is not a product overview. By the end of Day 2, you will have configured, '
        'generated, and extended a real IFP model in a live training tenant.',
        ParagraphStyle('emph', parent=body, fontName='Helvetica-Bold', textColor=NAVY)))
    story.append(Spacer(1, 18))

    # Who it's for
    story.append(Paragraph('Who Should Attend', h2))
    who = [
        ['Role', 'Relevant If…'],
        ['IFP Delivery Consultant',
         'You are implementing or expect to implement IFP for a customer in the next 12 months'],
        ['Solution Architect',
         'You design IFP architectures and want hands-on depth in App Framework configuration'],
        ['Senior Model Builder',
         'You build IFP extensions and need to understand upgrade-safe extension patterns'],
    ]
    wt = Table(who, colWidths=[138, CONTENT_W - 138])
    wt.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, 0), NAVY),
        ('TEXTCOLOR',   (0, 0), (-1, 0), WHITE),
        ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, -1), 9),
        ('FONTNAME',    (0, 1), (0, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR',   (0, 1), (0, -1), NAVY),
        ('FONTNAME',    (1, 1), (1, -1), 'Helvetica'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, CREAM]),
        ('TOPPADDING',  (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('GRID',        (0, 0), (-1, -1), 0.4, colors.HexColor('#C8D4DC')),
        ('VALIGN',      (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(wt)
    story.append(Spacer(1, 18))

    # Prerequisites
    story.append(Paragraph('Prerequisites', h2))
    prereqs = [
        '✔  Active Anaplan workspace admin access — confirmed before Day 1',
        '✔  Model Builder (MB), Solution Architect (SA), or Master Anaplanner certification',
        '✔  Prior experience building or configuring Anaplan models',
        '✔  Familiarity with financial planning concepts (P&L, balance sheet, headcount)',
    ]
    pt = Table([[Paragraph(p, body)] for p in prereqs], colWidths=[CONTENT_W])
    pt.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), LIGHT_BLUE),
        ('TOPPADDING',   (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 5),
        ('LEFTPADDING',  (0, 0), (-1, -1), 12),
        ('LINEBELOW',    (0, 0), (-1, -2), 0.3, colors.HexColor('#C8DCF0')),
    ]))
    story.append(pt)
    story.append(Spacer(1, 18))

    # Format pills
    story.append(Paragraph('Format & Time Commitment', h2))
    fmt_items = [
        ('<b>Format</b><br/>Instructor-led,<br/>hands-on in a live training tenant',),
        ('<b>Duration</b><br/>2 full days<br/>(approx. 6–7 hrs each)',),
        ('<b>Access</b><br/>Credentialed Anaplan<br/>delivery partners',),
        ('<b>Certification</b><br/>Counts toward IFP<br/>delivery cert requirement',),
    ]
    fp = [Paragraph(t[0], ParagraphStyle('fp', fontName='Helvetica', fontSize=9,
                                          textColor=WHITE, leading=14)) for t in fmt_items]
    ft = Table([fp], colWidths=[CONTENT_W / 4] * 4)
    ft.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), NAVY),
        ('TOPPADDING',   (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 12),
        ('LEFTPADDING',  (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEAFTER',    (0, 0), (-2, -1), 0.5, colors.HexColor('#1A4A6A')),
    ]))
    story.append(ft)

    # ── PAGE 3: Outcomes ───────────────────────────────────────────────────────
    story.append(Spacer(1, 24))
    story.append(SectionBanner("What You'll Be Able to Do"))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        'Six verifiable, practitioner-level outcomes — each maps directly to a real '
        'delivery scenario you will encounter on a customer engagement.',
        body))
    story.append(Spacer(1, 10))

    outcomes = [
        (1, 'Configure the IFP App Framework end-to-end — 43 questions answered, model architecture defined, generation triggered.'),
        (2, 'Read, interpret, and resolve generation error logs without escalating basic formula errors to Anaplan support.'),
        (3, 'Build a multi-layer adjustment extension on the Direct Input planning method — correctly tagged, upgrade-safe.'),
        (4, 'Build a Headcount × Rate planning method from scratch — module structure, formula logic, and UX wiring.'),
        (5, 'Map the six Anaplan Way delivery phases for IFP and know which configuration decisions belong in each phase.'),
        (6, 'Apply the 7 extension best practices that keep IFP models upgradeable across App Framework version releases.'),
    ]

    cw = (CONTENT_W - 10) / 2
    for i in range(0, len(outcomes), 2):
        pair = outcomes[i:i+2]
        cells = [OutcomeCard(n, t, cw - 4) for n, t in pair]
        if len(cells) == 1:
            cells.append(Spacer(cw, 64))
        rt = Table([cells], colWidths=[cw, cw])
        rt.setStyle(TableStyle([
            ('LEFTPADDING',  (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (0, -1), 10),
            ('TOPPADDING',   (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING',(0, 0), (-1, -1), 8),
            ('VALIGN',       (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(rt)

    story.append(Spacer(1, 8))
    # Cert callout
    cert_t = Table([[Paragraph(
        '🎓  <b>Completing this workshop counts toward your IFP delivery certification</b> '
        'in the Anaplan Partner Program.',
        ParagraphStyle('cert', fontName='Helvetica', fontSize=9.5, textColor=DARK_TEXT, leading=14)
    )]], colWidths=[CONTENT_W])
    cert_t.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), colors.HexColor('#E8F7EE')),
        ('TOPPADDING',   (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 12),
        ('LEFTPADDING',  (0, 0), (-1, -1), 16),
    ]))
    story.append(cert_t)

    # ── PAGE 4: 2-Day Schedule ─────────────────────────────────────────────────
    story.append(Spacer(1, 22))
    story.append(SectionBanner('Two-Day Workshop Structure'))
    story.append(Spacer(1, 12))

    d1 = DayBlock('Day 1 — Configuration', NAVY, [
        ('35 min',  'IFP Overview + Anaplan Way for IFP',              'Tell / Show'),
        ('45 min',  'App Framework Configurator Walkthrough',           'Guided'),
        ('60 min',  'Lab A: Configurator Exercise — FintechCo',        'Hands-On Lab'),
        ('30 min',  'Model Generation',                                 'Demo + Do'),
        ('20 min',  'Post-Generation Checklist',                        'Checklist'),
        ('60 min',  'Error Log Review + Hands-On Lab',                  'Hands-On Lab'),
    ], CONTENT_W)
    d2 = DayBlock('Day 2 — Extensions', ORANGE, [
        ('30 min',  'Extensions Overview + 7 Best Practices',          'Tell / Show'),
        ('45 min',  'Lab B: Direct Input + Adjustments Extension',      'Hands-On Lab'),
        ('60 min',  'Lab C: Headcount × Rate Planning Method',          'Hands-On Lab'),
        ('60 min',  'Knowledge Check + Debrief',                        'Discussion'),
        ('30 min',  'IFP Roadmap — What\'s Coming',                    'Briefing'),
        ('—',       'Q&A + Wrap-Up',                                    ''),
    ], CONTENT_W)
    story.append(d1)
    story.append(Spacer(1, 10))
    story.append(d2)
    story.append(Spacer(1, 14))

    # TSD legend — keep intro + table together
    tsd_rows = [
        [Paragraph('<b>Tell</b>', ParagraphStyle('tsdl', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
         Paragraph('Facilitator explains the concept — what it is and why it matters for IFP delivery', body)],
        [Paragraph('<b>Show</b>', ParagraphStyle('tsdl2', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
         Paragraph('Live demonstration in the training tenant — follow along in your own workspace', body)],
        [Paragraph('<b>Do</b>', ParagraphStyle('tsdl3', fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)),
         Paragraph('Independent hands-on exercise — complete the task, raise blockers, debrief with peers', body)],
    ]
    tt = Table(tsd_rows, colWidths=[50, CONTENT_W - 50])
    tt.setStyle(TableStyle([
        ('FONTSIZE',  (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 0), (-1, -1), [WHITE, CREAM]),
        ('TOPPADDING',   (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 7),
        ('LEFTPADDING',  (0, 0), (-1, -1), 9),
        ('LINEBELOW', (0, 0), (-1, -2), 0.3, colors.HexColor('#D0D8E0')),
    ]))
    from reportlab.platypus import KeepTogether
    story.append(KeepTogether([
        Paragraph('All sessions follow the <b>Tell · Show · Do</b> instructional design model:', body),
        Spacer(1, 4),
        tt,
    ]))

    # ── PAGE 5: Why IFP + CTA ──────────────────────────────────────────────────
    story.append(Spacer(1, 22))
    story.append(SectionBanner('Why IFP — and Why Now'))
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        'IFP 2.0 is Anaplan\'s next-generation finance application. Built on the App Framework, '
        'it replaces hand-crafted model builds with a configuration-driven approach — the same '
        '43 questions shape the architecture for every customer. Implementations are faster, '
        'more consistent, and upgradeable as Anaplan releases new capabilities.',
        body))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        'For partners, this is a meaningful shift in how IFP delivery works. Partners who '
        'train now position themselves ahead of growing customer demand.',
        body))
    story.append(Spacer(1, 14))

    why_rows = [
        ['Only <b>14</b>',      'IFP-credentialed delivery resources exist in the global partner ecosystem today — massive opportunity'],
        ['<b>43 questions</b>', 'determine the complete model architecture — knowing them cold separates great IFP partners from mediocre ones'],
        ['<b>4 models</b>',     'generated in a single operation: P&amp;L, Balance Sheet, Headcount, and OpEx — all from one configurator run'],
        ['<b>Upgrade-safe</b>', 'extension patterns mean your customisations survive App Framework version releases without rework'],
    ]
    for cells in why_rows:
        row = Table(
            [[Paragraph(cells[0], ParagraphStyle('wn', fontName='Helvetica-Bold',
                fontSize=11, textColor=ORANGE)),
              Paragraph(cells[1], body)]],
            colWidths=[130, CONTENT_W - 130])
        row.setStyle(TableStyle([
            ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING',   (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING',(0, 0), (-1, -1), 9),
            ('LEFTPADDING',  (0, 0), (-1, -1), 10),
            ('LINEBELOW',    (0, 0), (-1, -1), 0.3, colors.HexColor('#D0D8E0')),
        ]))
        story.append(row)

    story.append(Spacer(1, 20))

    # CTA box
    cta = Table([[Paragraph(
        '<b>Ready to certify your delivery team?</b><br/>'
        'Contact your Partner Success Manager to register for the next cohort.<br/>'
        'Seats are limited — early registration is recommended.<br/><br/>'
        '<b>Online lab guide:</b>  https://gunnarstoa.github.io/ifp-delivery-workshop/',
        ParagraphStyle('cta', fontName='Helvetica', fontSize=10,
                       textColor=WHITE, leading=16)
    )]], colWidths=[CONTENT_W])
    cta.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, -1), NAVY),
        ('TOPPADDING',   (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 20),
        ('LEFTPADDING',  (0, 0), (-1, -1), 22),
        ('RIGHTPADDING', (0, 0), (-1, -1), 22),
    ]))
    story.append(cta)
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width=CONTENT_W, thickness=0.5, color=GREY_MID))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Anaplan Partner Enablement  ·  IFP Delivery Certification Track  ·  '
        'Confidential — Partner Use Only  ·  © 2026 Anaplan, Inc.',
        small))

    doc.build(story)
    print(f'✅  PDF written → {out}')


def _draw_content_footer(c, doc):
    """Draw page number on content pages."""
    c.saveState()
    c.setFillColor(GREY_MID)
    c.setFont('Helvetica', 8)
    c.drawRightString(W - MARGIN, 22, f'Page {doc.page}')
    c.restoreState()


if __name__ == '__main__':
    build()
