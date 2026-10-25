import sys
import os
import re
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
        textColor=c_primary, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        "CoverSubtitle", parent=styles["Normal"],
        fontName="Helvetica", fontSize=9.5, leading=13.5,
        textColor=c_teal, spaceAfter=10
    )
    h1_style = ParagraphStyle(
        "CustomH1", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=12, leading=15,
        textColor=c_navy, spaceBefore=10, spaceAfter=5, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "CustomH2", parent=styles["Normal"],
        fontName="Helvetica-Bold", fontSize=10, leading=13,
        textColor=c_primary, spaceBefore=8, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        "CustomBody", parent=styles["Normal"],
        fontName="Helvetica", fontSize=8.2, leading=11.2,
        textColor=c_slate, spaceAfter=4
    )
    quote_style = ParagraphStyle(
        "CustomQuote", parent=styles["Normal"],
        fontName="Helvetica-Oblique", fontSize=8, leading=11,
        textColor=colors.HexColor("#1E293B")
    )
    code_style = ParagraphStyle(
        "CustomCode", parent=styles["Normal"],
        fontName="Courier", fontSize=7.2, leading=9.2,
        textColor=colors.HexColor("#0F172A")
    )

    story = []
    story.append(Paragraph(doc_title, title_style))
    story.append(Paragraph(subtitle, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=c_navy, spaceBefore=0, spaceAfter=8))

    for sec in sections:
        if sec["type"] == "h1":
            story.append(Paragraph(sec["text"], h1_style))
            story.append(HRFlowable(width="100%", thickness=0.6, color=c_teal, spaceBefore=1, spaceAfter=4))
        elif sec["type"] == "h2":
            story.append(Paragraph(sec["text"], h2_style))
        elif sec["type"] == "body":
            story.append(Paragraph(sec["text"], body_style))
        elif sec["type"] == "quote":
            t_q = Table([[Paragraph(sec["text"], quote_style)]], colWidths=[7.4*inch])
            t_q.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8FAFC")),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
                ('LINEBEFORE', (0,0), (0,0), 3, c_navy),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_q)
            story.append(Spacer(1, 4))
        elif sec["type"] == "code":
            t_c = Table([[Preformatted(sec["text"], code_style)]], colWidths=[7.4*inch])
            t_c.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), c_code_bg),
                ('BOX', (0,0), (-1,-1), 0.5, c_border),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(t_c)
            story.append(Spacer(1, 4))
        elif sec["type"] == "table":
            t = Table(sec["data"], colWidths=sec.get("colWidths", None))
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), c_navy),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,-1), 7.2),
                ('GRID', (0,0), (-1,-1), 0.5, c_border),
                ('TOPPADDING', (0,0), (-1,-1), 2.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
                ('LEFTPADDING', (0,0), (-1,-1), 4),
                ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ]))
            story.append(t)
            story.append(Spacer(1, 5))
        elif sec["type"] == "pagebreak":
            story.append(PageBreak())

    def canvas_factory(*args, **kwargs):
        c = NumberedCanvas(*args, **kwargs)
        c.header_title = header_title
        return c

    doc.build(story, canvasmaker=canvas_factory)
    print(f"Generated {filename} successfully.")

