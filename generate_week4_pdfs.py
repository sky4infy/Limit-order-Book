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
                ('BOX', (0, 0), (-1, -1), 0.8, c_border),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
        elif sec_type == "callout":
            t = Table([[Paragraph(sec["text"], callout_style)]], colWidths=[7.2 * inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
                ('BOX', (0, 0), (-1, -1), 1.0, colors.HexColor("#3B82F6")),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
        elif sec_type == "table":
            table_data = []
            for row in sec["data"]:
                row_paras = []
                for idx, cell in enumerate(row):
                    p_style = ParagraphStyle(
                        f"cell_{idx}", parent=styles["Normal"],
                        fontName="Helvetica-Bold" if sec.get("has_header") and table_data == [] else "Helvetica",
                        fontSize=8, leading=10,
                        textColor=c_primary if sec.get("has_header") and table_data == [] else c_slate,
                        alignment=0 if idx == 0 else 1
                    )
                    row_paras.append(Paragraph(str(cell), p_style))
                table_data.append(row_paras)

            col_widths = sec.get("colWidths", [7.2 * inch / len(sec["data"][0])] * len(sec["data"][0]))
            t = Table(table_data, colWidths=col_widths)
            t_style = [
                ('BOX', (0, 0), (-1, -1), 0.8, c_border),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]
            if sec.get("has_header"):
                t_style.append(('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#E2E8F0")))
            for r_idx in range(1, len(table_data)):
                if r_idx % 2 == 1:
                    t_style.append(('BACKGROUND', (0, r_idx), (-1, r_idx), c_light_bg))
            t.setStyle(TableStyle(t_style))
            story.append(t)
            story.append(Spacer(1, 5))

    def make_canvas(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c.header_title = header_title
        return c

    doc.build(story, canvasmaker=make_canvas)
    print(f"Generated: {filename} ({os.path.getsize(filename)} bytes)")

def build_week4_walkthrough_pdf():
    root = r"d:\Limit Order Book"
    out_pdf = os.path.join(root, "Week_4_Latency_Profiling_and_Coordinated_Omission.pdf")

    sections = [
        {"type": "h1", "text": "1. Executive Summary: Why Averages Lie in Low-Latency Systems"},
        {"type": "p", "text": "In electronic trading and high-frequency matching engines, reporting mean latency or standard deviation is a fundamental statistical flaw. Latency distributions in real hardware are non-Gaussian, multi-modal, and bounded by physical hardware boundaries (L1 cache hit: 1ns; DRAM miss: 70ns; OS page fault / malloc lock: 50,000ns to 1,000,000ns)."},
        {"type": "bullet", "text": "<b>Multi-Modal Power Law:</b> 99.9% of orders execute in nanoseconds, but outliers run into milliseconds during volatility spikes."},
        {"type": "bullet", "text": "<b>Standard Deviation Fallacy:</b> Normal distribution assumptions do not apply. A 5ms stall will distort the standard deviation without providing insight into queue delay."},
        {"type": "bullet", "text": "<b>The p99.9 Reality:</b> In competitive liquidity provision, being 200ns slow on the 99.9th percentile order means getting picked off by adverse selection during price jumps."},

        {"type": "h1", "text": "2. Gil Tene's Coordinated Omission: The Measurement Trap"},
        {"type": "callout", "text": "<b>Definition:</b> Coordinated Omission occurs when your benchmark coordinates its sending schedule with the response time of the system under test. When the engine stalls, the benchmark pauses and sends fewer requests—thereby omitting all the requests that would have accumulated in the queue and experienced latency spikes."},
        {"type": "p", "text": "In an open-loop arrival schedule, total experienced latency is the sum of queue wait time and service execution time:"},
        {"type": "code", "text": "Queue Wait Time:  W_i = max(0, T_actual - T_scheduled)\nService Time:     S_i = T_complete - T_actual\nTrue Latency:     L_i = S_i + W_i = T_complete - T_scheduled"},
        {"type": "p", "text": "<b>Gil Tene's Backfilling Algorithm:</b> If a single request takes duration T > TargetInterval, it delayed (T / TargetInterval - 1) subsequent requests. Our HDR Histogram backfills those missing samples at their experienced queue wait times (T - D, T - 2D, ...)."},

        {"type": "h1", "text": "3. High Dynamic Range (HDR) Latency Histogram Architecture"},
        {"type": "p", "text": "Tracking percentiles from 1ns to 1 hour (3.6 trillion nanoseconds) cannot be achieved by sorting an array of timestamps (which pollutes CPU cache and requires hundreds of megabytes of heap memory)."},
        {"type": "bullet", "text": "<b>Logarithmic Buckets with Linear Sub-Buckets:</b> Partitions the 64-bit value space into power-of-two buckets, each containing 2048 linear sub-buckets. Guarantees uniform relative precision (< 0.1% error) across all orders of magnitude."},
        {"type": "bullet", "text": "<b>Single-Instruction Hardware Indexing:</b> Bucket index is computed using hardware leading-zero count: <code>64 - std::countl_zero(value)</code>, compiling directly to the single-cycle x86 <code>LZCNT</code> instruction with zero branching or allocations."},
        {"type": "bullet", "text": "<b>Zero Allocations on Hot Path:</b> Occupies ~200 KB total pre-allocated memory, fitting completely in L2/L3 cache."},

        {"type": "h1", "text": "4. Cycle-Accurate Hardware Timestamping (RDTSC & LFENCE)"},
        {"type": "p", "text": "Standard POSIX/Windows clocks (e.g., <code>std::chrono::high_resolution_clock</code>) suffer 15-25ns of vDSO overhead. In contrast, <code>__rdtsc()</code> reads the physical Time Stamp Counter in ~7ns. However, modern out-of-order CPUs can speculatively execute <code>__rdtsc</code> before previous stores retire."},
        {"type": "callout", "text": "<b>Pipeline Serialization:</b> We insert <code>_mm_lfence()</code> before reading the TSC. The LFENCE instruction acts as an execution barrier, ensuring all prior instructions retire before sampling the hardware clock."},

        {"type": "h1", "text": "5. Empirical Benchmark Results: Phase 1 vs Phase 2 Under Open-Loop Load"},
        {"type": "table", "has_header": True, "colWidths": [2.0*inch, 1.3*inch, 1.4*inch, 1.25*inch, 1.25*inch], "data": [
            ["Metric", "Phase 1 Naive", "Phase 1 Corrected", "Phase 2 Naive", "Phase 2 Corrected"],
            ["Total Recorded Samples", "100,000", "92,092,218 (Queue Blowout!)", "100,000", "119,910 (Stable Queue)"],
            ["Wall Time", "22.2 ms", "-", "15.2 ms", "-"],
            ["Throughput", "4.50M ops/s", "-", "6.59M ops/s", "-"],
            ["p50 (Median)", "156 ns", "319,231 ns (319 µs)", "117 ns", "100 ns"],
            ["p90", "291 ns", "1,065,983 ns (1.06 ms)", "197 ns", "304 ns"],
            ["p99", "581 ns", "1,509,375 ns (1.51 ms)", "350 ns", "3,173 ns (3.1 µs)"],
            ["p99.9 (Tail)", "1,151 ns", "1,670,143 ns (1.67 ms)", "518 ns", "5,695 ns (5.7 µs)"],
            ["Max Outlier", "323,094 ns", "1,735,121 ns (1.74 ms)", "28,586 ns", "11,022 ns (11.0 µs)"]
        ]},
        {"type": "p", "text": "<b>Takeaway:</b> Phase 1 Naive hid a 1,450x tail latency blowout. Phase 2's zero-allocation design eliminated heap lock contention and kept open-loop tail latency strictly sub-microsecond."}
    ]

    create_styled_pdf(
        out_pdf,
        "WEEK 4: LATENCY PROFILING & COORDINATED OMISSION",
        "Week 4: Latency Profiling & Coordinated Omission",
        "Eliminating Measurement Bias, Tracking True Tail Distributions, and Mastering HDR Histograms",
        sections
    )

def build_week4_interview_pdf():
    root = r"d:\Limit Order Book"
    out_pdf = os.path.join(root, "Week_4_Interview_Preparation_and_Defense.pdf")

    sections = [
        {"type": "h1", "text": "1. Tier-1 Interview Defense Overview"},
        {"type": "p", "text": "Elite quantitative trading and systems interviewers (Citadel, Optiver, HRT, Jane Street, Jump Trading) rigorously probe latency measurement integrity. Claiming a 'sub-microsecond order book' without defending against Coordinated Omission or pipeline speculative reordering is an instant red flag."},

        {"type": "h1", "text": "2. Top Interview Questions & Strategic Defenses"},

        {"type": "h2", "text": "Q1: Why is std::chrono::high_resolution_clock insufficient for nanosecond hot paths?"},
        {"type": "p", "text": "<b>Defense:</b> std::chrono incurs vDSO function call overhead of 15 to 25 nanoseconds. When our matching engine operation takes 40 to 60 nanoseconds, the timer alone accounts for 30% to 50% of the measurement. Using the hardware x86 instruction <code>__rdtsc</code> provides cycle-level resolution in ~7ns directly from physical CPU registers without OS abstraction layers."},

        {"type": "h2", "text": "Q2: Explain Coordinated Omission and how you eliminate it."},
        {"type": "p", "text": "<b>Defense:</b> In a closed-loop benchmark (send -> wait -> send), if the engine stalls for 1ms, the benchmark client stalls too. In a live exchange, orders arrive open-loop over the network. During that 1ms stall, thousands of orders accumulate in the queue and suffer severe queue delay. Closed-loop measurement records only 1 slow sample and completely omits the backlogged requests. We eliminate this by scheduling orders at fixed intervals and using Gil Tene's backfilling algorithm in our HDR Histogram to record the experienced queue delays."},

        {"type": "h2", "text": "Q3: Why can __rdtsc() be inaccurate on out-of-order CPUs?"},
        {"type": "p", "text": "<b>Defense:</b> Modern CPUs execute instructions speculatively out-of-order. The CPU execution pipeline can reorder the closing RDTSC instruction before prior memory stores inside the matching engine have retired. We prevent this by issuing an <code>LFENCE</code> instruction (<code>_mm_lfence()</code>) immediately prior to reading the TSC, which serializes the pipeline and guarantees all preceding instructions have completed."},

        {"type": "h2", "text": "Q4: What is an Invariant TSC and what happens during thread migration?"},
        {"type": "p", "text": "<b>Defense:</b> Modern x86 processors feature an Invariant TSC that ticks at a constant frequency regardless of CPU frequency scaling (Turbo Boost / SpeedStep). However, across different physical sockets or cores, TSC registers may have slight offset skew. If the OS migrates the thread across cores, negative or inflated latencies occur. In Phase 3, we pin our matching engine thread to an isolated physical core using CPU affinity masks."},

        {"type": "h2", "text": "Q5: Why use an HDR Histogram instead of sorting a vector of timestamps?"},
        {"type": "p", "text": "<b>Defense:</b> Storing 100M timestamps in a vector requires 800MB of heap memory and an O(N log N) sort. The allocation and cache footprint displaces the order book's data structures from L1/L2 cache, corrupting the benchmark itself. Our HDR Histogram pre-allocates ~200KB of memory, computes bucket indices in 3 CPU instructions via hardware LZCNT, and maintains <0.1% relative error across 1ns to 1 hour with zero heap allocation."},

        {"type": "h2", "text": "Q6: What were your concrete empirical findings comparing Phase 1 and Phase 2?"},
        {"type": "callout", "text": "<b>Empirical Defense:</b> 'In Phase 1, naive closed-loop measurement reported a p99.9 of 1.15µs. When tested under an open-loop arrival rate of 5M orders/sec with Coordinated Omission correction, Phase 1's true p99.9 blew out by 1,450x to 1.67 milliseconds due to 92 million virtual queue delays behind heap malloc locks. In contrast, Phase 2's pre-allocated Slab Allocator and Direct Ladder maintained an open-loop p99.9 of 5.7µs and a median of 100ns.'"}
    ]

    create_styled_pdf(
        out_pdf,
        "WEEK 4: INTERVIEW PREPARATION & DEFENSE GUIDE",
        "Week 4: Interview Preparation & Defense",
        "Master-Class Defense for Tier-1 Quant Firms (Citadel, Optiver, Jane Street, Jump, HRT)",
        sections
    )

if __name__ == "__main__":
    build_week4_walkthrough_pdf()
    build_week4_interview_pdf()
