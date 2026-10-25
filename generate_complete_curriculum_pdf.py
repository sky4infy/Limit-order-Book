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
        self.drawString(42, 11 * inch - 26, "WEEKS 1 & 2 COMPLETE TEACHING CURRICULUM — ZERO-TO-HERO")
        
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawRightString(8.5 * inch - 42, 11 * inch - 26, "Market Microstructure & Mechanical Sympathy")

        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(42, 11 * inch - 30, 8.5 * inch - 42, 11 * inch - 30)
        
        # Running Footer
        self.line(42, 32, 8.5 * inch - 42, 32)
        self.setFont("Helvetica", 7.5)
        self.drawString(42, 22, "Institutional Limit Order Book Project | Engineering Masterclass | Akash")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 7.5)
        self.drawRightString(8.5 * inch - 42, 22, page_str)
        self.restoreState()

def build_pdf(filename="Week_1_and_Week_2_Complete_Teaching_Curriculum.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=42,
        rightMargin=42,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    c_primary = colors.HexColor("#0F172A")    # Slate 900
    c_navy = colors.HexColor("#1E3A8A")       # Blue 900
    c_teal = colors.HexColor("#0D9488")       # Teal 600
    c_slate = colors.HexColor("#334155")      # Slate 700
    c_light_bg = colors.HexColor("#F8FAFC")   # Slate 50
    c_code_bg = colors.HexColor("#F1F5F9")    # Slate 100
    c_border = colors.HexColor("#E2E8F0")     # Slate 200

    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=21,
        leading=25,
        textColor=c_primary,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=c_teal,
        spaceAfter=12
    )
    h1_style = ParagraphStyle(
        "CustomH1",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=c_navy,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "CustomH2",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13.5,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.5,
        textColor=c_slate,
        spaceAfter=5
    )
    code_style = ParagraphStyle(
        "CodeText",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )
    callout_style = ParagraphStyle(
        "Callout",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("Weeks 1 & 2: Complete HFT Teaching Curriculum", title_style))
    story.append(Paragraph("From Absolute Market Zero to Hardware-Level Mechanical Sympathy — Every Concept Taught Through Code", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_navy, spaceBefore=0, spaceAfter=8))

    # Meta banner
    meta_data = [
        [
            Paragraph("<b>Focus:</b> Market Microstructure & Computer Architecture", body_style),
            Paragraph("<b>Target Audience:</b> Quant Developers & HFT Core Engineers", body_style),
            Paragraph("<b>Companion Code:</b> 7 Source/Test/Benchmark Files", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[2.6*inch, 2.7*inch, 2.2*inch])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_light_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    # PART I HEADER
    story.append(Paragraph("PART I: WEEK 1 — FINANCIAL MARKET MECHANICS & C++20 ORDER BOOK", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_teal, spaceBefore=2, spaceAfter=6))

    # Ch 1
    story.append(Paragraph("1. What Is a Stock Exchange & Limit Order Book?", h2_style))
    story.append(Paragraph(
        "A Limit Order Book (LOB) is an electronic double-sided auction that organizes unexecuted orders into two queues: "
        "<b>Bids</b> (buyers sorted descending by price) and <b>Asks</b> (sellers sorted ascending by price). The difference between the highest "
        "bid and lowest ask is the <b>Spread</b>. Trades execute when an incoming order crosses this spread.",
        body_style
    ))

    # Ladder diagram box
    ladder_text = """        ASKS (Sellers - Ascending)
-------------------------------------------
  $150.15   | 5000 shares
  $150.10   | 2500 shares
  $150.05   |  800 shares   <-- BEST ASK (Lowest Seller)
-------------------------------------------
  >>> SPREAD: $0.05 (Gap between Best Bid & Best Ask) <<<
-------------------------------------------
  $150.00   |  500 shares   <-- BEST BID (Highest Buyer)
  $149.95   | 1200 shares
  $149.90   | 3000 shares
-------------------------------------------
        BIDS (Buyers - Descending)"""
    t_ladder = Table([[Preformatted(ladder_text, code_style)]], colWidths=[7.4*inch])
    t_ladder.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_ladder)
    story.append(Spacer(1, 6))

    # Ch 2 & 3
    story.append(Paragraph("2. Price-Time Priority (FIFO) & Maker-Taker Asymmetry", h2_style))
    story.append(Paragraph(
        "<b>Price-Time Priority:</b> Higher bids and lower asks always take priority. If prices match, arrival time determines priority (FIFO). "
        "In our engine, each price level maintains a <code>std::list&lt;Order&gt;</code> where new orders arrive at the tail (<code>push_back</code>) "
        "and fills consume from the front (<code>front()</code>).<br/>"
        "<b>Maker-Taker Pricing:</b> The passive resting order is the <b>Maker</b>. The incoming aggressive order is the <b>Taker</b>. "
        "<b>Crucial rule:</b> Execution price is ALWAYS the Maker's resting price, granting price improvement to aggressive orders.",
        body_style
    ))

    # Ch 4: Matching Code
    story.append(Paragraph("3. The Two-Loop Matching Engine Algorithm", h2_style))
    story.append(Paragraph(
        "In <code>OrderBookBaseline::match_buy_order()</code>, matching operates in two nested loops: "
        "Outer loop traverses ask price levels from lowest upwards; inner loop sweeps FIFO resting orders at each price level.",
        body_style
    ))

    code_snippet1 = """// From src/baseline/OrderBookBaseline.cpp
while (incoming_buy.quantity > 0 && !asks_.empty()) {
    auto best_ask_it = asks_.begin();
    if (incoming_buy.price < best_ask_it->first) break; // Cannot cross spread

    auto& resting_queue = best_ask_it->second;
    while (incoming_buy.quantity > 0 && !resting_queue.empty()) {
        Order& resting_ask = resting_queue.front(); // FIFO: Oldest order first
        Quantity fill = std::min(incoming_buy.quantity, resting_ask.quantity);
        trades.push_back(Trade{ .price = best_ask_it->first, .quantity = fill, ... });
        incoming_buy.quantity -= fill;
        resting_ask.quantity -= fill;
        if (resting_ask.is_filled()) {
            order_index_.erase(resting_ask.order_id);
            resting_queue.pop_front();
        }
    }
    if (resting_queue.empty()) asks_.erase(best_ask_it); // Prune empty price node
}"""
    t_code1 = Table([[Preformatted(code_snippet1, code_style)]], colWidths=[7.4*inch])
    t_code1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_code1)
    story.append(Spacer(1, 6))

    # Ch 5 & 6: Modern C++20
    story.append(Paragraph("4. Modern C++20 Strong Typing & Integer Ticks", h2_style))
    story.append(Paragraph(
        "Floating-point (<code>double</code>) fails due to IEEE-754 binary rounding errors (e.g., 0.1 + 0.2 != 0.3). "
        "In our codebase (<code>src/common/Types.hpp</code>), prices are stored as 64-bit unsigned integers representing fixed cents/ticks. "
        "Furthermore, <code>enum class Side : uint8_t</code> enforces type safety while shrinking enum storage from 4 bytes to 1 byte.",
        body_style
    ))

    # Baseline Benchmark Metrics Table
    story.append(Paragraph("5. Week 1 Baseline Benchmark Results", h2_style))
    bench_data = [
        ["Metric", "Measured Value", "Root Cause in Phase 1 Baseline Architecture"],
        ["Throughput", "602,410 orders/sec", "Restricted by malloc/free overhead and pointer-chasing traversals"],
        ["p50 Latency (Median)", "838.9 ns", "Average time for single order traversal through map and list"],
        ["p99 Latency", "3,843.3 ns", "Cache misses during multi-level sweep and deep queue iterations"],
        ["p99.9 Latency", "83,626.2 ns (83.6 us)", "Heap lock contention during node allocation and Red-Black tree rebalance"],
        ["Max Latency Outlier", "3,755,147.9 ns (3.7 ms)", "OS page fault / memory manager arena expansion on node malloc"]
    ]
    t_bench = Table(bench_data, colWidths=[1.8*inch, 1.8*inch, 3.8*inch])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    # Page Break for Part II
    story.append(PageBreak())

    # PART II HEADER
    story.append(Paragraph("PART II: WEEK 2 — COMPUTER ARCHITECTURE & MECHANICAL SYMPATHY", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_teal, spaceBefore=2, spaceAfter=6))

    # Memory Hierarchy
    story.append(Paragraph("6. The Memory Wall & CPU Cache Hierarchy", h2_style))
    story.append(Paragraph(
        "A 2.50 GHz CPU executes one instruction in 0.40 ns. Fetching a cache line from DRAM requires ~80 ns (200 idle cycles). "
        "Optimizing algorithms from O(log N) to O(1) is futile if data structures cause continuous DRAM trips.",
        body_style
    ))

    mem_data = [
        ["Level", "Size", "Latency", "Clock Cycles", "Hardware Characteristics"],
        ["L1 Cache", "32 KB - 48 KB", "~1.0 ns", "2 - 4 cycles", "Core-private, single-cycle SRAM, ultrafast"],
        ["L2 Cache", "512 KB - 1.25 MB", "~3.5 ns", "10 - 14 cycles", "Core-private, mid-tier cache"],
        ["L3 Cache", "16 MB - 36 MB", "~12.0 ns", "35 - 50 cycles", "Shared across all cores on the die"],
        ["Main DRAM", "16 GB - 64 GB", "~80.0 ns", "180 - 220 cycles", "Off-chip capacitor banks. CPU stalls completely!"]
    ]
    t_mem = Table(mem_data, colWidths=[1.1*inch, 1.3*inch, 1.0*inch, 1.2*inch, 2.8*inch])
    t_mem.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_mem)
    story.append(Spacer(1, 8))

    # CacheBenchmark Findings
    story.append(Paragraph("7. Empirical Proof: CacheBenchmark Findings (1M Elements)", h2_style))
    cache_bench_data = [
        ["Benchmark Test", "Access Pattern", "Measured Result", "Speed Ratio", "Physical Hardware Reason"],
        ["Vector vs List", "std::vector vs std::list", "0.74 ms vs 11.00 ms", "14.8x FASTER", "Vector: sequential cache reuse. List: pointer chasing across DRAM."],
        ["Sequential vs Random", "Sequential vs Shuffled", "0.65 ms vs 6.64 ms", "10.2x FASTER", "Stream prefetcher detects constant strides; random access stalls on DRAM."],
        ["Cold vs Warm", "First Pass vs Second Pass", "0.72 ms vs 0.65 ms", "1.1x FASTER", "Warm cache hits L1/L2 directly; cold pass brings cache lines into hierarchy."]
    ]
    t_cb = Table(cache_bench_data, colWidths=[1.3*inch, 1.4*inch, 1.2*inch, 1.0*inch, 2.5*inch])
    t_cb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_teal),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_cb)
    story.append(Spacer(1, 8))

    # Struct Memory Layout & Padding
    story.append(Paragraph("8. Memory Layout Analysis: Dead Padding & Cache Line Splitting", h2_style))
    story.append(Paragraph(
        "Inspected via <code>test/MemoryLayoutTests.cpp</code> on 64-bit MSVC: <code>Order</code> struct requires 40 bytes, but holds only 33 bytes of data. "
        "The compiler inserts <b>7 bytes of dead padding</b> between <code>side</code> (offset 8) and <code>price</code> (offset 16) to enforce 8-byte alignment.",
        body_style
    ))

    layout_text = """Byte Offsets  | Field Name        | Type     | Size     | Alignment & Notes
---------------------------------------------------------------------------------------
[0x00..0x07]  | order_id          | uint64_t | 8 bytes  | Aligned at offset 0
[0x08]        | side              | uint8_t  | 1 byte   | Aligned at offset 8
[0x09..0x0F]  | *** DEAD PADDING* | ---      | 7 bytes  | Wasted padding to align price to % 8 == 0
[0x10..0x17]  | price             | uint64_t | 8 bytes  | Aligned at offset 16
[0x18..0x1B]  | quantity          | uint32_t | 4 bytes  | Aligned at offset 24
[0x1C..0x1F]  | initial_quantity  | uint32_t | 4 bytes  | Packs tightly at offset 28
[0x20..0x27]  | timestamp         | uint64_t | 8 bytes  | Aligned at offset 32
Total Size: 40 bytes (33 bytes data + 7 bytes waste). Cache line splits: 64 / 40 = 1.6 orders/line."""
    t_lay = Table([[Preformatted(layout_text, code_style)]], colWidths=[7.4*inch])
    t_lay.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
        ('BOX', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_lay)
    story.append(Spacer(1, 8))

    # Architecture Bridge: Week 1 to Week 2
    story.append(Paragraph("9. The Architecture Bridge: Week 1 Bottleneck -> Phase 2 Zero-Allocation Fix", h2_style))
    bridge_data = [
        ["Phase 1 Component", "Baseline Data Structure", "Hardware Bottleneck Diagnosed in Week 2", "Phase 2 Production Solution"],
        ["Price Levels", "std::map (Red-Black)", "Pointer chasing down tree nodes; 5-10 cache misses", "Direct-indexed flat array: levels[2000], O(1) single index"],
        ["Queue Iteration", "std::list (Doubly-Linked)", "14.8x slower; separate node mallocs; DRAM stalls", "Intrusive linked list inside pre-allocated slab"],
        ["Order Allocation", "new Order() on hot path", "100k malloc calls; heap locks; latency spikes", "Contiguous Slab Allocator: pre-allocated ring buffer"],
        ["Order Lookup", "std::unordered_map", "Hash collision chaining; rehashing latency cliff", "Flat direct-address dense table: order_index[1M]"],
        ["Struct Layout", "40-byte unaligned Order", "7 dead bytes (17.5%); 1.6 orders/cache line", "Pack flags and intrusive list indices into dead padding"]
    ]
    t_br = Table(bridge_data, colWidths=[1.2*inch, 1.4*inch, 2.3*inch, 2.5*inch])
    t_br.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.2),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_br)
    story.append(Spacer(1, 10))

    # Page Break for Part III & IV
    story.append(PageBreak())

    # PART III HEADER
    story.append(Paragraph("PART III: SOCRATIC DRILLS & 14-DAY STUDY ROADMAP", h1_style))
    story.append(HRFlowable(width="100%", thickness=0.8, color=c_teal, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph("10. Hands-on Socratic Practice Drills", h2_style))
    story.append(Paragraph(
        "<b>Drill A (Engine Trace):</b> Bids resting @ $100.00 (300 shs). Asks resting @ $100.10 (100 shs) and $100.20 (200 shs). "
        "Incoming: BUY 250 @ $100.20.<br/>"
        "<i>Answer:</i> 2 trades executed. Trade 1: 100 shs @ $100.10 (Maker: Ask 1, Taker: Buy). Trade 2: 150 shs @ $100.20 (Maker: Ask 2, Taker: Buy). "
        "Remaining: Ask 2 rests 50 shs @ $100.20. New spread: $0.20 ($100.00 - $100.20). Tested in <code>test_multi_level_sweep()</code>.<br/>"
        "<b>Drill B (Padding Math):</b> Struct with <code>uint8_t a; uint64_t b; uint16_t c; uint32_t d;</code>.<br/>"
        "<i>Answer:</i> Offset a=0; 7 bytes pad; offset b=8; offset c=16; 2 bytes pad; offset d=20; Total=24 bytes (15 data + 9 waste). Reordered to b,d,c,a = 16 bytes (33% saved!).<br/>"
        "<b>Drill C (Memory Penalty):</b> Iterating 1M elements via vector vs list.<br/>"
        "<i>Answer:</i> Vector streams via hardware prefetcher (~0.7 ns/elem = 0.7 ms). List pointer chases randomly across DRAM (~80 ns/elem = 80 ms).",
        body_style
    ))

    story.append(Spacer(1, 4))
    story.append(Paragraph("11. 14-Day Structured Mastery Schedule", h2_style))
    sched_data = [
        ["Day", "Topic Focus", "Code Files to Inspect", "Action Item"],
        ["1-2", "Market Fundamentals & Types", "src/common/Types.hpp, Order.hpp", "Trace integer tick arithmetic & enum class side storage."],
        ["3-5", "Baseline Engine & Matching", "src/baseline/OrderBookBaseline.cpp", "Step through match_buy_order, cancel_order, modify_order."],
        ["6-7", "Verification & Benchmarking", "test/BaselineTests.cpp, BaselineBenchmark.cpp", "Compile and run bin/BaselineTests.exe and bin/BaselineBenchmark.exe."],
        ["8-10", "Computer Architecture & Prefetch", "benchmark/CacheBenchmark.cpp", "Execute CacheBenchmark.exe; analyze 14.8x vector speedup."],
        ["11-12", "Struct Layout & Heap Jitter", "test/MemoryLayoutTests.cpp", "Run MemoryLayoutTests.exe; calculate padding offsets."],
        ["13-14", "Architectural Defense & Bridge", "PHASED_BUILD_PLAN_AND_INTERVIEW_DEFENSE.md", "Rehearse institutional interview questions using your measured data."]
    ]
    t_sc = Table(sched_data, colWidths=[0.6*inch, 2.0*inch, 2.6*inch, 2.2*inch])
    t_sc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_navy),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sc)
    story.append(Spacer(1, 10))

    # Defense Checklist
    story.append(Paragraph("12. Institutional Interview Competency Checklist", h2_style))
    story.append(Paragraph(
        "By completing this syllabus, you can defend the following topics with empirical numbers from your own engine:<br/>"
        "- <b>Market Microstructure:</b> Order ladder mechanics, spread calculation, price improvement, FIFO priority rules.<br/>"
        "- <b>C++20 Type Safety:</b> Integer ticks vs floating-point representation, <code>enum class : uint8_t</code> packing, <code>std::optional</code>.<br/>"
        "- <b>Hardware Architecture:</b> The Memory Wall, 64-byte cache lines, spatial/temporal locality, hardware prefetching.<br/>"
        "- <b>Memory Optimization:</b> Struct field packing, alignment rules, cache line boundary splitting, heap allocation elimination.<br/>"
        "- <b>HFT Benchmarking:</b> Sub-nanosecond TSC measurement (<code>__rdtsc</code>), CPU frequency calibration, latency tail percentiles.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    build_pdf()
