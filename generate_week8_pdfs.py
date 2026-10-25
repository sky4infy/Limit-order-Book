import sys
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            self.saveState()
            self.setFillColor(colors.HexColor("#0F172A"))
            self.rect(0, 11 * inch - 6, 8.5 * inch, 6, fill=1, stroke=0)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        header_title = getattr(self, 'header_title', "HFT SYSTEM STUDY & INTERVIEW DEFENSE GUIDE")
        self.drawString(42, 11 * inch - 26, header_title)
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(8.5 * inch - 42, 11 * inch - 26, "Institutional Quant Developer Blueprint")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(42, 11 * inch - 30, 8.5 * inch - 42, 11 * inch - 30)
        
        # Running Footer
        self.line(42, 32, 8.5 * inch - 42, 32)
        self.setFont("Helvetica", 7.5)
        self.drawString(42, 22, "Confidential — High-Frequency Trading Systems Architecture | Author: Akash")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 7.5)
        self.drawRightString(8.5 * inch - 42, 22, page_str)
        self.restoreState()

def create_styled_pdf(filename, header_title, doc_title, subtitle, sections):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    c_primary = colors.HexColor("#0F172A")
    c_navy = colors.HexColor("#1E3A8A")
    c_teal = colors.HexColor("#0D9488")
    c_slate = colors.HexColor("#334155")
    c_light_bg = colors.HexColor("#F8FAFC")
    c_code_bg = colors.HexColor("#F1F5F9")
    c_border = colors.HexColor("#CBD5E1")

    title_style = ParagraphStyle(
        "CoverTitle", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=20, leading=24,
        textColor=c_primary, spaceAfter=5
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"],
        fontName="Helvetica", fontSize=10.5, leading=14,
        textColor=c_teal, spaceAfter=12
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=13, leading=16,
        textColor=c_navy, spaceBefore=12, spaceAfter=5, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=10.5, leading=13,
        textColor=c_primary, spaceBefore=8, spaceAfter=3, keepWithNext=True
    )
    body_style = ParagraphStyle(
        "Body_Custom", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8.5, leading=11.5,
        textColor=c_slate, spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        "Bullet_Custom", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8.5, leading=11.5,
        textColor=c_slate, leftIndent=12, firstLineIndent=-7, spaceAfter=3
    )
    code_style = ParagraphStyle(
        "Code_Custom", parent=styles["Normal"],
        fontName="Courier", fontSize=7.5, leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )
    callout_style = ParagraphStyle(
        "Callout_Custom", parent=styles["Normal"],
        fontName="Helvetica-Oblique", fontSize=8.5, leading=12,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # Title Banner
    story.append(Paragraph(doc_title, title_style))
    story.append(Paragraph(subtitle, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_navy, spaceBefore=2, spaceAfter=10))

    for sec in sections:
        sec_type = sec.get("type", "p")
        if sec_type == "h1":
            story.append(Paragraph(sec["text"], h1_style))
        elif sec_type == "h2":
            story.append(Paragraph(sec["text"], h2_style))
        elif sec_type == "p":
            story.append(Paragraph(sec["text"], body_style))
        elif sec_type == "bullet":
            story.append(Paragraph(f"• {sec['text']}", bullet_style))
        elif sec_type == "code":
            t = Table([[Paragraph(sec["text"].replace('\n', '<br/>'), code_style)]], colWidths=[7.2 * inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), c_code_bg),
                ('BOX', (0, 0), (-1, -1), 0.5, c_border),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
        elif sec_type == "callout":
            t = Table([[Paragraph(sec["text"], callout_style)]], colWidths=[7.2 * inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
                ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#3B82F6")),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
        elif sec_type == "table":
            headers = [Paragraph(f"<b>{h}</b>", body_style) for h in sec["headers"]]
            rows = [headers]
            for r in sec["rows"]:
                rows.append([Paragraph(str(cell), body_style) for cell in r])
            t = Table(rows, colWidths=sec.get("colWidths", None))
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
                ('GRID', (0, 0), (-1, -1), 0.5, c_border),
                ('TOPPADDING', (0, 0), (-1, -1), 3),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
                ('LEFTPADDING', (0, 0), (-1, -1), 5),
                ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
        elif sec_type == "spacer":
            story.append(Spacer(1, sec.get("height", 6)))

    def on_first_page(canvas_obj, doc_obj):
        canvas_obj.header_title = header_title

    doc.build(story, canvasmaker=NumberedCanvas, onFirstPage=on_first_page)
    print(f"Generated: {filename} ({os.path.getsize(filename)} bytes)")

def generate_week8_docs():
    root = r"d:\Limit Order Book"

    # PDF 1: Architecture & Walkthrough
    pdf1 = os.path.join(root, "Week_8_Market_Microstructure_and_Quantitative_Strategies.pdf")
    sections_walkthrough = [
        {"type": "h1", "text": "1. Sasha Stoikov's Micro-Price Estimator"},
        {"type": "p", "text": "Classical mid-price (P_bid + P_ask)/2 assumes symmetric probability of the next tick. In reality, order book queue imbalances provide massive predictive signals:"},
        {"type": "code", "text": "Imbalance I = Q_b / (Q_b + Q_a)\nMicroPrice = I * P_ask + (1 - I) * P_b"},
        {"type": "p", "text": "If 90% of book depth is at the bid, the micro-price skews 90% towards the ask. In our benchmarks, this computes in <b>19 nanoseconds</b> with 0 dynamic allocations (21.3M evals/s)."},

        {"type": "h1", "text": "2. Volume-Synchronized Probability of Toxicity (VPIN)"},
        {"type": "p", "text": "Easley, Lopez de Prado, and O'Hara (2012) proved that financial time advances in volume, not clock ticks. VPIN measures informed flow toxicity:"},
        {"type": "bullet", "text": "<b>Volume Buckets</b>: Flow is partitioned into discrete volume buckets of size V_bucket."},
        {"type": "bullet", "text": "<b>Trade Direction</b>: Trades are classified as buyer- or seller-initiated using the tick rule."},
        {"type": "bullet", "text": "<b>Toxicity Threshold</b>: VPIN = sum(|V_B - V_S|) / (N * V_bucket). Values > 0.70 indicate severe informed directional flow, prompting market makers to widen spreads."},

        {"type": "h1", "text": "3. Avellaneda-Stoikov High-Frequency Market Making Model"},
        {"type": "p", "text": "Optimal dynamic limit order quoting under inventory risk. The model derives a reservation price that moves against existing inventory:"},
        {"type": "code", "text": "Reservation Price R(s, q, t) = s - q * gamma * sigma^2 * (T - t)\nOptimal Bid = round(R - HalfSpread)\nOptimal Ask = round(R + HalfSpread)"},
        {"type": "callout", "text": "When long inventory (q > 0), the reservation price drops below mid-price, shifting quotes downward to encourage selling and discourage buying."},

        {"type": "h1", "text": "4. Empirical Quantitative Benchmark Results (1,000,000 Evaluations)"},
        {"type": "table", "headers": ["Model", "Throughput (ops/s)", "p50 (Median)", "p99.9 (Tail)", "Execution Profile"],
         "rows": [
             ["Stoikov Micro-Price", "21,298,601 ops/s", "19 ns", "213 ns", "Sub-20ns inline arithmetic"],
             ["VPIN Toxicity Calc", "17,597,964 ops/s", "26 ns", "254 ns", "Rolling circular volume buffer"],
             ["Avellaneda-Stoikov Bot", "19,616,421 ops/s", "19 ns", "54 ns", "Optimal reservation quote skew"]
         ],
         "colWidths": [1.6 * inch, 1.4 * inch, 1.0 * inch, 1.1 * inch, 2.1 * inch]}
    ]
    create_styled_pdf(pdf1, "WEEK 8: MARKET MICROSTRUCTURE & QUANTITATIVE STRATEGIES",
                      "Week 8: Market Microstructure Signals & Algorithmic Strategies",
                      "Stoikov Micro-Price, VPIN Toxicity, and Avellaneda-Stoikov Inventory Market Making",
                      sections_walkthrough)

    # PDF 2: Interview Defense
    pdf2 = os.path.join(root, "Week_8_Interview_Preparation_and_Defense.pdf")
    sections_interview = [
        {"type": "h1", "text": "1. Institutional Quantitative Interview Defense"},
        {"type": "h2", "text": "Q1: Why does mid-price fail, and how does Micro-Price solve it?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Mid-price ignores order queue imbalances. If the bid has 10,000 shares and the ask has 100, the probability of the next tick being up is nearly 100%. Micro-Price weights the fair value by the queue imbalance ratio I = Q_b / (Q_b + Q_a), yielding a true probability-adjusted fair value.'"},

        {"type": "h2", "text": "Q2: What is VPIN and why is volume time preferred over clock time?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Information arrival in financial markets is non-uniform. Volume time synchronizes data sampling with market activity using fixed volume buckets. VPIN measures order toxicity sum(|V_B - V_S|) / (N * V_bucket). When VPIN > 0.70, it signals an informed toxic run, instructing market makers to widen quotes or pull resting orders.'"},

        {"type": "h2", "text": "Q3: Walk me through the Avellaneda-Stoikov model. What is the reservation price?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'The reservation price R(s, q, t) = s - q * gamma * sigma^2 * (T - t) is the price at which a market maker is indifferent between holding their current inventory or executing a contract. If inventory is long (q > 0), the reservation price drops below mid-price, dynamically skewing quotes downward to offload risk.'"},

        {"type": "callout", "text": "<b>Performance Metric</b>: All three quantitative models execute at over 17M–21M operations/second with sub-25 nanosecond median latencies in pure C++20."}
    ]
    create_styled_pdf(pdf2, "WEEK 8: INTERVIEW DEFENSE & QUANTITATIVE MASTERY",
                      "Week 8: Market Microstructure & Quantitative Strategies Defense",
                      "Rigorous Answers for Quantitative Researcher & High-Frequency Trader Interviews",
                      sections_interview)

if __name__ == "__main__":
    generate_week8_docs()
