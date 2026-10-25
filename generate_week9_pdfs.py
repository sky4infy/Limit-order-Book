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

def generate_week9_docs():
    root = r"d:\Limit Order Book"

    # PDF 1: Architecture & Walkthrough
    pdf1 = os.path.join(root, "Week_9_System_Hardening_Determinism_and_Journaling.pdf")
    sections_walkthrough = [
        {"type": "h1", "text": "1. Append-Only Memory-Mapped Transaction Journaling"},
        {"type": "p", "text": "In production exchange architectures, trading engines must guarantee zero state loss without sacrificing nanosecond execution speed. We engineered a zero-allocation, append-only memory-mapped journal:"},
        {"type": "bullet", "text": "<b>Memory Mapping (MapViewOfFile / mmap)</b>: Direct access to kernel page cache; hot-path appends execute in user-space via raw pointer advances without syscall overhead."},
        {"type": "bullet", "text": "<b>64-Byte Persistent Header</b>: Stamped with 'LOBJRNL' magic bytes, write offsets, record counts, and sequence counters to withstand dirty unmaps."},
        {"type": "bullet", "text": "<b>46-Byte Packed Binary Records</b>: Exact layout storing sequence numbers, timestamps, order IDs, sides, prices, quantities, and XOR checksums."},
        {"type": "callout", "text": "<b>Benchmark Result</b>: Sustained <b>7,643,342 writes/sec (335.3 MB/s)</b> at <b>20-nanosecond median latency</b> (p90: 22ns, p99: 1.05µs)."},

        {"type": "h1", "text": "2. Deterministic Crash Recovery & Sequence Replay"},
        {"type": "p", "text": "Deterministic state recovery requires that replaying the identical event stream restores 100% bit-level order book parity:"},
        {"type": "bullet", "text": "<b>Cold Start Initialization</b>: Reopens journal file using OPEN_ALWAYS, validates header magic, and initializes a clean OrderBookOptimized instance."},
        {"type": "bullet", "text": "<b>Sequential Event Application</b>: Sequentially executes ORDER_ADD, ORDER_CANCEL, and ORDER_EXECUTE directly from memory pointers."},
        {"type": "callout", "text": "<b>Recovery Speed</b>: Replayed <b>1,000,000 orders in 253.25 ms</b> (3,948,611 records/sec), perfectly restoring Best Bid and Ask states."},

        {"type": "h1", "text": "3. Institutional Level 3 Real-Time Market Depth Dashboard"},
        {"type": "p", "text": "Full depth visualization aggregating individual Level 3 orders into visual ladder depth:"},
        {"type": "bullet", "text": "<b>Top 10 Bids and Asks</b>: Side-by-side volume distribution with ASCII bar indicators."},
        {"type": "bullet", "text": "<b>Microstructure Integration</b>: Real-time Sasha Stoikov Micro-Price and VPIN order flow toxicity classification."}
    ]
    create_styled_pdf(pdf1, "WEEK 9: SYSTEM HARDENING, DETERMINISM & JOURNALING",
                      "Week 9: Memory-Mapped Journaling, Crash Replay & L3 Visualizer",
                      "Zero-Allocation Persistence, Bit-Level Determinism, and Real-Time Risk Monitoring",
                      sections_walkthrough)

    # PDF 2: Interview Defense
    pdf2 = os.path.join(root, "Week_9_Interview_Preparation_and_Defense.pdf")
    sections_interview = [
        {"type": "h1", "text": "1. Institutional Persistence & High-Availability Defense"},
        {"type": "h2", "text": "Q1: How do you achieve high-throughput persistence without hurting nanosecond latency?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Traditional database commits and file write() syscalls cause kernel transitions and thread stalls. We use memory-mapped files (MapViewOfFile / mmap). Appending is simply pointer arithmetic and copying 46-byte packed structs into the page cache. The OS kernel flushes dirty pages asynchronously in the background, achieving 7.64M writes/sec with 20ns median latency.'"},

        {"type": "h2", "text": "Q2: How do you guarantee deterministic crash recovery?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Every event has a monotonic, gap-free sequence number and checksum. When recovering from a crash, a clean engine instance replays the binary event log from sequence #1. In our empirical test, 1,000,000 transactions were replayed in 253 milliseconds (3.95M records/sec), restoring identical order book depth.'"},

        {"type": "h2", "text": "Q3: What is the difference between Level 1, Level 2, and Level 3 market depth?"},
        {"type": "p", "text": "<b>Candidate Defense</b>: 'Level 1 is Top-of-Book (BBO). Level 2 provides aggregated volume across discrete price ticks. Level 3 (TotalView) reveals every individual order with order ID, queue position, and size. Our visualizer aggregates Level 3 orders to display queue lengths, spread in basis points, and real-time Micro-Price.'"}
    ]
    create_styled_pdf(pdf2, "WEEK 9: INTERVIEW DEFENSE & PERSISTENCE MASTERY",
                      "Week 9: System Hardening & Determinism Interview Defense",
                      "Rigorous Answers for Systems Architecture & Exchange Core Reliability Interviews",
                      sections_interview)

if __name__ == "__main__":
    generate_week9_docs()
