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
            self.setFillColor(colors.HexColor("#1E3A8A")) # Deep Blue accent
            self.rect(0, 11 * inch - 6, 8.5 * inch, 6, fill=1, stroke=0)
            self.restoreState()
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.drawString(42, 11 * inch - 26, "WEEK 1 ARCHITECTURAL WALKTHROUGH & CODE DEEP-DIVE")
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(8.5 * inch - 42, 11 * inch - 26, "Phase 1 Baseline: Modern C++20 Limit Order Book")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(42, 11 * inch - 30, 8.5 * inch - 42, 11 * inch - 30)
        
        # Running Footer
        self.line(42, 32, 8.5 * inch - 42, 32)
        self.drawString(42, 22, "Confidential — High-Frequency Trading Systems Architecture Guide | Author: Akash")
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
    accent_blue = colors.HexColor("#1E3A8A")      # Blue 900
    accent_sub = colors.HexColor("#2563EB")       # Blue 600
    text_dark = colors.HexColor("#1E293B")        # Slate 800
    text_muted = colors.HexColor("#64748B")       # Slate 500
    border_color = colors.HexColor("#CBD5E1")     # Slate 300
    callout_bg = colors.HexColor("#EFF6FF")       # Blue 50
    table_alt_bg = colors.HexColor("#F8FAFC")     # Slate 50

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
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
        fontSize=10,
        leading=13,
        textColor=primary_color,
        spaceBefore=6,
        spaceAfter=2.5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=10.5,
        textColor=accent_blue,
        spaceBefore=3.5,
        spaceAfter=1.5,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.6,
        leading=10,
        textColor=text_dark,
        spaceAfter=3
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.8,
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
        fontSize=7.5,
        leading=10,
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
    # PAGE 1: OBJECTIVES & ENVIRONMENT SETUP
    # =============================================================
    story.append(Paragraph("WEEK 1 COMPREHENSIVE CODE WALKTHROUGH & ARCHITECTURE", subtitle_style))
    story.append(Paragraph("Phase 1 Baseline Limit Order Book in Modern C++20", title_style))
    story.append(Paragraph("<b>End-to-End Deep-Dive:</b> Development Toolchains, Domain Types, FIFO Matching Loop, Unit Tests, and RDTSC Latency Profiling", ParagraphStyle('SubSub', fontName='Helvetica', fontSize=7.6, leading=10, textColor=text_muted, spaceAfter=5)))
    
    meta_table_data = [
        [
            Paragraph("<b>Target Stack:</b> Modern C++20 / MSVC 19.51 Optimizing Compiler", meta_style),
            Paragraph("<b>Author / Engineer:</b> Akash", meta_style)
        ],
        [
            Paragraph("<b>Project Phase:</b> Phase 1 Baseline (FIFO Price-Time Priority)", meta_style),
            Paragraph("<b>Deliverable:</b> Verified Core + RDTSC Hardware Benchmark", meta_style)
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[290, 238])
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
            "<b>Week 1 Mission:</b> The goal of Week 1 was <i>not</i> premature micro-optimization. The mission was to establish an indisputable, "
            "100% semantically correct baseline matching engine using standard C++ STL data structures (<code>std::map</code> and <code>std::list</code>), "
            "verify all exchange matching invariants via automated unit tests, and profile execution latency using CPU hardware clock cycles (<code>__rdtsc()</code>) "
            "to discover the empirical memory bottlenecks that justify Phase 2.",
            callout_style
        )
    ]], colWidths=[528])
    callout_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(callout_box)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Toolchain & Environment Configuration", h1_style))
    story.append(Paragraph(
        "Low-latency systems require native 64-bit compilation and modern language features. Here is how the environment was set up:",
        body_style
    ))

    setup_data = [
        [
            Paragraph("Component", table_header_style),
            Paragraph("Discovered / Configured", table_header_style),
            Paragraph("Low-Latency Architectural Impact", table_header_style)
        ],
        [
            Paragraph("<b>Compiler Discovery</b>", table_cell_bold),
            Paragraph("MSVC 19.51 (Visual Studio 2026 Developer BuildTools) detected.", table_cell_style),
            Paragraph("Replaced legacy MinGW 6.3.0 (2016) with an enterprise-grade C++20 optimizing compiler.", table_cell_style)
        ],
        [
            Paragraph("<b>Environment Init</b>", table_cell_bold),
            Paragraph("<code>vcvars64.bat</code> native 64-bit shell initialization.", table_cell_style),
            Paragraph("Configures 64-bit pointer architecture, access to <code>cl.exe</code>, and x86 hardware intrinsics.", table_cell_style)
        ],
        [
            Paragraph("<b>Optimization Flags</b>", table_cell_bold),
            Paragraph("<code>/std:c++20 /O2 /EHsc /W4</code>", table_cell_style),
            Paragraph("Enforces strict C++20 ISO standards, aggressive inlining, loop unrolling, and maximum warning scrutiny.", table_cell_style)
        ],
        [
            Paragraph("<b>Automation Script</b>", table_cell_bold),
            Paragraph("<code>build.bat</code> one-click compilation pipeline.", table_cell_style),
            Paragraph("Automatically builds unit tests, executes test suite, builds benchmark harness, and runs 100k-order test.", table_cell_style)
        ],
        [
            Paragraph("<b>Version Control</b>", table_cell_bold),
            Paragraph("Git repository initialized with <code>.gitignore</code>.", table_cell_style),
            Paragraph("Initial commit recorded: establishes chronological engineering audit trail for interviews.", table_cell_style)
        ]
    ]
    setup_table = Table(setup_data, colWidths=[95, 175, 258])
    setup_table.setStyle(TableStyle([
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
    story.append(setup_table)

    # =============================================================
    # PAGE 2: DOMAIN TYPES & ORDER MODEL
    # =============================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Domain Model & Foundation Types", h1_style))
    story.append(Paragraph(
        "Low-latency architecture begins with careful representation of domain data. Let's inspect <code>Types.hpp</code> and <code>Order.hpp</code>:",
        body_style
    ))

    story.append(Paragraph("<b>File: src/common/Types.hpp</b>", h2_style))
    story.append(Paragraph(
        "• <b><code>enum class Side : uint8_t { BUY = 0, SELL = 1 };</code></b><br/>"
        "  - <i>Why <code>enum class</code>?</i> Strongly typed; prevents accidental comparisons against raw integers.<br/>"
        "  - <i>Why <code>: uint8_t</code>?</i> Default C++ enums take 4 bytes. Specifying <code>uint8_t</code> packs it into <b>1 single byte</b>, minimizing cache-line footprint.<br/>"
        "• <b><code>using Price = uint64_t;</code> (Fixed-Point Arithmetic):</b><br/>"
        "  - <i>The Floating-Point Trap:</i> In IEEE 754 floating-point, <code>0.1 + 0.2 != 0.3</code> due to binary fraction rounding noise. "
        "Exchanges cannot tolerate price calculation drift. We store prices as 64-bit integer ticks (e.g. $100.25 is stored as <code>10025</code> cents). "
        "Comparisons take a single CPU cycle with zero floating-point unit (FPU) stalls.<br/>"
        "• <b><code>using Quantity = uint32_t;</code>:</b> Represents open shares or contracts up to 4.29 billion.<br/>"
        "• <b><code>using OrderId = uint64_t;</code>:</b> Monotonically increasing unique 64-bit identifier.<br/>"
        "• <b><code>using Timestamp = uint64_t;</code>:</b> Nanosecond timestamp or hardware CPU cycle counter recorded at ingress.<br/>"
        "• <b><code>struct Trade</code>:</b> Emitted whenever an incoming order crosses resting liquidity:",
        bullet_style
    ))

    trade_code = (
        "<code>"
        "struct Trade {<br/>"
        "    OrderId   maker_order_id; // Resting passive order already in the book<br/>"
        "    OrderId   taker_order_id; // Aggressive incoming order that took liquidity<br/>"
        "    Price     price;          // Execution price (ALWAYS set by maker's resting price)<br/>"
        "    Quantity  quantity;       // Number of shares executed<br/>"
        "    Timestamp timestamp;      // Execution timestamp<br/>"
        "};"
        "</code>"
    )
    trade_box = Table([[Paragraph(trade_code, code_style)]], colWidths=[528])
    trade_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(trade_box)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>File: src/common/Order.hpp</b>", h2_style))
    story.append(Paragraph(
        "Represents an individual order instance in the system:<br/>"
        "• <code>quantity</code> vs. <code>initial_quantity</code>: As partial fills occur, <code>quantity</code> decrements. "
        "Retaining <code>initial_quantity</code> allows microstructure estimators to track fill ratios.<br/>"
        "• <code>is_filled() const</code>: Inline helper returning <code>quantity == 0</code>.<br/>"
        "• <code>print() const</code>: Formats order details for console debugging.",
        bullet_style
    ))

    # =============================================================
    # PAGE 3: CORE MATCHING ENGINE LOGIC
    # =============================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Core Matching Engine Architecture & Walkthrough", h1_style))
    story.append(Paragraph(
        "In <code>OrderBookBaseline.hpp</code> and <code>OrderBookBaseline.cpp</code>, the limit order book is organized using textbook STL containers:",
        body_style
    ))

    story.append(Paragraph("<b>Data Structures Under the Hood:</b>", h2_style))
    story.append(Paragraph(
        "• <b><code>std::map&lt;Price, std::list&lt;Order&gt;, std::greater&lt;Price&gt;&gt; bids_;</code></b>: "
        "A Red-Black tree storing Bids sorted in descending order. <code>bids_.begin()</code> always points to the <b>Best Bid</b> (highest price).<br/>"
        "• <b><code>std::map&lt;Price, std::list&lt;Order&gt;, std::less&lt;Price&gt;&gt; asks_;</code></b>: "
        "A Red-Black tree storing Asks sorted in ascending order. <code>asks_.begin()</code> always points to the <b>Best Ask</b> (lowest price).<br/>"
        "• <b><code>std::list&lt;Order&gt;</code></b>: A doubly-linked list representing the queue of resting orders at a specific price level in FIFO time order.<br/>"
        "• <b><code>std::unordered_map&lt;OrderId, std::pair&lt;Side, Price&gt;&gt; order_index_;</code></b>: "
        "Hash map enabling fast $O(1)$ lookup for cancellations.",
        bullet_style
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>The 6-Step Matching Algorithm (Inside <code>match_buy_order</code>):</b>", h2_style))
    story.append(Paragraph(
        "<b>Step 1: Spread Verification:</b> While incoming buy quantity $> 0$ and asks exist, inspect <code>best_ask = asks_.begin()</code>. "
        "If <code>incoming_buy.price &lt; best_ask_price</code>, the spread is not crossed. Matching halts.<br/>"
        "<b>Step 2: FIFO Queue Traversal:</b> Access the resting order queue at <code>best_ask_price</code>. Inspect the oldest order at <code>front()</code>.<br/>"
        "<b>Step 3: Trade Execution:</b> Matched quantity is <code>min(incoming_buy.qty, resting_ask.qty)</code>. A <code>Trade</code> event is emitted at the maker's resting price.<br/>"
        "<b>Step 4: Quantity Decrement:</b> Subtract <code>fill_qty</code> from both incoming buy and resting ask. If the resting ask hits 0, pop it from the queue and remove from <code>order_index_</code>.<br/>"
        "<b>Step 5: Empty Level Pruning:</b> If the price level queue becomes empty, erase the price node from <code>asks_</code>.<br/>"
        "<b>Step 6: Passive Resting:</b> If incoming buy order still has open shares, append it to <code>bids_[price].push_back()</code> and register in <code>order_index_</code>.",
        body_style
    ))

    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>Order Cancellation Routine (<code>cancel_order</code>):</b>", h2_style))
    story.append(Paragraph(
        "1. Look up <code>order_id</code> in <code>order_index_</code>. If absent, return <code>false</code>.<br/>"
        "2. Retrieve the order's <code>Side</code> and <code>Price</code>; find the corresponding price level list in <code>bids_</code> or <code>asks_</code>.<br/>"
        "3. Traverse the list, erase the matching order, clean up the price level if empty, and return <code>true</code>.",
        bullet_style
    ))

    # =============================================================
    # PAGE 4: TEST SUITE & VERIFICATION
    # =============================================================
    story.append(PageBreak())
    story.append(Paragraph("4. Correctness Test Suite (BaselineTests.cpp)", h1_style))
    story.append(Paragraph(
        "Financial systems require zero tolerance for execution bugs. <code>BaselineTests.cpp</code> validates 6 mission-critical exchange invariants:",
        body_style
    ))

    test_data = [
        [
            Paragraph("Unit Test Function", table_header_style),
            Paragraph("Scenario Tested", table_header_style),
            Paragraph("Expected Invariant Verified", table_header_style)
        ],
        [
            Paragraph("<b><code>test_passive_resting</code></b>", table_cell_bold),
            Paragraph("Buy @ $100.00, Sell @ $100.50 submitted.", table_cell_style),
            Paragraph("Zero trades generated; BBO correctly reflects $100.00 Bid and $100.50 Ask.", table_cell_style)
        ],
        [
            Paragraph("<b><code>test_exact_fill</code></b>", table_cell_bold),
            Paragraph("Resting Ask 100 @ $100; Incoming Buy 100 @ $100.", table_cell_style),
            Paragraph("1 Trade emitted for 100 shares; book is left completely empty.", table_cell_style)
        ],
        [
            Paragraph("<b><code>test_partial_fill</code></b>", table_cell_bold),
            Paragraph("Resting Ask 200 @ $100; Incoming Buy 50 @ $100.", table_cell_style),
            Paragraph("1 Trade for 50 shares; 150 shares remain resting on the Ask level.", table_cell_style)
        ],
        [
            Paragraph("<b><code>test_multi_level_price_sweep</code></b>", table_cell_bold),
            Paragraph("Asks at $100.00, $100.05, $100.10. Buy 200 @ $100.10.", table_cell_style),
            Paragraph("Sweeps Level 1 and 2 completely, partially fills Level 3; 3 distinct trades emitted.", table_cell_style)
        ],
        [
            Paragraph("<b><code>test_fifo_time_priority</code></b>", table_cell_bold),
            Paragraph("Order A arrives before Order B at the same price.", table_cell_style),
            Paragraph("Incoming cross fills Order A completely before Order B receives a single share.", table_cell_style)
        ],
        [
            Paragraph("<b><code>test_order_cancellation</code></b>", table_cell_bold),
            Paragraph("Cancel resting order; re-cancel same order.", table_cell_style),
            Paragraph("First cancel succeeds and decrements depth; second cancel returns false.", table_cell_style)
        ]
    ]
    test_table = Table(test_data, colWidths=[125, 175, 228])
    test_table.setStyle(TableStyle([
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
    story.append(test_table)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>Console Order Book Depth Ladder Output:</b>", h2_style))
    ladder_text = (
        "<code>"
        "================= ORDER BOOK DEPTH =================<br/>"
        "        ASKS (SELLERS - Lowest First)               <br/>"
        "----------------------------------------------------<br/>"
        "   Price ($)      Shares      Orders<br/>"
        "     150.15         5000           1<br/>"
        "     150.10         2500           1<br/>"
        "     150.05          800           1<br/>"
        "----------------------------------------------------<br/>"
        "&gt;&gt;&gt; SPREAD: $0.05 &lt;&lt;&lt;<br/>"
        "----------------------------------------------------<br/>"
        "        BIDS (BUYERS - Highest First)               <br/>"
        "----------------------------------------------------<br/>"
        "     150.00          500           1<br/>"
        "     149.95         1200           1<br/>"
        "     149.90         3000           1<br/>"
        "===================================================="
        "</code>"
    )
    ladder_box = Table([[Paragraph(ladder_text, code_style)]], colWidths=[528])
    ladder_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), callout_bg),
        ('BOX', (0,0), (-1,-1), 0.75, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(ladder_box)

    # =============================================================
    # PAGE 5: BENCHMARK RESULTS & THE PROFILING DISCOVERY
    # =============================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Hardware Benchmarking & The Profiling Epiphany", h1_style))
    story.append(Paragraph(
        "Using <code>benchmark/BaselineBenchmark.cpp</code>, we calibrated the CPU hardware clock frequency and timed 100,000 synthetic orders:",
        body_style
    ))

    bench_res_data = [
        [
            Paragraph("Metric", table_header_style),
            Paragraph("Measured Value", table_header_style),
            Paragraph("Systems Analysis / Low-Latency Interpretation", table_header_style)
        ],
        [
            Paragraph("<b>Orders Processed</b>", table_cell_bold),
            Paragraph("100,000 orders", table_cell_style),
            Paragraph("50% Buys, 50% Sells, randomized prices around $100.00.", table_cell_style)
        ],
        [
            Paragraph("<b>Trades Executed</b>", table_cell_bold),
            Paragraph("78,243 trades", table_cell_style),
            Paragraph("Demonstrates active matching across dynamic bid/ask spreads.", table_cell_style)
        ],
        [
            Paragraph("<b>Total Wall Time</b>", table_cell_bold),
            Paragraph("21 milliseconds", table_cell_style),
            Paragraph("Whole test completed in a fraction of a blink.", table_cell_style)
        ],
        [
            Paragraph("<b>Throughput</b>", table_cell_bold),
            Paragraph("<b>4,761,905 orders/sec</b>", table_cell_style),
            Paragraph("Warm cache single-threaded execution rate.", table_cell_style)
        ],
        [
            Paragraph("<b>p50 Latency (Median)</b>", table_cell_bold),
            Paragraph("<b>149.8 nanoseconds</b>", table_cell_style),
            Paragraph("Typical fast-path insertion when cache lines are hot.", table_cell_style)
        ],
        [
            Paragraph("<b>p90 Latency</b>", table_cell_bold),
            Paragraph("297.7 nanoseconds", table_cell_style),
            Paragraph("Slight degradation under multi-level traversals.", table_cell_style)
        ],
        [
            Paragraph("<b>p99 Latency</b>", table_cell_bold),
            Paragraph("585.7 nanoseconds", table_cell_style),
            Paragraph("Beginning of Red-Black tree pointer chasing overhead.", table_cell_style)
        ],
        [
            Paragraph("<b>p99.9 Latency</b>", table_cell_bold),
            Paragraph("2,740.8 nanoseconds (2.7&mu;s)", table_cell_style),
            Paragraph("18x degradation from median due to memory allocator stalls.", table_cell_style)
        ],
        [
            Paragraph("<b>Max Latency (Outlier)</b>", table_cell_bold),
            Paragraph("<b>273,349.9 ns (273.3&mu;s)</b>", table_cell_style),
            Paragraph("<b>1,824x LATENCY SPIKE!</b> Caused by heap allocator locks and page faults.", table_cell_style)
        ]
    ]
    bench_table = Table(bench_res_data, colWidths=[105, 120, 303])
    bench_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, table_alt_bg]),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(bench_table)
    story.append(Spacer(1, 3))

    takeaway_box = Table([[
        Paragraph(
            "<b>The Phase 2 Mandate: Why This Number Wins Interviews:</b><br/>"
            "Notice that while the median latency is <b>149.8 nanoseconds</b>, the worst-case outlier spikes to <b>273 microseconds</b> (a 1,824x degradation). "
            "In a real electronic trading environment, a 273-microsecond pause during high volatility results in severe slippage and adverse selection. "
            "This empirical data provides the exact justification for <b>Phase 2 (Weeks 2-3)</b>: replacing <code>std::map</code> and <code>std::list</code> "
            "with a <b>Contiguous Slab Allocator (Object Pool)</b> and <b>Flat Direct-Indexed Price Ladder</b>, eliminating all dynamic heap allocations and crushing tail latency.",
            callout_style
        )
    ]], colWidths=[528])
    takeaway_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#93C5FD")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(takeaway_box)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated: {filename}")

if __name__ == "__main__":
    output_pdf = r"d:\Limit Book Order\Week_1_Deep_Dive_and_Code_Walkthrough.pdf"
    build_pdf(output_pdf)
