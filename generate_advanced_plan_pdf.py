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
            # Top accent bar on cover page
            self.saveState()
            self.setFillColor(colors.HexColor("#1E3A8A"))
            self.rect(0, 11 * inch - 6, 8.5 * inch, 6, fill=1, stroke=0)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(42, 11 * inch - 26, "GOLDMAN SACHS ENG 2027 / QUANTITATIVE EXECUTION ARCHITECTURE")
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(8.5 * inch - 42, 11 * inch - 26, "Institutional-Grade Ultra-Low-Latency LOB")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(42, 11 * inch - 30, 8.5 * inch - 42, 11 * inch - 30)
        
        # Running Footer
        self.line(42, 32, 8.5 * inch - 42, 32)
        self.drawString(42, 22, "Confidential — High-Frequency Trading & Systems Architecture Blueprint | Owner: Akash")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 7.5)
        self.drawRightString(8.5 * inch - 42, 22, page_str)
        self.restoreState()

def build_pdf(filename):
    # Usable width: 612 - 84 = 528 points. Usable height: 792 - 68 = 724 points.
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary_color = colors.HexColor("#0F172A")    # Slate 900
    accent_blue = colors.HexColor("#1E3A8A")      # Blue 900
    accent_sub = colors.HexColor("#2563EB")       # Blue 600
    text_dark = colors.HexColor("#1E293B")        # Slate 800
    text_muted = colors.HexColor("#64748B")       # Slate 500
    border_color = colors.HexColor("#CBD5E1")     # Slate 300
    callout_bg = colors.HexColor("#F8FAFC")       # Slate 50
    table_alt_bg = colors.HexColor("#F8FAFC")     # Slate 50

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=accent_blue,
        spaceAfter=6
    )
    meta_style = ParagraphStyle(
        'MetaText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=text_dark
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=accent_blue,
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=text_dark,
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10.5,
        textColor=text_dark,
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=2.5
    )
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=8.8,
        textColor=colors.HexColor("#0F172A")
    )
    callout_style = ParagraphStyle(
        'Callout_Text',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=text_dark
    )
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=10,
        textColor=colors.white
    )

    story = []

    # =============================================================
    # PAGE 1: COVER & PARADIGM SHIFT (TOY VS. INSTITUTIONAL)
    # =============================================================
    story.append(Paragraph("INSTITUTIONAL QUANTITATIVE ENGINEERING SPECIFICATION", subtitle_style))
    story.append(Paragraph("Ultra-Low-Latency Limit Order Book & Electronic Trading Exchange", title_style))
    story.append(Paragraph("<b>End-to-End Master Blueprint:</b> Sub-Microsecond Matching, Binary Protocols (ITCH/OUCH/SBE), Lock-Free Ring Buffers, and Microstructure Analytics", ParagraphStyle('SubSub', fontName='Helvetica', fontSize=8, leading=11, textColor=text_muted, spaceAfter=6)))
    
    meta_table_data = [
        [
            Paragraph("<b>Target Role:</b> Goldman Sachs Engineering Summer Analyst 2027 / HFT Quant Dev", meta_style),
            Paragraph("<b>Candidate / Owner:</b> Akash", meta_style)
        ],
        [
            Paragraph("<b>Domain Track:</b> Core Strats / Electronic Trading / Low-Latency Systems", meta_style),
            Paragraph("<b>Execution Roadmap:</b> 8-Week Modular Production Build", meta_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[278, 250])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5))

    # Executive Callout
    callout_box = Table([[
        Paragraph(
            "<b>Architectural Directive:</b> Generic limit order book projects (standard Java TreeMap + REST HTTP + basic FIFO) "
            "fail to impress elite interviewers because they ignore mechanical sympathy, cache locality, network protocols, and real exchange mechanics. "
            "This master plan transforms the project into an <b>institutional-grade electronic trading venue</b> that demonstrates zero-allocation memory design, "
            "cache-conscious data structures, binary exchange protocols (NASDAQ ITCH 5.0 / OUCH 5.0), auction uncrossing, quantitative microstructure "
            "(Stoikov Micro-Price, VPIN), and nanosecond-level profiling (RDTSC & PMU hardware counters).",
            callout_style
        )
    ]], colWidths=[528])
    callout_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(callout_box)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Paradigm Shift: Toy vs. Institutional Trading Engine", h1_style))
    story.append(Paragraph(
        "To stand out for Tier-1 investment bank quantitative desks (Goldman Sachs Core Strats, Electronic Trading) and top proprietary trading firms (Jane Street, Citadel Securities, Optiver), "
        "every single layer of the stack must demonstrate <i>mechanical sympathy</i>—designing software to align with CPU cache hierarchies, memory controllers, and network hardware.",
        body_style
    ))

    comp_data = [
        [
            Paragraph("Dimension", table_header_style),
            Paragraph("Generic / Toy Project (Current Baseline)", table_header_style),
            Paragraph("Institutional / Advanced System (This Master Plan)", table_header_style)
        ],
        [
            Paragraph("<b>Memory Management</b>", table_cell_bold),
            Paragraph("Dynamic heap allocations per order (<code>new Order()</code>). Heavy GC churn and 5-50ms latency spikes.", table_cell_style),
            Paragraph("<b>Zero-allocation hot path:</b> Pre-allocated contiguous Slab Allocators & Object Pools. Zero heap churn during matching.", table_cell_style)
        ],
        [
            Paragraph("<b>Data Structures</b>", table_cell_bold),
            Paragraph("<code>TreeMap&lt;Double, Queue&gt;</code>: Red-Black tree pointer-chasing, cache-misses on every price probe.", table_cell_style),
            Paragraph("<b>Price-Indexed Direct Array</b> for BBO spread + Cache-aligned intrusive doubly-linked list. O(1) BBO access, maximum cache line reuse.", table_cell_style)
        ],
        [
            Paragraph("<b>Protocols & I/O</b>", table_cell_bold),
            Paragraph("REST HTTP (JSON) + WebSocket JSON strings. High serialization overhead and connection latency.", table_cell_style),
            Paragraph("<b>Binary Exchange Protocols:</b> NASDAQ OUCH 5.0 (order entry) and NASDAQ ITCH 5.0 (Level 3 binary multicast) via zero-copy SBE/raw buffers.", table_cell_style)
        ],
        [
            Paragraph("<b>Concurrency</b>", table_cell_bold),
            Paragraph("Synchronized blocks or heavy locks. Lock contention bottlenecks throughput under heavy concurrency.", table_cell_style),
            Paragraph("<b>Lock-free SPSC Ring Buffers (Disruptor pattern)</b> with CPU core pinning (<code>pthread_setaffinity_np</code>) and cache-line padding (<code>alignas(64)</code>).", table_cell_style)
        ],
        [
            Paragraph("<b>Exchange Mechanics</b>", table_cell_bold),
            Paragraph("Simple FIFO Limit and Market orders only.", table_cell_style),
            Paragraph("<b>Full Exchange Feature Set:</b> Pro-Rata allocation, Pre-Open Call Auction (Walrasian uncrossing), Iceberg orders, Pegged, Post-Only, and Self-Trade Prevention.", table_cell_style)
        ],
        [
            Paragraph("<b>Microstructure & Quant</b>", table_cell_bold),
            Paragraph("None (simple price matching demo).", table_cell_style),
            Paragraph("<b>Real-time Microstructure Engine:</b> Sasha Stoikov's Micro-Price, Order Flow Toxicity (VPIN), and Avellaneda-Stoikov Market Making simulation.", table_cell_style)
        ],
        [
            Paragraph("<b>Benchmarking Rigor</b>", table_cell_bold),
            Paragraph("Basic wall-clock averages, suffers from Coordinated Omission.", table_cell_style),
            Paragraph("<b>Nanosecond Hardware Timestamping (RDTSC):</b> HdrHistogram (p99/p99.99), and Linux PMU hardware counters (L1 cache misses, branch mispredictions).", table_cell_style)
        ]
    ]
    comp_table = Table(comp_data, colWidths=[90, 210, 228])
    comp_table.setStyle(TableStyle([
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
    story.append(comp_table)
    
    # =============================================================
    # PAGE 2: ADVANCED FINANCIAL CONCEPTS & MICROSTRUCTURE
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("2. Advanced Financial Concepts & Exchange Microstructure", h1_style))
    story.append(Paragraph(
        "To demonstrate genuine domain mastery, the engine implements institutional trading venue mechanisms that go far beyond introductory coursework:",
        body_style
    ))

    concepts = [
        ("1. Pro-Rata Matching vs. Price-Time Priority (FIFO)", 
         "While equities (NASDAQ/NYSE) predominantly use FIFO, short-term interest rate futures (CME SOFR, Eurodollars) and Treasury futures use <b>Pro-Rata allocation</b>. "
         "Under pure Pro-Rata, fills are distributed proportionally to resting order size: <i>Allocation_i = floor(FillQty * Qty_i / TotalDepthAtPrice)</i>. "
         "Implementing both algorithms with a configurable match rule demonstrates deep structural understanding of modern market microstructure."),
        
        ("2. Pre-Open Call Auction & Walrasian Equilibrium Uncrossing", 
         "Real exchanges do not start immediately in continuous trading. Markets open with a <b>Call Auction</b> (accumulating resting orders without matching) "
         "followed by an <b>Uncrossing Cross</b>. The engine calculates the single <i>Equilibrium Clearing Price</i> that: (a) Maximizes matched volume, "
         "(b) Minimizes remaining order imbalance (surplus), and (c) Minimizes distance from the previous reference price. Transitions seamlessly into continuous trading."),
        
        ("3. Institutional Order Types: Iceberg, Pegged, Post-Only & STP", 
         "<b>Iceberg (Reserve) Orders:</b> Rest with a visible display quantity and a hidden reserve; when display is filled, the reserve replenishes the visible book with a new time priority stamp. "
         "<br/><b>Pegged Orders:</b> Dynamically track the BBO (Primary Peg, Market Peg, or Midpoint Peg) as market prices shift without client message churn. "
         "<br/><b>Post-Only (Maker-or-Cancel):</b> Guarantees passive liquidity provision; if the order would cross the spread and take liquidity, it is automatically cancelled. "
         "<br/><b>Self-Trade Prevention (STP):</b> Prevents wash trading between the same trading desk across four modes: Cancel Newest (CN), Cancel Oldest (CO), Decrement and Cancel (DC), and Cancel Both (CB)."),

        ("4. Quantitative Microstructure: Sasha Stoikov's Micro-Price & VPIN", 
         "<b>Stoikov Micro-Price:</b> Unlike the simplistic mid-price <i>(Bid + Ask)/2</i>, the micro-price incorporates queue imbalance across multiple price levels: "
         "<i>P_micro = P_bid * (Q_ask / (Q_bid + Q_ask)) + P_ask * (Q_bid / (Q_bid + Q_ask))</i>, expanded to multi-level depth with Markov transition probabilities. "
         "<br/><b>VPIN (Volume-Synchronized Probability of Toxicity):</b> Quantifies adverse selection and informed order flow toxicity by sampling volume buckets and calculating trade imbalance."),

        ("5. Deterministic Event Sourcing & Memory-Mapped Binary Journal", 
         "Every state-mutating command (Order Enter, Cancel, Amend) is written to a zero-copy append-only memory-mapped file (<code>mmap</code>) with monotonic sequence numbers. "
         "The matching engine operates as a strictly deterministic finite state machine (FSM). Bit-for-bit state recovery is verified by replaying 10 million transactions and asserting state checksums.")
    ]

    for title, desc in concepts:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(desc, body_style))

    # =============================================================
    # PAGE 3: TECH STACK & SYSTEM ARCHITECTURE
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("3. Production-Grade Technology Stack & Mechanics", h1_style))
    story.append(Paragraph(
        "The architecture is designed to reflect the production environments of Goldman Sachs Electronic Trading / Quantitative Execution teams. Two implementation paths are fully supported:",
        body_style
    ))

    stack_data = [
        [
            Paragraph("System Layer", table_header_style),
            Paragraph("Option A: Modern C++20/23 (Recommended HFT Tier)", table_header_style),
            Paragraph("Option B: Low-Latency Zero-GC Java (GS Core Strats Tier)", table_header_style)
        ],
        [
            Paragraph("<b>Core Runtime</b>", table_cell_bold),
            Paragraph("C++20 with Clang 18 / GCC 14. <code>-O3 -march=native -fno-rtti -fno-exceptions</code>. Cache-line aligned data structures.", table_cell_style),
            Paragraph("Java 21+ LTS using <b>Agrona</b> direct off-heap memory buffers and primitive arrays. Zero-allocation hot path, Shenandoah/ZGC.", table_cell_style)
        ],
        [
            Paragraph("<b>Memory Management</b>", table_cell_bold),
            Paragraph("Custom Contiguous Slab Allocator / Object Pool. Static array indexing, intrusive doubly-linked list nodes. Zero <code>malloc</code> in hot path.", table_cell_style),
            Paragraph("Pre-allocated object pools, Flyweight pattern over off-heap <code>Unsafe</code> / Agrona <code>DirectBuffer</code>. Zero GC cycles.", table_cell_style)
        ],
        [
            Paragraph("<b>Concurrency</b>", table_cell_bold),
            Paragraph("Lock-free Single-Producer Single-Consumer (SPSC) Ring Buffers with atomic acquire-release memory semantics. CPU core affinity pinning.", table_cell_style),
            Paragraph("<b>LMAX Disruptor</b> ring buffer with <code>BusySpinWaitStrategy</code>. Dedicated pinned threads per instrument symbol.", table_cell_style)
        ],
        [
            Paragraph("<b>Protocols</b>", table_cell_bold),
            Paragraph("<b>NASDAQ OUCH 5.0</b> (binary order entry) & <b>NASDAQ ITCH 5.0</b> (multicast UDP market data feed). Custom zero-copy binary parser.", table_cell_style),
            Paragraph("<b>Simple Binary Encoding (SBE)</b> or native binary OUCH/ITCH codecs mapped directly over memory buffers.", table_cell_style)
        ],
        [
            Paragraph("<b>Journaling & Audit</b>", table_cell_bold),
            Paragraph("Memory-Mapped Journaling via Linux <code>mmap</code> / Windows Memory-Mapped Files. Asynchronous <code>msync</code> flusher thread.", table_cell_style),
            Paragraph("Agrona <code>MappedByteBuffer</code> / Chronicle Queue for append-only deterministic transaction logging.", table_cell_style)
        ],
        [
            Paragraph("<b>Hardware Profiling</b>", table_cell_bold),
            Paragraph("x86_64 <code>RDTSC</code> hardware timestamping, Linux <code>perf stat</code> (PMU hardware performance counters), Cachegrind.", table_cell_style),
            Paragraph("JNI/Java Panama <code>__rdtsc</code> bindings, Gil Tene's <b>HdrHistogram</b> to eliminate Coordinated Omission.", table_cell_style)
        ],
        [
            Paragraph("<b>Visualization & UI</b>", table_cell_bold),
            Paragraph("High-performance C++ Terminal UI (FTXUI) + WebTransport / WebSocket binary bridge into React Canvas L3 Depth Chart.", table_cell_style),
            Paragraph("React + Canvas/WebGL real-time Level 2 / Level 3 Depth Ladder, Queue Position Tracker, and Live Trade Tape.", table_cell_style)
        ]
    ]
    stack_table = Table(stack_data, colWidths=[88, 220, 220])
    stack_table.setStyle(TableStyle([
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
    story.append(stack_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. System Architecture & Zero-Allocation Memory Layout", h1_style))
    story.append(Paragraph(
        "The architecture is organized around the <b>Single-Writer Principle</b>. To eliminate locking, thread contention, and cache-line invalidation (MESI coherence traffic), "
        "the matching engine core runs on an isolated, pinned CPU core with non-blocking SPSC ring buffer ingress and egress pipelines:",
        body_style
    ))

    arch_box_data = [
        [
            Paragraph("<b>ARCHITECTURAL TOPOLOGY & ZERO-COPY PIPELINE</b>", ParagraphStyle('BoxHead', fontName='Helvetica-Bold', fontSize=8, textColor=accent_blue))
        ],
        [
            Paragraph(
                "<code>"
                "[OUCH 5.0 TCP Clients]  ---&gt;  [Inbound Gateway Thread (Pinned Core 1)]<br/>"
                "                                      |<br/>"
                "                                      v  (Lock-Free SPSC Ring Buffer - Zero Copy)<br/>"
                "                       [Matching Engine Core FSM (Pinned Core 2)]<br/>"
                "                                /                  \\<br/>"
                "      (Lock-Free SPSC Ring Buffer)                  (Lock-Free SPSC Ring Buffer)<br/>"
                "                  /                                          \\<br/>"
                "                 v                                            v<br/>"
                "[Binary Journal Writer (Core 3)]            [ITCH 5.0 Multicast Disseminator (Core 4)]<br/>"
                "   (Zero-Copy mmap file append)                 (UDP Outbound Multicast + Retransmission)<br/>"
                "</code>",
                code_style
            )
        ]
    ]
    arch_box = Table(arch_box_data, colWidths=[528])
    arch_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(arch_box)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Mechanical Sympathy: Cache-Line Layout & Direct Indexing</b>", h2_style))
    story.append(Paragraph(
        "• <b>Direct-Indexed Price Buckets:</b> For active ticks around BBO (&plusmn;500 ticks), price levels are stored in a contiguous array indexed by tick offset (<code>price - min_price</code>). Access is a single <b>O(1) flat array dereference</b> without tree traversal. "
        "<br/>• <b>Intrusive Doubly-Linked Lists:</b> The <code>prev_order_id</code> and <code>next_order_id</code> pointers are embedded directly in pre-allocated <code>Order</code> structs inside the slab pool (zero node allocation). "
        "<br/>• <b>Cache-Line Alignment (<code>alignas(64)</code>):</b> Hot matching data structures and ring buffer cursors are padded to 64 bytes to eliminate <i>false sharing</i>. "
        "<br/>• <b>Fixed-Point Representation:</b> Prices/quantities stored as 64-bit unsigned integers (fixed ticks), eliminating IEEE 754 float inaccuracies and FPU overhead.",
        body_style
    ))

    # =============================================================
    # PAGE 4: 8-WEEK PHASED IMPLEMENTATION PLAN
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("5. Comprehensive Week-by-Week Implementation Plan (Weeks 1 to 8)", h1_style))
    story.append(Paragraph(
        "An intensive, 8-week production roadmap structured with explicit weekly deliverables, code milestones, and testing gates. "
        "Designed to produce an unassailable GitHub portfolio and defensible technical numbers for Goldman Sachs Superday interviews.",
        body_style
    ))

    weeks_all = [
        ("Week 1: Zero-Allocation Memory Architecture & Core Price-Time Book",
         "• Implement fixed-size contiguous Slab Allocator / Object Pool for <code>Order</code>, <code>PriceLevel</code>, and <code>Trade</code> records.<br/>"
         "• Design cache-aligned <code>Order</code> struct with intrusive pointers (<code>next_order</code>, <code>prev_order</code>) and fixed-point integers.<br/>"
         "• Implement Flat Direct-Indexed Price Array for active BBO ticks, with fallback flat sparse map for outlier orders.<br/>"
         "• Implement core FIFO Price-Time matching loop: exact matches, multi-level partial fills, passive resting, cancellations.<br/>"
         "• <b>Deliverable:</b> Standalone zero-allocation matching library with 100% unit test coverage verifying priority preservation."),

        ("Week 2: Advanced Institutional Order Types & Execution Rules",
         "• Implement <b>Iceberg / Reserve Orders:</b> manage visible tranche and hidden pool; enforce time-priority degradation on display replenishment.<br/>"
         "• Implement <b>Post-Only (Maker-or-Cancel)</b> orders: immediate rejection if order would cross resting book and take liquidity.<br/>"
         "• Implement <b>Stop-Loss & Stop-Limit</b> conditional order triggers: maintain off-book trigger registry, activate on trade tick.<br/>"
         "• Implement <b>Self-Trade Prevention (STP)</b> engine supporting 4 regulatory modes: Cancel Newest, Cancel Oldest, Decrement & Cancel, Cancel Both.<br/>"
         "• <b>Deliverable:</b> Comprehensive execution suite testing all complex order transitions and edge cases under adversarial conditions."),

        ("Week 3: Pro-Rata Matching Engine & Pre-Open Call Auction Uncrossing",
         "• Build configurable matching mode: toggle between Price-Time (FIFO) and <b>Pro-Rata Allocation</b>.<br/>"
         "• Implement Pro-Rata integer rounding rules (largest remainder method / deterministic allocation tie-breaker).<br/>"
         "• Build <b>Call Auction State Machine</b> (Pre-Open &rarr; Indicative Price Dissemination &rarr; Auction Match &rarr; Continuous Trading).<br/>"
         "• Implement Walrasian Equilibrium Price algorithm: calculate price maximizing executed volume and minimizing market surplus.<br/>"
         "• <b>Deliverable:</b> Multi-mode matching engine capable of running both equity FIFO auctions and Treasury pro-rata books."),

        ("Week 4: Binary Exchange Protocols: NASDAQ OUCH 5.0 & ITCH 5.0",
         "• Implement <b>OUCH 5.0 binary order entry codec:</b> Enter Order ('O'), Cancel Order ('X'), Order Accepted ('A'), Order Executed ('E').<br/>"
         "• Implement <b>ITCH 5.0 binary market data disseminator:</b> System Event ('S'), Add Order ('A'), Order Executed ('E'), Order Delete ('D').<br/>"
         "• Build zero-copy buffer serializer/deserializer with endianness handling and zero runtime heap allocations.<br/>"
         "• Implement high-throughput UDP multicast feed publisher + TCP snapshot/retransmission session buffer.<br/>"
         "• <b>Deliverable:</b> Networked binary exchange gateway accepting real OUCH packets and multicasting ITCH Level 3 feeds."),

        ("Week 5: Lock-Free Concurrency, Disruptor Ring Buffers & Binary Journaling",
         "• Implement lock-free Single-Producer Single-Consumer (SPSC) Ring Buffers (Disruptor pattern) with memory barriers (acquire/release).<br/>"
         "• Pin Gateway, Matching Engine, Journaler, and ITCH Disseminator to dedicated physical CPU cores (<code>pthread_setaffinity_np</code>).<br/>"
         "• Build zero-copy append-only <b>Memory-Mapped Journal (<code>mmap</code>)</b> with monotonic 64-bit sequence numbers.<br/>"
         "• Implement <b>Deterministic State Recovery:</b> crash the engine, replay 5M journal transactions, and verify bit-for-bit state checksums.<br/>"
         "• <b>Deliverable:</b> Fully concurrent, lock-free, crash-resilient exchange engine operating with zero mutexes on the hot path."),

        ("Week 6: Quantitative Microstructure & Autonomous Market Making Sandbox",
         "• Implement real-time Level 2 (L2) Depth Book Aggregator deriving top 10/50 price levels with Volume-Weighted Average Price (VWAP).<br/>"
         "• Implement <b>Sasha Stoikov's Micro-Price Estimator</b> incorporating multi-level queue imbalances.<br/>"
         "• Implement <b>VPIN (Volume-Synchronized Probability of Toxicity)</b> module to detect toxic order flow and adverse selection.<br/>"
         "• Build an autonomous agent simulation: <b>Avellaneda-Stoikov Market Maker Bot</b> interacting with Hawkes-process synthetic noise traders.<br/>"
         "• <b>Deliverable:</b> Self-contained quantitative trading sandbox demonstrating live order book microstructure dynamics."),

        ("Week 7: Sub-Microsecond Benchmarking, PMU Hardware Profiling & Latency Tuning",
         "• Build nanosecond-precision benchmarking harness using x86_64 <code>RDTSC</code> hardware instructions.<br/>"
         "• Integrate <b>HdrHistogram</b> to record p50, p90, p99, p99.9, and p99.99 tick-to-trade latencies without Coordinated Omission.<br/>"
         "• Profile hardware performance counters using Linux <code>perf stat</code>: L1-dcache misses, LLC misses, branch mispredictions, IPC.<br/>"
         "• Conduct latency optimization study: eliminate false sharing, vectorize data alignment, and unroll critical matching loops.<br/>"
         "• <b>Deliverable:</b> Exhaustive <code>BENCHMARKS.md</code> with defensible, reproducible graphs and optimization case studies."),

        ("Week 8: Full-Stack Real-Time L3 Visualizer, Documentation & GS Interview Defense",
         "• Build high-performance WebSocket/WebTransport binary bridge streaming live L2/L3 order book depth and recent trades.<br/>"
         "• Develop React / Canvas-based real-time frontend: live depth ladder, queue position visualizer, and latency histogram.<br/>"
         "• Author production-grade repository documentation: architecture diagrams, memory layout specs, and design tradeoff analysis.<br/>"
         "• Conduct mock Goldman Sachs Superday interview defense sessions: practice explaining every mechanical decision in under 3 minutes.<br/>"
         "• <b>Deliverable:</b> Polished, publication-grade GitHub repository with interactive demo, benchmark graphs, and defense whitepaper.")
    ]

    for title, tasks in weeks_all:
        story.append(Paragraph(f"<b>{title}</b>", h2_style))
        story.append(Paragraph(tasks, bullet_style))

    # =============================================================
    # PAGE 5: BENCHMARKING TARGETS & RESUME BULLETS
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("6. Rigorous Benchmarking & Hardware Profiling Targets", h1_style))
    story.append(Paragraph(
        "Goldman Sachs interviewers immediately spot fabricated or naive benchmark numbers. "
        "A benchmark must demonstrate that you understand <i>Coordinated Omission</i> (Gil Tene methodology) and have measured hardware counters directly:",
        body_style
    ))

    bench_data = [
        [
            Paragraph("Metric", table_header_style),
            Paragraph("Naive / Generic Project", table_header_style),
            Paragraph("Target for This Advanced Engine", table_header_style),
            Paragraph("Defensible Explanation / Mechanism", table_header_style)
        ],
        [
            Paragraph("<b>Throughput</b>", table_cell_bold),
            Paragraph("10k - 50k orders/sec", table_cell_style),
            Paragraph("<b>&gt; 5,000,000 orders/sec</b> (single core)", table_cell_style),
            Paragraph("Zero heap allocation; lock-free SPSC queue; flat array price indexing.", table_cell_style)
        ],
        [
            Paragraph("<b>p50 Latency</b>", table_cell_bold),
            Paragraph("1.5 - 5.0 milliseconds", table_cell_style),
            Paragraph("<b>&lt; 350 - 450 nanoseconds</b>", table_cell_style),
            Paragraph("O(1) direct price-bucket dereference; intrusive node linking.", table_cell_style)
        ],
        [
            Paragraph("<b>p99 Latency</b>", table_cell_bold),
            Paragraph("15 - 50 milliseconds", table_cell_style),
            Paragraph("<b>&lt; 1.2 microseconds</b>", table_cell_style),
            Paragraph("No GC stop-the-world pauses; CPU core pinned to prevent context switching.", table_cell_style)
        ],
        [
            Paragraph("<b>p99.99 Latency</b>", table_cell_bold),
            Paragraph("&gt; 100 milliseconds", table_cell_style),
            Paragraph("<b>&lt; 3.8 microseconds</b>", table_cell_style),
            Paragraph("Ring buffer size calibrated to L3 cache; zero lock contention.", table_cell_style)
        ],
        [
            Paragraph("<b>L1 Cache Misses</b>", table_cell_bold),
            Paragraph("Unmeasured (&gt; 15%)", table_cell_style),
            Paragraph("<b>&lt; 1.8% L1-dcache misses</b>", table_cell_style),
            Paragraph("Sequential slab allocation; cache-line padding (<code>alignas(64)</code>).", table_cell_style)
        ],
        [
            Paragraph("<b>Branch Miss Rate</b>", table_cell_bold),
            Paragraph("Unmeasured (&gt; 8%)", table_cell_style),
            Paragraph("<b>&lt; 0.9% branch mispredictions</b>", table_cell_style),
            Paragraph("Branchless matching logic; <code>[[likely]]</code> / <code>[[unlikely]]</code> annotations.", table_cell_style)
        ]
    ]
    bench_table = Table(bench_data, colWidths=[80, 95, 140, 213])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, table_alt_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("7. Resume Bullets & Superday Interview Defense", h1_style))
    story.append(Paragraph(
        "How to present and defend this project to technical interviewers at Goldman Sachs, Morgan Stanley, or proprietary trading desks:",
        body_style
    ))

    story.append(Paragraph("<b>Resume Bullet Templates (Battle-Tested)</b>", h2_style))
    resume_bullets = [
        "• Engineered a sub-microsecond limit order book matching engine in C++20 / Low-Latency Java sustaining <b>5.2M orders/sec at p99 latency &lt; 1.2&mu;s</b>, utilizing contiguous slab allocators and lock-free SPSC ring buffers.",
        "• Implemented <b>NASDAQ ITCH 5.0 Level 3 multicast publisher</b> and <b>OUCH 5.0 binary order entry gateway</b>, eliminating JSON serialization overhead and achieving zero heap allocations on the critical path.",
        "• Designed dual-mode execution supporting <b>FIFO Price-Time</b> and <b>CME-style Pro-Rata allocation</b>, alongside pre-open Call Auction uncrossing utilizing Walrasian equilibrium clearing price discovery.",
        "• Built an automated quantitative microstructure sandbox incorporating <b>Stoikov's Micro-Price</b>, real-time <b>VPIN toxicity scoring</b>, and an <b>Avellaneda-Stoikov market-making agent</b> simulating adversarial order flow.",
        "• Benchmarked tick-to-trade latency using hardware <b>RDTSC timestamping</b> and <b>HdrHistogram</b> to prevent Coordinated Omission; profiled CPU PMU counters with <code>perf stat</code>, achieving &lt;1.5% L1-dcache misses."
    ]
    for b in resume_bullets:
        story.append(Paragraph(b, bullet_style))

    # =============================================================
    # PAGE 6: INTERVIEW DEFENSE Q&A & REPO BLUEPRINT
    # =============================================================
    story.append(PageBreak())

    story.append(Paragraph("<b>Crucial Interview Defense Questions & Answering Strategy</b>", h1_style))
    qa_list = [
        ("Q1: Why did you avoid Red-Black Trees (std::map / TreeMap) for price levels?",
         "A: Red-Black trees allocate individual heap nodes for each price level, causing pointer-chasing and CPU cache misses across the memory bus. "
         "Instead, I implemented a Direct-Indexed Price Bucket array for active ticks around the BBO (O(1) flat array lookup with zero pointer traversal) "
         "paired with an intrusive doubly-linked list embedded inside pre-allocated slab orders."),

        ("Q2: How do you handle Coordinated Omission in your latency benchmarks?",
         "A: In naive load testing, if the server pauses (e.g. GC or cache stall), a synchronous test client halts and delays firing the next order, artificially masking the tail latency. "
         "I built an asynchronous harness that schedules order emissions at fixed Poisson intervals independent of response arrival, tracking scheduled vs. actual arrival times via HdrHistogram."),

        ("Q3: How do you prevent false sharing in your multi-threaded ring buffer?",
         "A: Modern x86 CPUs maintain cache coherence in 64-byte cache lines. If the producer write-pointer and consumer read-pointer reside in the same 64-byte line, "
         "the cores continuously invalidate each other's L1/L2 caches (cache ping-ponging). I explicitly aligned and padded ring buffer cursors using alignas(64) to ensure cache-line isolation."),

        ("Q4: How does your Call Auction Walrasian clearing price resolve tie-breakers?",
         "A: If multiple prices yield identical maximum executable volume, the engine chooses the price with the minimum imbalance surplus. "
         "If surplus is also identical, it selects the price nearest to the previous trading session's official closing reference price.")
    ]
    for q, a in qa_list:
        story.append(Paragraph(f"<b>{q}</b>", ParagraphStyle('QStyle', fontName='Helvetica-Bold', fontSize=8, textColor=primary_color, spaceBefore=3)))
        story.append(Paragraph(f"<i>{a}</i>", ParagraphStyle('AStyle', fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=text_dark, spaceAfter=2.5)))

    story.append(Spacer(1, 6))

    story.append(Paragraph("8. Production Repository Blueprint", h1_style))
    repo_blueprint = (
        "<code>"
        "limit-order-book-hft/<br/>"
        "+-- CMakeLists.txt / pom.xml         # Modern C++20 build or Maven with Agrona/Disruptor<br/>"
        "+-- src/<br/>"
        "|   +-- core/                        # Matching Engine Core (Zero-allocation FSM)<br/>"
        "|   |   +-- OrderBook.hpp / .cpp     # Direct-indexed flat price ladder & intrusive book<br/>"
        "|   |   +-- MatchingEngine.hpp       # Price-Time & Pro-Rata continuous matching loop<br/>"
        "|   |   +-- CallAuction.hpp          # Walrasian equilibrium clearing price uncrossing<br/>"
        "|   |   \\-- SlabAllocator.hpp        # Pre-allocated memory pool (zero malloc on hot path)<br/>"
        "|   +-- protocol/                    # Binary Exchange Protocols<br/>"
        "|   |   +-- OuchCodec.hpp            # NASDAQ OUCH 5.0 binary order entry parser/encoder<br/>"
        "|   |   \\-- ItchPublisher.hpp        # NASDAQ ITCH 5.0 UDP multicast Level 3 feed generator<br/>"
        "|   +-- concurrency/                 # Lock-Free Concurrency & Journaling<br/>"
        "|   |   +-- SpscRingBuffer.hpp       # Lock-free SPSC ring buffer with 64-byte cache padding<br/>"
        "|   |   \\-- BinaryJournal.hpp        # Zero-copy memory-mapped file (mmap) audit journal<br/>"
        "|   +-- quant/                       # Microstructure & Simulation Sandbox<br/>"
        "|   |   +-- MicroPrice.hpp           # Sasha Stoikov multi-level order book micro-price<br/>"
        "|   |   +-- VpinCalculator.hpp       # Volume-synchronized probability of toxicity<br/>"
        "|   |   \\-- MarketMakerBot.hpp       # Avellaneda-Stoikov automated market maker bot<br/>"
        "|   \\-- ui_bridge/                   # WebSocket / WebTransport binary feed gateway<br/>"
        "+-- test/                            # Comprehensive Unit & Concurrency Test Suite<br/>"
        "|   +-- MatchingCorrectnessTest.cpp  # Exhaustive order type & priority verification<br/>"
        "|   +-- ProRataValidationTest.cpp    # CME-style pro-rata allocation tests<br/>"
        "|   \\-- DeterministicReplayTest.cpp  # Crash recovery and bit-for-bit state checksum replay<br/>"
        "+-- benchmark/                       # Nanosecond Hardware Benchmarks<br/>"
        "|   +-- RdtscHarness.cpp             # Hardware RDTSC latency recorder + HdrHistogram<br/>"
        "|   \\-- perf_profile.sh              # Linux perf script capturing L1 cache misses & IPC<br/>"
        "+-- visualizer/                      # React / Canvas Level 3 Order Book Depth Visualizer<br/>"
        "+-- docs/                            # High-Frequency Trading Whitepaper & Architecture Specs<br/>"
        "+-- README.md                        # Institutional overview with real benchmark graphs<br/>"
        "\\-- RESULTS.md                       # Defensible latency percentiles (p50, p95, p99, p99.99)<br/>"
        "</code>"
    )
    repo_box = Table([[Paragraph(repo_blueprint, code_style)]], colWidths=[528])
    repo_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(repo_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    output_pdf = r"d:\Limit Book Order\Institutional_Limit_Order_Book_HFT_Engine_Master_Plan.pdf"
    build_pdf(output_pdf)
