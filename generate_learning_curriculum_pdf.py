import sys
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
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
            self.setFillColor(colors.HexColor("#047857")) # Emerald 700 accent
            self.rect(0, 11 * inch - 6, 8.5 * inch, 6, fill=1, stroke=0)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#065F46"))
        self.drawString(42, 11 * inch - 26, "HFT & SYSTEMS ENGINEERING CURRICULUM: ZERO TO HERO")
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(8.5 * inch - 42, 11 * inch - 26, "10-Week Mastery Syllabus | Goldman Sachs / Prop Trading")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(42, 11 * inch - 30, 8.5 * inch - 42, 11 * inch - 30)
        
        # Running Footer
        self.line(42, 32, 8.5 * inch - 42, 32)
        self.drawString(42, 22, "Confidential — Self-Paced Systems & Trading Foundations Syllabus | Student: Akash")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 7.5)
        self.drawRightString(8.5 * inch - 42, 22, page_str)
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#0F172A")    # Slate 900
    accent_emerald = colors.HexColor("#065F46")   # Emerald 800
    accent_sub = colors.HexColor("#047857")       # Emerald 700
    text_dark = colors.HexColor("#1E293B")        # Slate 800
    text_muted = colors.HexColor("#64748B")       # Slate 500
    border_color = colors.HexColor("#CBD5E1")     # Slate 300
    callout_bg = colors.HexColor("#F0FDF4")       # Emerald 50
    table_alt_bg = colors.HexColor("#F8FAFC")     # Slate 50

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        textColor=primary_color,
        spaceAfter=3
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=accent_emerald,
        spaceAfter=5
    )
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=text_dark
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=primary_color,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=accent_emerald,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=text_dark,
        spaceAfter=3.5
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=text_dark,
        leftIndent=9,
        firstLineIndent=-6,
        spaceAfter=2
    )
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=8.5,
        textColor=colors.HexColor("#0F172A")
    )
    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10.5,
        textColor=colors.HexColor("#1E293B")
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.2,
        textColor=text_dark
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.5,
        textColor=colors.white
    )

    story = []

    # PAGE 1: INTRO & SYLLABUS OVERVIEW
    story.append(Paragraph("ZERO-TO-HERO COMPREHENSIVE LEARNING SYLLABUS", subtitle_style))
    story.append(Paragraph("Low-Latency Systems & High-Frequency Trading Foundations", title_style))
    story.append(Paragraph("<b>10-Week Step-by-Step Curriculum:</b> Starting with Zero Knowledge to Building an Institutional Limit Order Book", ParagraphStyle('SubSub', fontName='Helvetica', fontSize=7.8, leading=10.5, textColor=text_muted, spaceAfter=5)))
    
    meta_table_data = [
        [
            Paragraph("<b>Target Mastery:</b> Market Mechanics, Computer Architecture, Lock-Free Concurrency, Microstructure", meta_style),
            Paragraph("<b>Student / Candidate:</b> Akash", meta_style)
        ],
        [
            Paragraph("<b>Time Commitment:</b> 1.5 to 2.0 Hours / Day (Self-Paced)", meta_style),
            Paragraph("<b>Target Outcome:</b> Goldman Sachs Core Strats / HFT Superday Ready", meta_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[310, 218])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    callout_box = Table([[
        Paragraph(
            "<b>The Ground-Zero Mindset:</b> Starting with zero prior knowledge is your greatest competitive advantage. "
            "You do not have bad habits or false assumptions to unlearn. Many university students learn high-level abstractions "
            "where memory is 'free' and threads are 'automatic'. In this curriculum, you will learn <b>Mechanical Sympathy</b>—how "
            "CPUs, hardware caches, memory controllers, and operating system schedulers actually function—and apply it directly to building "
            "an electronic exchange from scratch.",
            callout_style
        )
    ]], colWidths=[528])
    callout_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#86EFAC")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(callout_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. The 10-Week Curriculum Roadmap at a Glance", h1_style))
    
    curriculum_data = [
        [
            Paragraph("Week", table_header_style),
            Paragraph("Core Concept / Theory", table_header_style),
            Paragraph("Hands-On Engineering Deliverable", table_header_style),
            Paragraph("Milestone Code", table_header_style)
        ],
        [
            Paragraph("<b>Week 1</b>", table_cell_bold),
            Paragraph("Market Mechanics: Bids, Asks, Spread, FIFO Price-Time Priority.", table_cell_style),
            Paragraph("Textbook Order Book with clean OOP & 5 unit tests.", table_cell_style),
            Paragraph("Phase 1 Baseline", table_cell_style)
        ],
        [
            Paragraph("<b>Week 2</b>", table_cell_bold),
            Paragraph("Computer Architecture: L1/L2/L3 Caches, Cache Lines, Pointer Chasing.", table_cell_style),
            Paragraph("Array vs. Linked List benchmark; fixed-point integer ticks.", table_cell_style),
            Paragraph("Mechanical Sympathy", table_cell_style)
        ],
        [
            Paragraph("<b>Week 3</b>", table_cell_bold),
            Paragraph("Zero-Allocation Memory: Slab Allocator, Object Pools, Flat Arrays.", table_cell_style),
            Paragraph("Slab allocator & direct-indexed price array (0 heap malloc).", table_cell_style),
            Paragraph("Phase 2 Zero-Alloc", table_cell_style)
        ],
        [
            Paragraph("<b>Week 4</b>", table_cell_bold),
            Paragraph("Benchmarking Rigor: Coordinated Omission, RDTSC, HdrHistogram.", table_cell_style),
            Paragraph("Asynchronous Poisson load generator & PMU hardware profiling.", table_cell_style),
            Paragraph("Latency Percentiles", table_cell_style)
        ],
        [
            Paragraph("<b>Week 5</b>", table_cell_bold),
            Paragraph("Lock-Free Concurrency: Single-Writer Principle, SPSC Queue, False Sharing.", table_cell_style),
            Paragraph("Lock-free SPSC Ring Buffer with <code>alignas(64)</code> & core pinning.", table_cell_style),
            Paragraph("Phase 3 Disruptor", table_cell_style)
        ],
        [
            Paragraph("<b>Week 6</b>", table_cell_bold),
            Paragraph("Binary Exchange Protocols: NASDAQ OUCH 5.0 & ITCH 5.0 Multicast.", table_cell_style),
            Paragraph("Zero-copy binary packet parser & UDP market data disseminator.", table_cell_style),
            Paragraph("Wall Street Codecs", table_cell_style)
        ],
        [
            Paragraph("<b>Week 7</b>", table_cell_bold),
            Paragraph("Exchange Mechanics: Call Auction (Walrasian Uncrossing) & Pro-Rata.", table_cell_style),
            Paragraph("Equilibrium clearing price engine & CME-style pro-rata rules.", table_cell_style),
            Paragraph("Call Auction FSM", table_cell_style)
        ],
        [
            Paragraph("<b>Week 8</b>", table_cell_bold),
            Paragraph("Microstructure & Quant: Stoikov Micro-Price, VPIN Toxicity, MM Bot.", table_cell_style),
            Paragraph("Autonomous Avellaneda-Stoikov market maker & VPIN calculator.", table_cell_style),
            Paragraph("Quant Simulation", table_cell_style)
        ],
        [
            Paragraph("<b>Week 9</b>", table_cell_bold),
            Paragraph("System Hardening: Deterministic Event Sourcing & Memory-Mapped Log.", table_cell_style),
            Paragraph("Append-only <code>mmap</code> journal with crash-recovery replay test.", table_cell_style),
            Paragraph("L3 Web Visualizer", table_cell_style)
        ],
        [
            Paragraph("<b>Week 10</b>", table_cell_bold),
            Paragraph("Interview Mastery: Superday Defense, Tradeoff Explanations, Portfolio.", table_cell_style),
            Paragraph("GitHub documentation, benchmark comparison report & mock defense.", table_cell_style),
            Paragraph("Superday Ready", table_cell_style)
        ]
    ]
    curriculum_table = Table(curriculum_data, colWidths=[48, 195, 205, 80])
    curriculum_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, table_alt_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(curriculum_table)

    # PAGE 2: WEEKS 1 TO 3 (FOUNDATIONS & ZERO ALLOCATION)
    story.append(PageBreak())
    story.append(Paragraph("2. Weeks 1 - 3: Foundations, Mechanical Sympathy & Zero-Allocation", h1_style))
    
    story.append(Paragraph("<b>Week 1: Financial Market Mechanics & The Baseline Order Book</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Double auction marketplaces; Bid vs. Ask; The Spread; FIFO Price-Time Priority; Market vs. Limit vs. Cancel orders.<br/>"
        "• <b>Study Resources:</b> Watch <i>'How Does a Limit Order Book Work?'</i> (CME Group, YouTube); read Larry Harris's <i>Trading and Exchanges</i> (Chapters 1-3).<br/>"
        "• <b>Hands-On:</b> Implement Phase 1 in C++ (<code>std::map&lt;uint64_t, std::list&lt;Order&gt;&gt;</code>) or Java (<code>TreeMap</code>). "
        "Write 5 unit tests for exact fills, partial fills, multi-level sweeps, cancellations, and edge cases. Save in <code>src/baseline/</code>.",
        bullet_style
    ))

    story.append(Paragraph("<b>Week 2: Computer Architecture & The 'Mechanical Sympathy' Epiphany</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> The Memory Wall (CPU 0.25ns vs. RAM 100ns); L1/L2/L3 cache hierarchies; 64-byte cache lines; pointer chasing; heap allocation latency.<br/>"
        "• <b>Study Resources:</b> Watch Carl Cook's landmark talk <i>'When a Microsecond Is an Eternity'</i> (CppCon 2017); read CS:APP (Chapter 6: Memory Hierarchy).<br/>"
        "• <b>Hands-On:</b> Write a standalone benchmark comparing sequential array traversal vs. linked list traversal (see the 10x cache speedup!). "
        "Convert order prices from floating-point to 64-bit fixed-point integer ticks.",
        bullet_style
    ))

    story.append(Paragraph("<b>Week 3: Zero-Allocation Memory Design & Flat Data Structures</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Object pools; contiguous slab allocators; free-list index stacks; direct array indexing for BBO spread; intrusive doubly-linked lists.<br/>"
        "• <b>Study Resources:</b> Read Niklas Frykholm's <i>'Memory Pools and Slab Allocation'</i>; review boost intrusive list architectures.<br/>"
        "• <b>Hands-On:</b> Implement <code>SlabAllocator.hpp</code> (pre-allocates 1M orders) and <code>DirectPriceLadder.hpp</code> (flat array indexed by price offset). "
        "Wire into <code>OrderBookOptimized.hpp</code> with zero <code>malloc</code> calls on the critical matching path.",
        bullet_style
    ))

    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Week 1-3 Concept Check: Can You Answer These?</b>", h2_style))
    story.append(Paragraph(
        "1. Why does reading memory from RAM take hundreds of CPU clock cycles while L1 cache takes only 4 cycles?<br/>"
        "2. Why does a linked list suffer more cache misses than a contiguous array of the same size?<br/>"
        "3. How does pre-allocating an object pool at startup eliminate latency spikes during trading hours?",
        body_style
    ))

    # PAGE 3: WEEKS 4 TO 6 (BENCHMARKING, CONCURRENCY & PROTOCOLS)
    story.append(PageBreak())
    story.append(Paragraph("3. Weeks 4 - 6: Latency Benchmarking, Lock-Free Concurrency & Protocols", h1_style))

    story.append(Paragraph("<b>Week 4: Nanosecond Benchmarking & Latency Tail Analysis</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Average latency fallacy; why p99/p99.99 tails matter; Gil Tene's Coordinated Omission; CPU cycle counters (<code>RDTSC</code>); PMU hardware counters.<br/>"
        "• <b>Study Resources:</b> Watch Gil Tene's <i>'How NOT to Measure Latency'</i> (essential viewing); read Brendan Gregg's Linux <code>perf</code> profiling guides.<br/>"
        "• <b>Hands-On:</b> Build an asynchronous benchmark driver scheduling Poisson order arrivals; record latencies via <code>HdrHistogram</code>. "
        "Run <code>perf stat</code> to measure the 8x drop in L1-dcache misses between Phase 1 and Phase 2.",
        bullet_style
    ))

    story.append(Paragraph("<b>Week 5: Lock-Free Concurrency & The Single-Writer Principle</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Mutex lock contention; kernel sleep/wake costs; MESI cache coherence bus storms; Single-Writer Principle; memory order barriers (acquire/release); False Sharing.<br/>"
        "• <b>Study Resources:</b> Read the <i>LMAX Disruptor Technical Whitepaper</i>; watch Herb Sutter's <i>'Lock-Free Programming'</i> (CppCon 2014).<br/>"
        "• <b>Hands-On:</b> Implement a lock-free Single-Producer Single-Consumer (SPSC) ring buffer with <code>alignas(64)</code> cache-line padding. "
        "Pin the matching thread to Core 2 via <code>pthread_setaffinity_np</code>. Scale throughput past 5M orders/sec.",
        bullet_style
    ))

    story.append(Paragraph("<b>Week 6: Binary Exchange Protocols (NASDAQ OUCH & ITCH)</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Why Wall Street avoids JSON/REST; binary serialization; packed byte structs; network big-endian vs. little-endian; zero-copy deserialization.<br/>"
        "• <b>Study Resources:</b> Read the official NASDAQ specifications: <i>'NASDAQ ITCH 5.0'</i> and <i>'NASDAQ OUCH 5.0'</i>.<br/>"
        "• <b>Hands-On:</b> Implement <code>OuchCodec.hpp</code> to parse binary order entry packets without string allocations; "
        "build <code>ItchPublisher.hpp</code> to broadcast UDP multicast Level 3 market data events.",
        bullet_style
    ))

    story.append(Spacer(1, 3))
    story.append(Paragraph("<b>Week 4-6 Concept Check: Can You Answer These?</b>", h2_style))
    story.append(Paragraph(
        "1. What is Coordinated Omission, and how does a synchronous load tester hide server stalls?<br/>"
        "2. What happens to CPU performance when two threads write to variables in the same 64-byte cache line?<br/>"
        "3. Why can casting a raw byte pointer to a packed C++ struct be 100x faster than parsing JSON?",
        body_style
    ))

    # PAGE 4: WEEKS 7 TO 10 (EXCHANGE MECHANICS, QUANT & INTERVIEWS)
    story.append(PageBreak())
    story.append(Paragraph("4. Weeks 7 - 10: Exchange Mechanics, Microstructure & Superday Mastery", h1_style))

    story.append(Paragraph("<b>Week 7: Advanced Exchange Mechanics (Call Auctions & Pro-Rata)</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Continuous trading vs. pre-open Call Auction; Walrasian equilibrium clearing price discovery; CME Pro-Rata allocation; Iceberg orders; Self-Trade Prevention.<br/>"
        "• <b>Study Resources:</b> Read CME Group's <i>'Pro-Rata Allocation Rules in Futures'</i>; review NASDAQ Rule 4752.<br/>"
        "• <b>Hands-On:</b> Build <code>CallAuction.hpp</code> computing the equilibrium price maximizing executed volume; implement configurable FIFO vs. Pro-Rata matching rules.",
        bullet_style
    ))

    story.append(Paragraph("<b>Week 8: Market Microstructure & Algorithmic Trading Sandbox</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Sasha Stoikov's Micro-Price; multi-level queue depth imbalance; VPIN order flow toxicity; Avellaneda-Stoikov market making model; inventory risk.<br/>"
        "• <b>Study Resources:</b> Read Sasha Stoikov's 2018 paper <i>'The Micro-Price'</i>; read Avellaneda & Stoikov (2008) <i>'High-frequency trading in a limit order book'</i>.<br/>"
        "• <b>Hands-On:</b> Implement <code>MicroPrice.hpp</code> and <code>VpinCalculator.hpp</code>. Build an autonomous market maker bot trading against synthetic Poisson noise orders.",
        bullet_style
    ))

    story.append(Paragraph("<b>Week 9: System Hardening, Real-Time Visualizer & Determinism</b>", h2_style))
    story.append(Paragraph(
        "• <b>Concepts:</b> Deterministic Event Sourcing; memory-mapped files (<code>mmap</code>); crash recovery; real-time web streaming via WebSocket/WebTransport.<br/>"
        "• <b>Hands-On:</b> Implement append-only <code>mmap</code> binary transaction journaling. Run a 10M trade crash-recovery test asserting bit-for-bit state checksum parity. Connect a React/Canvas Level 3 visualizer.",
        bullet_style
    ))

    story.append(Paragraph("<b>Week 10: Superday Interview Defense & Portfolio Packaging</b>", h2_style))
    story.append(Paragraph(
        "• <b>Deliverables:</b> Format README with architecture diagrams and Phase 1 vs. 2 vs. 3 benchmark tables; practice the 2-minute project defense; conduct mock technical interviews.<br/>"
        "• <b>Target Result:</b> Stand out as a top 1% candidate for Goldman Sachs Core Strats / Electronic Trading and premier prop trading desks.",
        bullet_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Recommended Daily Routine (1.5 - 2.0 Hours / Day)", h1_style))
    
    routine_data = [
        [Paragraph("Time Allocation", table_header_style), Paragraph("Focus Activity", table_header_style), Paragraph("Actionable Goal", table_header_style)],
        [Paragraph("<b>First 30 Mins</b>", table_cell_bold), Paragraph("Concept & Reading", table_cell_style), Paragraph("Watch 1 video or read 1 paper/chapter; annotate key concepts.", table_cell_style)],
        [Paragraph("<b>Next 60 Mins</b>", table_cell_bold), Paragraph("Hands-On Coding", table_cell_style), Paragraph("Write modular, test-driven code for that week's deliverable.", table_cell_style)],
        [Paragraph("<b>Final 20 Mins</b>", table_cell_bold), Paragraph("Profiling & Reflection", table_cell_style), Paragraph("Run benchmarks, record metrics, and write a 3-bullet takeaway.", table_cell_style)]
    ]
    routine_table = Table(routine_data, colWidths=[110, 150, 268])
    routine_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, table_alt_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(routine_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    output_pdf = r"d:\Limit Book Order\Zero_To_Hero_Weekly_Learning_Curriculum.pdf"
    build_pdf(output_pdf)