def build_week1_interview_pdf():
    sections = [
        {"type": "h1", "text": "1. Executive Overview & The Interviewer's Evaluation Criteria"},
        {"type": "body", "text": "When interviewing for Quant Development or Core Systems at Citadel, Jane Street, Optiver, HRT, or Goldman Sachs, interviewers evaluate four competencies: Financial Domain Fluency, Algorithmic & Big-O Tradeoffs, Numerical Rigor (IEEE-754 floating point hazards), and Defensible Low-Latency C++ Systems Architecture."},
        {"type": "h1", "text": "2. Financial Market Microstructure & Exchange Mechanics"},
        {"type": "h2", "text": "Q1: How does a double-auction Limit Order Book operate? Continuous trading vs Call auction?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> An LOB is a double-sided continuous auction aggregating Bids (buyers descending) and Asks (sellers ascending). In Continuous Trading, matches occur instantly when incoming orders cross the spread. In Call Auctions (Pre-Open / Closing Cross), orders accumulate and match at an uncrossing time at a single clearing price that maximizes volume and minimizes market imbalance."},
        {"type": "h2", "text": "Q2: What is Price-Time Priority (FIFO)? Why Equities use FIFO vs Pro-Rata in Interest Rate Futures?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> Price Priority dictates that better prices always execute first. Time Priority dictates that identical prices execute in arrival sequence. Equities use FIFO to reward posting early liquidity and narrowing spreads. CME Interest Rate Futures use Pro-Rata allocation (proportional to resting depth) because queues are massive (millions of contracts at one tick), preventing a pure microwave-latency race from monopolizing the market."},
        {"type": "h2", "text": "Q3: Maker vs. Taker Economics & The Price Improvement Rule"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> Makers post passive resting orders; Takers cross the spread aggressively. The execution price is <b>always the resting Maker's price</b>, never the Taker's limit price. If Best Ask is $150.00 and an aggressive Buy arrives with limit $150.10, the trade fills at $150.00, granting $0.10 of price improvement to the taker."},
        {"type": "h2", "text": "Q4: Multi-Level Order Sweeps & Residual Resting Orders"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> When incoming quantity exceeds Best Ask depth, the engine sweeps upward across multiple levels. Filled orders and depleted price levels are pruned. If the taker has residual unfilled shares, they rest passively as a new Best Bid on the other side."},
        {"type": "pagebreak"},
        {"type": "h1", "text": "3. Baseline Data Structures & Algorithmic Complexity"},
        {"type": "h2", "text": "Q5: Defend the 3-Layer Baseline Order Book Architecture"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> Layer 1: std::map for price levels (Red-Black tree, O(log P) lookup/insert). Layer 2: std::list at each price level (doubly-linked list, O(1) push_back and pop_front for FIFO). Layer 3: std::unordered_map for OrderId -> {Side, Price} (O(1) hash table for fast cancellation)."},
        {"type": "table", "data": [
            ["Operation", "Baseline Complexity", "Physical Silicon Reality / Tradeoff"],
            ["Add Resting Order", "O(log P) + O(1) list insert", "std::map tree traversal; node malloc introduces heap jitter"],
            ["Match Order", "O(K) where K = fills", "Looping linked list nodes causes pointer chasing cache misses"],
            ["Cancel Order", "O(1) map + O(log P) + O(K)", "Fast price jump via unordered_map, then unlink from list"],
            ["Amend Size (Decrease)", "O(1) queue in-place", "Preserves FIFO queue position; zero allocations"],
            ["Amend Size (Increase)", "O(1) unlink + O(1) push_back", "Must forfeit time priority to prevent quote manipulation; moves to tail"]
        ], "colWidths": [1.8*inch, 2.2*inch, 3.4*inch]},
        {"type": "h1", "text": "4. Modern C++20 Systems Engineering"},
        {"type": "h2", "text": "Q6: Why Fixed-Point Integer Ticks over IEEE-754 Floating-Point?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> Binary floating-point cannot represent decimal fractions like 0.1 cleanly (0.1 + 0.2 = 0.30000000000000004). Equality comparisons silently fail. Using uint64_t ticks (cents) guarantees exact comparisons, avoids FPU overhead, and eliminates regulatory violations."},
        {"type": "h2", "text": "Q7: Strong Typing: enum class Side : uint8_t & std::optional"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> Scoped enum class prevents implicit conversions to int at compile-time. : uint8_t forces 1-byte storage instead of 4-byte default int, saving 3 MB of cache across 1M orders. std::optional eliminates hazardous sentinels like 0 or -1 for empty books."},
        {"type": "h1", "text": "5. Baseline Performance & Tail Latency Defense"},
        {"type": "h2", "text": "Q8: Defend Your Baseline Benchmark Results (p50 vs p99.9 Tail Cliff)"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> On our test bench, baseline throughput was 602,410 orders/sec with p50 of 838.9 ns. However, p99.9 spiked to 83.6 µs and max reached 3.7 ms. This tail cliff is caused by std::list node allocations triggering malloc arena locks and OS page fault kernel syscalls on the hot path."}
    ]
    create_styled_pdf(
        "Week_1_Interview_Preparation_and_Defense.pdf",
        "WEEK 1 MASTER INTERVIEW GUIDE & ARCHITECTURAL DEFENSE",
        "Week 1 Master Interview Guide: Financial Mechanics & Order Book Architecture",
        "The Tier-1 Interview Defense Blueprint (Citadel, Jane Street, Optiver, HRT, Goldman Sachs Core Strats)",
        sections
    )

def build_week2_walkthrough_pdf():
    sections = [
        {"type": "h1", "text": "1. Week 2 Executive Architectural Summary"},
        {"type": "body", "text": "Week 2 transitions from software algorithmic abstractions to Computer Architecture and Mechanical Sympathy. We profile why the CPU core stalls on main memory (DRAM), quantify cache line dynamics on x86-64, inspect physical struct alignment, and measure sub-nanosecond CPU cycles with RDTSC."},
        {"type": "h1", "text": "2. Computer Architecture Foundations: The Memory Wall"},
        {"type": "body", "text": "A 2.50 GHz CPU executes one instruction every 0.40 nanoseconds. Accessing main system memory (DRAM) takes 60 to 100 nanoseconds (~200 wasted clock cycles). If algorithms dereference random heap pointers, the CPU spends 98% of its time stalled."},
        {"type": "table", "data": [
            ["Memory Level", "Capacity", "Latency (ns)", "Clock Cycles", "Hardware Physics"],
            ["CPU Registers", "~1 KB", "0.0 ns", "0 cycles", "Immediate on-core silicon registers"],
            ["L1 Cache", "32 - 48 KB", "~1.0 ns", "2 - 4 cycles", "Core-private SRAM; ultrafast single-cycle access"],
            ["L2 Cache", "512 KB - 1.25 MB", "~3.5 ns", "10 - 14 cycles", "Core-private mid-tier cache"],
            ["L3 Cache", "16 - 36 MB", "~12.0 ns", "35 - 50 cycles", "Shared across cores on the CPU die"],
            ["Main DRAM", "16 - 64 GB", "~80.0 ns", "180 - 220 cycles", "Off-chip capacitor banks across the motherboard bus"]
        ], "colWidths": [1.2*inch, 1.2*inch, 1.1*inch, 1.2*inch, 2.7*inch]},
        {"type": "h1", "text": "3. CacheBenchmark Findings (1,000,000 Elements)"},
        {"type": "body", "text": "In benchmark/CacheBenchmark.cpp, we tested three empirical memory experiments to prove cache line and prefetcher behavior:"},
        {"type": "table", "data": [
            ["Experiment", "Access Pattern", "Measured Result", "Speedup", "Silicon Mechanism"],
            ["1: Vector vs List", "std::vector vs std::list", "0.74 ms vs 11.00 ms", "14.8x FASTER", "Vector: sequential cache reuse. List: pointer chasing across DRAM."],
            ["2: Cold vs Warm", "First vs Second Pass", "0.72 ms vs 0.65 ms", "1.1x FASTER", "Warm cache hits L1/L2 directly; cold pass brings lines from DRAM."],
            ["3: Sequential vs Random", "Sequential vs Shuffled", "0.65 ms vs 6.64 ms", "10.2x FASTER", "Stream prefetcher detects constant stride; random access stalls."]
        ], "colWidths": [1.4*inch, 1.5*inch, 1.3*inch, 1.0*inch, 2.2*inch]},
        {"type": "pagebreak"},
        {"type": "h1", "text": "4. MemoryLayoutTests: Struct Order Dissection"},
        {"type": "body", "text": "In test/MemoryLayoutTests.cpp, we inspected the physical layout of struct Order on 64-bit MSVC. The struct occupies 40 bytes, but holds only 33 bytes of payload, leaving 7 dead padding bytes (17.5% memory waste):"},
        {"type": "code", "text": """Offset Range | Field Name        | Type     | Size     | Alignment Rule
---------------------------------------------------------------------------------
[0x00..0x07] | order_id          | uint64_t | 8 bytes  | Aligned at offset 0 (0 % 8 == 0)
[0x08]       | side              | uint8_t  | 1 byte   | Aligned at offset 8
[0x09..0x0F] | *** DEAD PADDING* | ---      | 7 bytes  | Wasted padding to align price to offset 16
[0x10..0x17] | price             | uint64_t | 8 bytes  | Aligned at offset 16 (16 % 8 == 0)
[0x18..0x1B] | quantity          | uint32_t | 4 bytes  | Aligned at offset 24 (24 % 4 == 0)
[0x1C..0x1F] | initial_quantity  | uint32_t | 4 bytes  | Aligned at offset 28 (28 % 4 == 0)
[0x20..0x27] | timestamp         | uint64_t | 8 bytes  | Aligned at offset 32 (32 % 8 == 0)
Total Size: 40 bytes (33 bytes data + 7 bytes waste). Cache line split: 64/40 = 1.6 orders/line."""},
        {"type": "h1", "text": "5. Cache Line Splitting & The Cost of Hot-Path Malloc"},
        {"type": "body", "text": "Because 64 / 40 = 1.6 orders per cache line, alternate orders straddle the 64-byte boundary, requiring TWO memory bus transactions per order read. Furthermore, allocating nodes via malloc on the hot path induces heap lock contention and OS page faults, directly causing the 83 µs tail spike."},
        {"type": "h1", "text": "6. The Architectural Bridge: Phase 1 Bottlenecks -> Phase 2 Solutions"},
        {"type": "table", "data": [
            ["Component", "Baseline Data Structure", "Hardware Flaw Diagnosed", "Phase 2 Solution"],
            ["Price Levels", "std::map (Red-Black)", "Pointer chasing down tree; 5-10 cache misses", "Direct-indexed flat array: levels[2000], O(1) single index"],
            ["Queues", "std::list (Doubly-Linked)", "14.8x slower traversal; node mallocs scatter in DRAM", "Intrusive doubly-linked list inside pre-allocated slab"],
            ["Allocations", "new Order() per trade", "100k malloc calls; heap locks; latency spikes", "Contiguous Slab Allocator: pre-allocated order slab"],
            ["Order Lookup", "std::unordered_map", "Hash bucket collision chaining; rehashing cliff", "Direct dense address table: order_index[1M]"],
            ["Struct Layout", "40-byte unaligned Order", "7 dead bytes (17.5%); 1.6 orders/cache line", "Pack flags and intrusive list pointers into dead padding"]
        ], "colWidths": [1.1*inch, 1.4*inch, 2.4*inch, 2.5*inch]}
    ]
    create_styled_pdf(
        "Week_2_Code_Walkthrough_and_Deep_Dive.pdf",
        "WEEK 2 CODE WALKTHROUGH & ARCHITECTURE GUIDE",
        "Week 2 Master Architecture Guide: Computer Architecture & Mechanical Sympathy",
        "Empirical Silicon Analysis, Cache Line Dynamics, and Memory Layout Profiling",
        sections
    )

def build_week2_interview_pdf():
    sections = [
        {"type": "h1", "text": "1. Executive Overview & The Systems Interview Mindset"},
        {"type": "body", "text": "In top-tier HFT and low-latency infrastructure interviews (Citadel, Jane Street, Optiver, Jump Trading, HRT), interviewers evaluate your Mechanical Sympathy—your ability to visualize how cache lines, memory buses, and pipelines physically behave under execution."},
        {"type": "h1", "text": "2. CPU Memory Hierarchy & Silicon Physics"},
        {"type": "h2", "text": "Q1: What is the 'Memory Wall'? Why can't CPU memory access keep up with CPU clock speeds?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> The Memory Wall is the widening gap between CPU processing speeds (0.25 to 0.40 ns cycle) and DRAM access latency (60 to 100 ns). In 1980, access latency and cycles were 1:1; today, a DRAM trip costs 200 to 400 CPU cycles. Without effective cache management, the CPU spends 98% of its time stalled."},
        {"type": "h2", "text": "Q2: Compare L1, L2, L3, and DRAM. Why can't all system memory be SRAM?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> L1 takes ~1 ns (2-4 cycles), L2 ~3.5 ns (10-14 cycles), L3 ~12 ns (35-50 cycles), and DRAM ~80 ns (200 cycles). Memory cannot be all SRAM due to: 1) Transistor density (SRAM requires 6 transistors vs DRAM's 1T-1C, making it 6x larger), 2) Signal propagation delay across large physical dies, and 3) Extreme thermal dissipation requirements."},
        {"type": "h2", "text": "Q3: What happens in the CPU execution pipeline during a cache miss?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> On a cache miss, the out-of-order execution engine places the stalled instruction into the Reorder Buffer (ROB) and attempts to execute subsequent independent micro-ops. However, once the ROB saturates (256-512 micro-ops), instruction dispatch stalls completely (pipeline bubble), leaving execution units idle while waiting on DRAM."},
        {"type": "pagebreak"},
        {"type": "h1", "text": "3. Cache Lines, Spatial Locality & Prefetching"},
        {"type": "h2", "text": "Q4: What is a Cache Line? Why is it 64 bytes instead of 8 bytes or 1 KB?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> A cache line is the 64-byte atomic transfer unit between memory and CPU caches. 8 bytes would be inefficient due to bus protocol handshake overhead. 1 KB would cause severe cache pollution and false sharing contention. 64 bytes is the sweet spot balancing bus burst efficiency with spatial locality."},
        {"type": "h2", "text": "Q5: How does the Hardware Stream Prefetcher operate? How do pointer structures defeat it?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> The stream prefetcher monitors memory address access patterns. On constant sequential strides, it loads upcoming lines into L1 before execution requests them. Pointer structures (like std::list) allocate nodes at arbitrary heap addresses; the prefetcher cannot predict non-linear addresses, resulting in continuous DRAM stalls (our benchmark showed a 10.2x penalty)."},
        {"type": "h1", "text": "4. Memory Layout, Alignment & Hot-Path Allocations"},
        {"type": "h2", "text": "Q6: Why are there 7 dead padding bytes in our Order struct? What is Cache Line Splitting?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> On x86-64, an 8-byte uint64_t must align to an address divisible by 8. Because Side (uint8_t) ends at offset 9, the compiler inserts 7 padding bytes before price (offset 16). Furthermore, sizeof(Order) = 40 bytes means 64 / 40 = 1.6 orders per cache line. Alternate orders split across the 64-byte line boundary, requiring two bus transactions to read a single struct."},
        {"type": "h2", "text": "Q7: Why must malloc be banned on the hot path? What causes the 3.7 ms latency outlier?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> malloc involves arena heap lock contention, free-list searches, and kernel page fault syscalls (mmap/brk) when pools deplete. This causes our 83 µs p99.9 spike and 3.7 ms outlier. In Phase 2, we replace malloc with a pre-allocated contiguous Slab Allocator that pops orders in O(1) time with zero syscalls."},
        {"type": "h2", "text": "Q8: What is the purpose of a volatile sink in latency benchmarking?"},
        {"type": "quote", "text": "<b>Verbatim Defense:</b> With /O2 optimization, compilers perform Dead-Code Elimination (DCE). If loop results are never observed, the compiler deletes the entire loop. Writing the output to a global volatile variable legally forbids the compiler from eliminating the loop, ensuring the benchmark measures real execution time."}
    ]
    create_styled_pdf(
        "Week_2_Interview_Preparation_and_Defense.pdf",
        "WEEK 2 MASTER INTERVIEW GUIDE & ARCHITECTURAL DEFENSE",
        "Week 2 Master Interview Guide: Computer Architecture & Mechanical Sympathy",
        "The Tier-1 Systems & Low-Latency C++ Interview Defense Blueprint (Citadel, Optiver, HRT)",
        sections
    )

if __name__ == "__main__":
    build_week1_interview_pdf()
    build_week2_walkthrough_pdf()
    build_week2_interview_pdf()
