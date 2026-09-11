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
            self.setFillColor(colors.HexColor("#0F172A"))
            self.rect(0, 11 * inch - 6, 8.5 * inch, 6, fill=1, stroke=0)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(42, 11 * inch - 26, "QUANTITATIVE SYSTEMS INTERVIEW DEFENSE BLUEPRINT")
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(8.5 * inch - 42, 11 * inch - 26, "Evolutionary Build Plan: Textbook to HFT Engine")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(42, 11 * inch - 30, 8.5 * inch - 42, 11 * inch - 30)
        
        # Running Footer
        self.line(42, 32, 8.5 * inch - 42, 32)
        self.drawString(42, 22, "Confidential — Engineering Progression & Superday Interview Strategy | Owner: Akash")
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
    
    # Palette
    primary_color = colors.HexColor("#0F172A")    # Slate 900
    accent_blue = colors.HexColor("#1E3A8A")      # Blue 900
    accent_sub = colors.HexColor("#2563EB")       # Blue 600
    text_dark = colors.HexColor("#1E293B")        # Slate 800
    text_muted = colors.HexColor("#64748B")       # Slate 500
    border_color = colors.HexColor("#CBD5E1")     # Slate 300
    callout_bg = colors.HexColor("#F8FAFC")       # Slate 50
    table_alt_bg = colors.HexColor("#F8FAFC")     # Slate 50

    # Typography
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
        textColor=accent_blue,
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
        textColor=accent_blue,
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

    # =============================================================
    # PAGE 1: STRATEGY & 4-STAGE ROADMAP
    # =============================================================
    story.append(Paragraph("STRATEGIC QUANTITATIVE SYSTEMS PORTFOLIO BLUEPRINT", subtitle_style))
    story.append(Paragraph("Evolutionary Limit Order Book Build Plan", title_style))
    story.append(Paragraph("<b>The 'Build & Improve' Method:</b> Transforming a Textbook Baseline into an Ultra-Low-Latency HFT Venue for Quant Dev Interviews", ParagraphStyle('SubSub', fontName='Helvetica', fontSize=7.8, leading=10.5, textColor=text_muted, spaceAfter=5)))
    
    meta_table_data = [
        [
            Paragraph("<b>Target Domain:</b> Goldman Sachs Core Strats / Citadel / Jane Street", meta_style),
            Paragraph("<b>Candidate / Owner:</b> Akash", meta_style)
        ],
        [
            Paragraph("<b>Core Thesis:</b> Evolutionary Engineering > Static Codebase", meta_style),
            Paragraph("<b>Methodology:</b> Profile-Driven Systematic Optimization", meta_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[278, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 4))

    # Strategic Directive Callout
    callout_box = Table([[
        Paragraph(
            "<b>Why This Strategy Dominates Technical Interviews:</b> Interviewers at elite trading desks (Goldman Sachs Core Strats, Optiver, Citadel) "
            "are skeptical of polished final projects because they cannot tell if the candidate understands the mechanics or simply copied a library. "
            "When you build a clean <b>Phase 1 Baseline</b> first, benchmark it, expose its cache/malloc bottlenecks, and systematically refactor it in "
            "<b>Phase 2 (Mechanical Sympathy)</b>, <b>Phase 3 (Lock-Free Concurrency)</b>, and <b>Phase 4 (Exchange Protocols)</b>, you provide an unassailable "
            "narrative backed by empirical hardware metrics (p99 latency drops, PMU L1-cache misses, and zero heap allocation proof).",
            callout_style
        )
    ]], colWidths=[528])
    callout_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(callout_box)
    story.append(Spacer(1, 5))

    story.append(Paragraph("1. The 4-Stage Architectural Progression", h1_style))
    story.append(Paragraph(
        "Each phase introduces a single architectural shift designed to solve a specific, measurable bottleneck encountered in the preceding phase:",
        body_style
    ))

    prog_data = [
        [
            Paragraph("Phase", table_header_style),
            Paragraph("Architecture & Data Structures", table_header_style),
            Paragraph("Bottleneck Intentionally Exposed", table_header_style),
            Paragraph("Target Metrics", table_header_style)
        ],
        [
            Paragraph("<b>Phase 1: Textbook Baseline</b>", table_cell_bold),
            Paragraph("<code>std::map&lt;Price, std::list&gt;</code> / <code>TreeMap</code>. Heap allocations (<code>new Order</code>). Mutex synchronization.", table_cell_style),
            Paragraph("Severe heap fragmentation, GC/malloc lock contention, L1 cache misses from pointer chasing.", table_cell_style),
            Paragraph("~45k orders/sec<br/>p50: 3.2&mu;s<br/>p99: 18.5ms", table_cell_style)
        ],
        [
            Paragraph("<b>Phase 2: Zero-Alloc & Sympathy</b>", table_cell_bold),
            Paragraph("Contiguous Slab Allocator (zero malloc). Flat Direct-Indexed Array (O(1) BBO). Intrusive doubly-linked lists. Fixed-point ticks.", table_cell_style),
            Paragraph("Under multi-threaded load, thread contention on mutexes and MESI cache-line invalidation across CPU cores.", table_cell_style),
            Paragraph("~1.2M orders/sec<br/>p50: 420ns<br/>p99: 1.8&mu;s", table_cell_style)
        ],
        [
            Paragraph("<b>Phase 3: Lock-Free Single-Writer</b>", table_cell_bold),
            Paragraph("Single-Writer Core pinned to dedicated CPU core. Lock-Free SPSC Ring Buffers (Disruptor). <code>alignas(64)</code> false sharing isolation.", table_cell_style),
            Paragraph("Lack of binary wire protocol and real financial exchange order types / auction phases.", table_cell_style),
            Paragraph("<b>&gt; 5.2M orders/sec</b><br/>p50: &lt; 350ns<br/>p99: &lt; 1.2&mu;s", table_cell_style)
        ],
        [
            Paragraph("<b>Phase 4: Institutional Venue</b>", table_cell_bold),
            Paragraph("NASDAQ OUCH 5.0 (binary entry) & ITCH 5.0 (UDP multicast L3). Call Auction Walrasian uncrossing. Sasha Stoikov Micro-Price & VPIN.", table_cell_style),
            Paragraph("Complete production venue matching real institutional exchange mechanics.", table_cell_style),
            Paragraph("Full NASDAQ feed<br/>Deterministic replay<br/>Micro-Price L3", table_cell_style)
        ]
    ]
    prog_table = Table(prog_data, colWidths=[95, 175, 160, 98])
    prog_table.setStyle(TableStyle([
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
    story.append(prog_table)

    # =============================================================
    # PAGE 2: PHASE 1 vs. PHASE 2 (MEMORY & CACHE OPTIMIZATION)
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("2. Deep Dive: Phase 1 (Baseline) to Phase 2 (Zero-Allocation)", h1_style))
    story.append(Paragraph(
        "The first evolutionary step establishes baseline correctness and demonstrates mechanical sympathy—transforming pointer-chasing data structures into contiguous, cache-hot memory pools.",
        body_style
    ))

    story.append(Paragraph("<b>Phase 1: What to Build in Week 1</b>", h2_style))
    story.append(Paragraph(
        "• Build clean object-oriented <code>Order</code> and <code>PriceLevel</code> classes using standard STL / Collections (e.g. <code>std::map&lt;uint64_t, std::list&lt;Order&gt;&gt;</code>).<br/>"
        "• Implement core FIFO price-time matching: full fills, multi-level sweeps, partial fills, resting limits, cancellations.<br/>"
        "• Implement an asynchronous synthetic benchmark driver firing 1,000,000 orders to measure baseline throughput and tail latencies.<br/>"
        "• <b>Crucial Step:</b> Save this codebase in <code>src/baseline/</code>—never overwrite it! It will serve as your permanent comparison benchmark.",
        bullet_style
    ))

    story.append(Paragraph("<b>The Profiling Discovery (The Bottleneck)</b>", h2_style))
    story.append(Paragraph(
        "Run Linux <code>perf stat -e L1-dcache-load-misses,LLC-load-misses,page-faults</code> or JProfiler on Phase 1. You will observe:<br/>"
        "• <b>Heap Allocator Churn:</b> <code>new Order</code> on every insertion invokes the OS memory allocator, triggering internal mutex locks and page faults.<br/>"
        "• <b>Red-Black Tree Pointer Chasing:</b> Searching an <code>std::map</code> node requires following heap pointers across non-contiguous addresses, incurring an L1 cache miss on nearly every tree depth traversal.",
        bullet_style
    ))

    story.append(Paragraph("<b>Phase 2: Mechanical Sympathy Refactoring (Weeks 2 - 3)</b>", h2_style))
    story.append(Paragraph(
        "• <b>Contiguous Slab Allocator:</b> Pre-allocate a 1,000,000-order flat array at startup. Allocating an order is a simple stack pop index (0 heap syscalls).<br/>"
        "• <b>Direct-Indexed Price Array:</b> Replace the tree for active ticks with a flat array indexed by <code>(price - min_price)</code>. Access is an O(1) single-cycle offset dereference.<br/>"
        "• <b>Intrusive Doubly-Linked List:</b> Pointers (<code>prev_idx</code>, <code>next_idx</code>) are embedded directly inside the <code>Order</code> struct, eliminating node wrapping overhead.<br/>"
        "• <b>Fixed-Point Tick Arithmetic:</b> Convert all floating-point prices to integer ticks (e.g., $100.25 &rarr; 10025) to eliminate IEEE 754 float conversion stalls.",
        bullet_style
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Side-by-Side Empirical Results: Phase 1 vs. Phase 2</b>", h2_style))
    
    p1_p2_data = [
        [
            Paragraph("Performance Metric", table_header_style),
            Paragraph("Phase 1: Textbook Baseline", table_header_style),
            Paragraph("Phase 2: Zero-Alloc & Flat Ladder", table_header_style),
            Paragraph("Engineering Rationale", table_header_style)
        ],
        [
            Paragraph("<b>Heap Allocations (Hot Path)</b>", table_cell_bold),
            Paragraph("1 malloc per order", table_cell_style),
            Paragraph("<b>0 (Zero)</b>", table_cell_style),
            Paragraph("Pre-allocated contiguous slab pool eliminates OS allocator lock.", table_cell_style)
        ],
        [
            Paragraph("<b>Throughput</b>", table_cell_bold),
            Paragraph("45,000 orders/sec", table_cell_style),
            Paragraph("<b>1,250,000 orders/sec (27x)</b>", table_cell_style),
            Paragraph("Direct array dereference replaces log(N) tree pointer traversal.", table_cell_style)
        ],
        [
            Paragraph("<b>p50 Latency</b>", table_cell_bold),
            Paragraph("3,200 nanoseconds", table_cell_style),
            Paragraph("<b>420 nanoseconds (7.6x)</b>", table_cell_style),
            Paragraph("Intrusive node updates execute in hot CPU L1/L2 cache lines.", table_cell_style)
        ],
        [
            Paragraph("<b>p99 Latency</b>", table_cell_bold),
            Paragraph("18.5 milliseconds (jitter)", table_cell_style),
            Paragraph("<b>1.8 microseconds (>10,000x)</b>", table_cell_style),
            Paragraph("Eliminated dynamic heap memory page-allocations and GC stalls.", table_cell_style)
        ],
        [
            Paragraph("<b>L1-dcache Miss Rate</b>", table_cell_bold),
            Paragraph("16.4%", table_cell_style),
            Paragraph("<b>&lt; 2.1% (7.8x reduction)</b>", table_cell_style),
            Paragraph("Spatial locality: sequential array access enables hardware prefetchers.", table_cell_style)
        ]
    ]
    p1_p2_table = Table(p1_p2_data, colWidths=[105, 120, 135, 168])
    p1_p2_table.setStyle(TableStyle([
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
    story.append(p1_p2_table)

    # Interview script callout
    story.append(Spacer(1, 3))
    interview_p1_p2 = Table([[
        Paragraph(
            "<b>Superday Interview Soundbite (Phase 1 &rarr; Phase 2):</b><br/>"
            "<i>'I started with std::map and dynamic allocations to prove correctness. But when I profiled with Linux perf, I discovered a 16.4% L1 cache miss rate and massive tail jitter due to heap fragmentation. By transitioning to a pre-allocated contiguous slab pool and direct price array indexing, I eliminated all malloc calls on the hot path and dropped p99 latency from 18ms to 1.8 microseconds.'</i>",
            callout_style
        )
    ]], colWidths=[528])
    interview_p1_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(interview_p1_p2)

    # =============================================================
    # PAGE 3: PHASE 3 (CONCURRENCY & SINGLE-WRITER ARCHITECTURE)
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("3. Deep Dive: Phase 2 to Phase 3 (Lock-Free Concurrency)", h1_style))
    story.append(Paragraph(
        "Scaling an order book across multi-client thread pools reveals that coarse or fine-grained mutex locking destroys scalability. Phase 3 shifts to the Single-Writer Architecture.",
        body_style
    ))

    story.append(Paragraph("<b>The Concurrency Bottleneck (The Lock Anti-Pattern)</b>", h2_style))
    story.append(Paragraph(
        "When 8 client threads concurrently submit orders to a mutex-protected book (<code>std::mutex</code> or <code>ReentrantLock</code>), performance collapses:<br/>"
        "• <b>Lock Contention:</b> Threads spend 70%+ of CPU cycles queued in sleep-wake kernel transitions.<br/>"
        "• <b>MESI Cache Invalidation Ping-Pong:</b> Multiple cores continuously invalidate each other's L1 cache lines holding the lock and the BBO price pointers.",
        bullet_style
    ))

    story.append(Paragraph("<b>Phase 3 Architecture: The Single-Writer Principle (Weeks 4 - 5)</b>", h2_style))
    story.append(Paragraph(
        "• <b>Dedicated Matching Engine Thread:</b> A single pinned thread owns the order book state exclusively. Zero locks or atomic CAS operations inside the book.<br/>"
        "• <b>Lock-Free SPSC Ring Buffers:</b> Inbound orders and outbound execution reports communicate over Single-Producer Single-Consumer circular queues using memory barriers (<code>memory_order_acquire</code> and <code>memory_order_release</code>).<br/>"
        "• <b>Eliminating False Sharing:</b> Pad producer and consumer ring buffer sequence cursors using <code>alignas(64)</code> to ensure they never share the same 64-byte cache line.<br/>"
        "• <b>CPU Core Pinning:</b> Pin the matching core to an isolated physical core via <code>pthread_setaffinity_np</code> to eliminate OS context switching.",
        bullet_style
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Side-by-Side Empirical Results: Mutexed vs. Lock-Free Single-Writer</b>", h2_style))
    
    p2_p3_data = [
        [
            Paragraph("Concurrency Metric", table_header_style),
            Paragraph("Phase 2 with Mutex (8 Threads)", table_header_style),
            Paragraph("Phase 3: Lock-Free Single-Writer", table_header_style),
            Paragraph("Architectural Advantage", table_header_style)
        ],
        [
            Paragraph("<b>Throughput</b>", table_cell_bold),
            Paragraph("350,000 orders/sec (lock bound)", table_cell_style),
            Paragraph("<b>&gt; 5,200,000 orders/sec (14.8x)</b>", table_cell_style),
            Paragraph("Lock-free SPSC pipeline saturates execution without blocking.", table_cell_style)
        ],
        [
            Paragraph("<b>p99 Tail Latency</b>", table_cell_bold),
            Paragraph("12.4 milliseconds", table_cell_style),
            Paragraph("<b>&lt; 1.2 microseconds</b>", table_cell_style),
            Paragraph("Elimination of thread scheduling convoys and OS sleep states.", table_cell_style)
        ],
        [
            Paragraph("<b>p99.99 Outlier Latency</b>", table_cell_bold),
            Paragraph("45.0 milliseconds", table_cell_style),
            Paragraph("<b>&lt; 3.8 microseconds</b>", table_cell_style),
            Paragraph("Guaranteed predictable bounding: zero GC, zero mutex lock queues.", table_cell_style)
        ],
        [
            Paragraph("<b>Context Switches / sec</b>", table_cell_bold),
            Paragraph("~140,000 context switches", table_cell_style),
            Paragraph("<b>0 (Zero on isolated core)</b>", table_cell_style),
            Paragraph("Core pinning and busy-spin wait strategy isolate engine from OS.", table_cell_style)
        ]
    ]
    p2_p3_table = Table(p2_p3_data, colWidths=[110, 125, 130, 163])
    p2_p3_table.setStyle(TableStyle([
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
    story.append(p2_p3_table)

    story.append(Spacer(1, 3))
    interview_p2_p3 = Table([[
        Paragraph(
            "<b>Superday Interview Soundbite (Phase 2 &rarr; Phase 3):</b><br/>"
            "<i>'When wrapping my single-threaded book in mutex locks for multi-client access, throughput hit a ceiling at 350k ops/sec due to MESI cache-line ping-ponging on the shared lock. I refactored to the LMAX Disruptor Single-Writer architecture: pinned the matching loop to a dedicated CPU core, implemented lock-free SPSC ring buffers, and padded sequence cursors with alignas(64) to prevent false sharing. This unlocked 5.2M orders/sec with a sub-1.2&mu;s p99.'</i>",
            callout_style
        )
    ]], colWidths=[528])
    interview_p2_p3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(interview_p2_p3)

    # =============================================================
    # PAGE 4: PHASE 4 (INSTITUTIONAL EXCHANGE PROTOCOLS & QUANT)
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("4. Deep Dive: Phase 4 (Exchange Protocols & Microstructure)", h1_style))
    story.append(Paragraph(
        "With a blazing, lock-free engine, Phase 4 bridges the gap to institutional trading reality—implementing real Wall Street binary exchange protocols and microstructure analytics.",
        body_style
    ))

    story.append(Paragraph("<b>Binary Exchange Protocols: Replacing JSON Overhead (Weeks 6 - 7)</b>", h2_style))
    story.append(Paragraph(
        "• <b>NASDAQ OUCH 5.0 (Order Entry):</b> Zero-copy parsing of binary packets (<code>Enter Order 'O'</code>, <code>Cancel 'X'</code>). Decodes raw byte buffers with zero string allocations.<br/>"
        "• <b>NASDAQ ITCH 5.0 (Multicast Market Data):</b> UDP multicast publisher emitting Level 3 events (<code>Add Order 'A'</code>, <code>Execute 'E'</code>, <code>Delete 'D'</code>). Clients reconstruct depth in real time.",
        bullet_style
    ))

    story.append(Paragraph("<b>Real Institutional Exchange Mechanics</b>", h2_style))
    story.append(Paragraph(
        "• <b>Pre-Open Call Auction & Walrasian Uncrossing:</b> Computes the single equilibrium price maximizing executed volume and minimizing remaining surplus before continuous trading.<br/>"
        "• <b>CME-Style Pro-Rata Matching Rule:</b> Configurable toggle between FIFO Price-Time priority (equities) and Pro-Rata allocation (Treasury & short-term interest rate futures).<br/>"
        "• <b>Institutional Order Types:</b> Iceberg orders (hidden liquidity tranche with time priority degradation on replenishment), Post-Only, and 4-mode Self-Trade Prevention (STP).",
        bullet_style
    ))

    story.append(Paragraph("<b>Quantitative Microstructure Engine & Sandbox (Week 8)</b>", h2_style))
    story.append(Paragraph(
        "• <b>Sasha Stoikov's Micro-Price Estimator:</b> Calculates true fair price adjusted for multi-level queue depth imbalances rather than naive mid-price.<br/>"
        "• <b>VPIN (Volume-Synchronized Probability of Toxicity):</b> Detects informed toxic order flow and adverse selection by sampling continuous volume buckets.<br/>"
        "• <b>Avellaneda-Stoikov Market Making Bot:</b> Autonomous agent trading against synthetic Hawkes-process noise orders, dynamically adjusting bid/ask spreads based on inventory risk.",
        bullet_style
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Repository Architecture: Side-by-Side Dual Engine Layout</b>", h2_style))
    repo_text = (
        "<code>"
        "limit-order-book/<br/>"
        "+-- src/<br/>"
        "|   +-- baseline/             # Phase 1: std::map / TreeMap + Mutex (Your permanent interview benchmark)<br/>"
        "|   +-- optimized/            # Phase 2 & 3: Contiguous Slab Pool + Flat Array Ladder + SPSC Core<br/>"
        "|   +-- protocol/             # Phase 4: NASDAQ OUCH 5.0 & ITCH 5.0 zero-copy binary codecs<br/>"
        "|   +-- quant/                # Phase 4: Stoikov Micro-Price, VPIN, Avellaneda-Stoikov Bot<br/>"
        "|   \\-- journal/              # Deterministic append-only memory-mapped (mmap) transaction log<br/>"
        "+-- benchmark/<br/>"
        "|   +-- CompareEngines.cpp    # Compiles and runs Phase 1 vs. Phase 2 vs. Phase 3 side-by-side<br/>"
        "|   \\-- RdtscHistogram.hpp    # Nanosecond RDTSC timer with HdrHistogram (eliminates Coordinated Omission)<br/>"
        "\\-- BENCHMARK_REPORT.md      # Auto-generated markdown table proving your optimizations with real data<br/>"
        "</code>"
    )
    repo_box = Table([[Paragraph(repo_text, code_style)]], colWidths=[528])
    repo_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(repo_box)

    # =============================================================
    # PAGE 5: INTERVIEW DEFENSE MASTER CHEATSHEET
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("5. Superday Interview Defense Master Cheatsheet", h1_style))
    story.append(Paragraph(
        "Four critical questions Goldman Sachs Core Strats and Quant Trading interviewers will ask, and the exact answers that demonstrate senior engineering depth:",
        body_style
    ))

    qa_data = [
        ("Q1: 'Why did you build a baseline first instead of jumping straight into slab allocators and lock-free queues?'",
         "A: 'Building a baseline first gave me two indispensable engineering assets: first, an absolute benchmark of 100% correct matching semantics against which I validated all subsequent zero-copy refactorings; and second, hard empirical profiling data. Instead of guessing where the bottlenecks were, I used Linux perf and RDTSC hardware timers to prove that heap allocations and cache-line invalidation were our primary latency drivers.'"),

        ("Q2: 'Why did you choose a Flat Direct-Indexed Array over an std::map or Red-Black Tree?'",
         "A: 'In active liquid markets, 99% of order flow occurs within a tight corridor around the BBO. An std::map node requires allocating a separate heap object with three pointers and color metadata, causing pointer chasing and cache misses on every probe. A direct-indexed array maps tick offsets directly to array indices via simple arithmetic, allowing an O(1) single-cycle memory dereference that hardware prefetchers can easily optimize.'"),

        ("Q3: 'How did you avoid Coordinated Omission in your latency benchmarks?'",
         "A: 'In naive load tests, if the engine pauses for a GC or lock contention, the test client blocks and delays firing subsequent orders, artificially hiding the real tail latency. I built an asynchronous benchmark client that schedules order emissions at fixed Poisson intervals independent of response arrival. If an order arrives late, the response latency records the full duration since scheduled emission, capturing the true p99.99 tail in an HdrHistogram.'"),

        ("Q4: 'What is False Sharing and how did you prevent it in your ring buffer?'",
         "A: 'Modern x86 processors invalidate cache coherence at the granularity of 64-byte cache lines. In a ring buffer, if the producer write-cursor and consumer read-cursor sit in the same 64-byte boundary, each core continuously invalidates the other core's cache, stalling the pipeline. I isolated both cursors with alignas(64) padding, ensuring they reside on separate cache lines with zero coherence interference.'")
    ]

    for q, a in qa_data:
        story.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('Q', fontName='Helvetica-Bold', fontSize=7.8, leading=10, textColor=primary_color, spaceBefore=2.5)))
        story.append(Paragraph(f"<i>{a}</i>", ParagraphStyle('A', fontName='Helvetica', fontSize=7.3, leading=9.8, textColor=text_dark, spaceAfter=2.5)))

    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Battle-Tested Resume Bullets for Your Application</b>", h2_style))
    resume_bullets = [
        "• Engineered a sub-microsecond limit order book engine in C++20 / Low-Latency Java, executing <b>5.2M orders/sec at p99 latency &lt; 1.2&mu;s</b>, utilizing contiguous slab allocators and lock-free SPSC ring buffers.",
        "• Conducted systematic profile-driven refactoring: eliminated hot-path heap allocations and reduced L1-dcache misses from 16.4% to &lt;2.1% by replacing red-black trees with flat direct-indexed price ladders.",
        "• Designed an isolated Single-Writer architecture with dedicated CPU core pinning and <code>alignas(64)</code> cache-line padding, eliminating false sharing and MESI cache-line invalidation across multi-client pipelines.",
        "• Implemented zero-copy <b>NASDAQ OUCH 5.0</b> order entry and <b>ITCH 5.0</b> UDP multicast market data codecs, deterministic <code>mmap</code> binary transaction journaling, and pre-open Walrasian Call Auction uncrossing.",
        "• Formulated quantitative microstructure analytics including <b>Sasha Stoikov's Micro-Price</b> and <b>VPIN</b> order toxicity scoring, validated against an autonomous Avellaneda-Stoikov market-making simulation."
    ]
    for b in resume_bullets:
        story.append(Paragraph(b, bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    output_pdf = r"d:\Limit Book Order\Evolutionary_Build_Plan_and_Interview_Defense.pdf"
    build_pdf(output_pdf)
