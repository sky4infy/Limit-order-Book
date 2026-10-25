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

def generate_week10_docs():
    root = r"d:\Limit Order Book"

    # PDF 1: Superday Defense & Resume Guide
    pdf1 = os.path.join(root, "Week_10_Superday_Interview_Defense_and_Resume.pdf")
    sections = [
        {"type": "h1", "text": "1. Institutional Quantitative Developer Resume Bullets"},
        {"type": "bullet", "text": "<b>Production Matching Engine</b>: Engineered deterministic C++20 engine processing 9.56M ops/s at 47ns median latency on an invariant TSC-calibrated testbed."},
        {"type": "bullet", "text": "<b>Zero-Allocation Architecture</b>: Custom SlabAllocator and 131,072-level DirectPriceLadder with 2-level 64-bit hierarchical bitmasks for O(1) BBO price discovery using hardware LZCNT intrinsics."},
        {"type": "bullet", "text": "<b>Lock-Free Concurrency</b>: Disruptor Single-Writer core with SPSC ring buffers and alignas(64) false sharing elimination, dropping ingress p99 latency from 1.94ms to 30µs (98% reduction)."},
        {"type": "bullet", "text": "<b>Wire Protocols</b>: Zero-copy NASDAQ OUCH 5.0 and TotalView-ITCH 5.0 binary protocol parsers at 25.4M msgs/sec and 12ns median latency (4.0x faster than JSON)."},
        {"type": "bullet", "text": "<b>Tail Profiling</b>: Corrected 1,450x Coordinated Omission tail blowout (1.15µs to 1.67ms) using Gil Tene's HDR latency histogram backfilling."},
        {"type": "bullet", "text": "<b>Exchange Mechanics</b>: Discrete Call Auction with 4-objective Walrasian clearing, CME Pro-Rata allocation with remainder distribution, Icebergs, and Self-Trade Prevention."},
        {"type": "bullet", "text": "<b>Quantitative Microstructure</b>: Sasha Stoikov Micro-Price (21.3M ops/s @ 19ns), VPIN toxicity calculator (17.6M ops/s @ 26ns), and Avellaneda-Stoikov market maker bot (19.6M ops/s @ 19ns)."},
        {"type": "bullet", "text": "<b>Deterministic Persistence</b>: Append-only memory-mapped journal (MapViewOfFile/mmap) sustaining 7.64M writes/sec (335 MB/s @ 20ns) with 1M order crash replay in 253ms."},

        {"type": "h1", "text": "2. Top 5 Superday Interview Trap Defenses"},
        {"type": "h2", "text": "Trap 1: Why not use mutexes or spinlocks for order ingress?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Mutexes incur an OS descheduling cliff (5–50µs wakeup delay), causing p99 latency to explode past 1.94ms. Atomic spinlocks cause MESI cache line bouncing across cores. Our lock-free SPSC Single-Writer engine with private cursors and memory_order_release eliminates both, slashing tail latency to 30µs.'"},

        {"type": "h2", "text": "Trap 2: What is Coordinated Omission and how was it diagnosed?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Closed-loop benchmarks pause when the engine pauses, artificially hiding queue delays. Gil Tene's backfilling algorithm revealed that Phase 1's true p99.9 tail was 1.67ms (a 1,450x blowout) rather than the reported 1.15µs. Phase 2 zero-allocation eliminated heap locks, keeping tail strictly sub-microsecond.'"},

        {"type": "h2", "text": "Trap 3: Why does std::map suffer a 14.2x latency penalty?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Red-Black tree pointer chasing triggers L1/L2 cache misses on every node hop. DirectPriceLadder maps prices directly to contiguous arrays in O(1) time with zero pointer chasing.'"},

        {"type": "callout", "text": "<b>Portfolio Summary</b>: Complete 10-week institutional engine verified across all 38 compilation, unit test, and benchmark steps with 100% test parity."}
    ]
    create_styled_pdf(pdf1, "WEEK 10: SUPERDAY INTERVIEW MASTERY & RESUME BLUEPRINT",
                      "Week 10: Superday Interview Defense & Quantitative Resume",
                      "Production-Grade Resume Bullet Points, Superday Trap Defenses, and Master Architecture",
                      sections)

if __name__ == "__main__":
    generate_week10_docs()
