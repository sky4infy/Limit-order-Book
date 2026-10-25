import os

def generate_interactive_course():
    html_path = r"d:\Limit Order Book\COURSE_COMPLETE_10_WEEKS_INTERACTIVE.html"
    
    html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Institutional Limit Order Book & HFT Engine: Complete 10-Week Master Curriculum</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Outfit:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #060911;
      --bg-surface: #0c1222;
      --bg-card: #111a30;
      --bg-card-hover: #162240;
      --border-subtle: #1e293b;
      --border-bright: #334155;
      --border-accent: rgba(56, 189, 248, 0.3);
      --accent-cyan: #38bdf8;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-violet: #8b5cf6;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --code-bg: #090e1a;
      --font-display: 'Outfit', -apple-system, sans-serif;
      --font-sans: 'Inter', -apple-system, sans-serif;
      --font-mono: 'Fira Code', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    /* Sidebar Navigation */
    aside {
      width: 320px;
      background: var(--bg-surface);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
    }
    .brand {
      padding: 24px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-icon {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, #0284c7, #38bdf8);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-family: var(--font-display);
      font-weight: 800;
      font-size: 20px;
      color: #fff;
      box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
    }
    .brand-text h1 {
      font-family: var(--font-display);
      font-size: 15px;
      font-weight: 700;
      letter-spacing: -0.3px;
      color: #fff;
    }
    .brand-text p {
      font-size: 11px;
      color: var(--accent-cyan);
      font-weight: 500;
    }

    .nav-list {
      flex: 1;
      overflow-y: auto;
      padding: 16px 12px;
      list-style: none;
    }
    .nav-item {
      padding: 12px 14px;
      border-radius: 8px;
      margin-bottom: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 12px;
      border: 1px solid transparent;
    }
    .nav-item:hover {
      background: var(--bg-card);
      border-color: var(--border-subtle);
    }
    .nav-item.active {
      background: var(--bg-card);
      border-color: var(--border-accent);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    }
    .nav-badge {
      font-family: var(--font-mono);
      font-size: 10px;
      font-weight: 600;
      padding: 3px 6px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.05);
      color: var(--text-muted);
    }
    .nav-item.active .nav-badge {
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent-cyan);
    }
    .nav-label {
      font-size: 12.5px;
      font-weight: 500;
      color: var(--text-muted);
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .nav-item.active .nav-label {
      color: #fff;
      font-weight: 600;
    }

    /* Main Content Area */
    main {
      flex: 1;
      overflow-y: auto;
      padding: 40px 48px;
      background: radial-gradient(circle at top right, rgba(56, 189, 248, 0.04), transparent 40%),
                  radial-gradient(circle at bottom left, rgba(139, 92, 246, 0.04), transparent 40%),
                  var(--bg-base);
    }
    .header-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
      color: var(--accent-cyan);
      margin-bottom: 12px;
    }
    .week-title {
      font-family: var(--font-display);
      font-size: 30px;
      font-weight: 800;
      letter-spacing: -0.5px;
      margin-bottom: 10px;
      background: linear-gradient(135deg, #fff 40%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .week-subtitle {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.6;
      margin-bottom: 32px;
      max-width: 900px;
    }

    /* Grid & Cards */
    .grid-2 {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 20px;
      margin-bottom: 24px;
    }
    .card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 12px;
      padding: 24px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    .card-title {
      font-family: var(--font-display);
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .card-title-icon {
      color: var(--accent-cyan);
    }

    /* Metric Callout Cards */
    .stat-row {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    .stat-card {
      background: linear-gradient(180deg, var(--bg-card) 0%, rgba(17, 26, 48, 0.5) 100%);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 18px;
      position: relative;
      overflow: hidden;
    }
    .stat-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 3px;
      height: 100%;
      background: var(--accent-cyan);
    }
    .stat-val {
      font-family: var(--font-display);
      font-size: 22px;
      font-weight: 800;
      color: #fff;
      margin-bottom: 4px;
    }
    .stat-label {
      font-size: 11px;
      font-weight: 500;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Code Blocks */
    pre {
      background: var(--code-bg);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 16px;
      overflow-x: auto;
      font-family: var(--font-mono);
      font-size: 12px;
      line-height: 1.5;
      color: #e2e8f0;
      margin: 12px 0 20px 0;
    }
    .code-keyword { color: #f43f5e; font-weight: 600; }
    .code-type { color: #38bdf8; }
    .code-func { color: #10b981; }
    .code-comment { color: #64748b; font-style: italic; }

    /* Tables */
    .styled-table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0 24px 0;
      font-size: 12.5px;
    }
    .styled-table th {
      background: rgba(255, 255, 255, 0.03);
      padding: 10px 14px;
      text-align: left;
      color: var(--text-muted);
      font-weight: 600;
      border-bottom: 1px solid var(--border-bright);
    }
    .styled-table td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--border-subtle);
      color: #cbd5e1;
    }
    .styled-table tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }

    /* Interactive Q&A Card */
    .qa-box {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 16px 20px;
      margin-bottom: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .qa-box:hover {
      border-color: var(--border-bright);
    }
    .qa-q {
      font-size: 13.5px;
      font-weight: 600;
      color: #fff;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .qa-a {
      display: none;
      margin-top: 12px;
      padding-top: 12px;
      border-top: 1px solid var(--border-subtle);
      font-size: 12.5px;
      color: var(--text-muted);
      line-height: 1.6;
    }
    .qa-box.open .qa-a {
      display: block;
    }
    .qa-toggle {
      font-size: 18px;
      color: var(--accent-cyan);
      transition: transform 0.2s;
    }
    .qa-box.open .qa-toggle {
      transform: rotate(45deg);
    }

    /* Content views */
    .view-content { display: none; }
    .view-content.active { display: block; }
  </style>
</head>
<body>

  <!-- Sidebar -->
  <aside>
    <div class="brand">
      <div class="brand-icon">L</div>
      <div class="brand-text">
        <h1>Limit Order Book</h1>
        <p>HFT Engine Master Course</p>
      </div>
    </div>
    <ul class="nav-list" id="navList">
      <li class="nav-item active" onclick="switchTab(1)">
        <span class="nav-badge">WK 1</span>
        <span class="nav-label">Baseline Naive Engine</span>
      </li>
      <li class="nav-item" onclick="switchTab(2)">
        <span class="nav-badge">WK 2</span>
        <span class="nav-label">Hardware Architecture</span>
      </li>
      <li class="nav-item" onclick="switchTab(3)">
        <span class="nav-badge">WK 3</span>
        <span class="nav-label">Zero-Allocation Engine</span>
      </li>
      <li class="nav-item" onclick="switchTab(4)">
        <span class="nav-badge">WK 4</span>
        <span class="nav-label">Coordinated Omission</span>
      </li>
      <li class="nav-item" onclick="switchTab(5)">
        <span class="nav-badge">WK 5</span>
        <span class="nav-label">Lock-Free Disruptor</span>
      </li>
      <li class="nav-item" onclick="switchTab(6)">
        <span class="nav-badge">WK 6</span>
        <span class="nav-label">OUCH & ITCH Protocols</span>
      </li>
      <li class="nav-item" onclick="switchTab(7)">
        <span class="nav-badge">WK 7</span>
        <span class="nav-label">Auctions & Pro-Rata</span>
      </li>
      <li class="nav-item" onclick="switchTab(8)">
        <span class="nav-badge">WK 8</span>
        <span class="nav-label">Micro-Price & VPIN</span>
      </li>
      <li class="nav-item" onclick="switchTab(9)">
        <span class="nav-badge">WK 9</span>
        <span class="nav-label">Journaling & Replay</span>
      </li>
      <li class="nav-item" onclick="switchTab(10)">
        <span class="nav-badge">WK 10</span>
        <span class="nav-label">Superday Mastery & Resume</span>
      </li>
    </ul>
  </aside>

  <!-- Main View -->
  <main>
    <!-- WEEK 1 -->
    <div class="view-content active" id="tab1">
      <div class="header-pill">PHASE 1: FOUNDATION</div>
      <h2 class="week-title">Week 1: The Baseline Order Book & Pointer Chasing Trap</h2>
      <p class="week-subtitle">Implementing the standard textbook limit order book using Red-Black trees (std::map) and doubly-linked lists (std::list), measuring baseline performance, and analyzing cache miss bottlenecks.</p>

      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">1.13M</div>
          <div class="stat-label">Throughput (ops/s)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">480 ns</div>
          <div class="stat-label">Median Latency (p50)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">O(log N)</div>
          <div class="stat-label">Price Discovery</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">>= 2 mallocs</div>
          <div class="stat-label">Per Order Added</div>
        </div>
      </div>

      <div class="grid-2">
        <div class="card">
          <div class="card-title"><span class="card-title-icon">⚙️</span> Architectural Bottlenecks</div>
          <p style="font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 12px;">
            The naive implementation allocates order nodes on the heap (`new Order`) and inserts them into `std::list`. Each price level is a node in `std::map<Price, LimitLevel>`.
          </p>
          <ul style="padding-left: 20px; font-size: 12.5px; color: #cbd5e1; line-height: 1.8;">
            <li>Heap allocator contention with OS `malloc()` lock.</li>
            <li>Random memory layout causes high L1/L2 cache miss rates.</li>
            <li>Traversing Red-Black tree pointers stalls the CPU execution pipeline.</li>
          </ul>
        </div>
        <div class="card">
          <div class="card-title"><span class="card-title-icon">💡</span> Superday Defense Insight</div>
          <p style="font-size: 13px; color: var(--text-muted); line-height: 1.6;">
            "Why is std::map unacceptable for HFT?"<br/>
            Because a tree search traverses disparate heap addresses, costing 50–100ns per pointer hop. In contrast, flat memory arrays allow hardware prefetchers to load contiguous lines in 1 clock cycle.
          </p>
        </div>
      </div>
    </div>

    <!-- WEEK 2 -->
    <div class="view-content" id="tab2">
      <div class="header-pill">PHASE 1: PROFILING</div>
      <h2 class="week-title">Week 2: Computer Architecture & Mechanical Sympathy</h2>
      <p class="week-subtitle">Diagnosing 14.2x pointer-chasing penalties, analyzing struct padding, eliminating 64-byte cache line straddling, and optimizing data layout for hardware prefetchers.</p>
      
      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">14.2x</div>
          <div class="stat-label">Pointer Miss Penalty</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">64 Bytes</div>
          <div class="stat-label">L1 Cache Line Size</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">40 Bytes</div>
          <div class="stat-label">Optimal Order Size</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">alignas(64)</div>
          <div class="stat-label">Cache Boundary Guard</div>
        </div>
      </div>

      <div class="card">
        <div class="card-title"><span class="card-title-icon">🔬</span> Cache Hierarchy Benchmark Results</div>
        <table class="styled-table">
          <thead>
            <tr><th>Memory Access Pattern</th><th>Latency per Access</th><th>Throughput</th><th>Hardware Behavior</th></tr>
          </thead>
          <tbody>
            <tr><td>Contiguous Array (Slab)</td><td>3.8 ns</td><td>263M accesses/s</td><td>Hardware stream prefetcher 100% L1 hit</td></tr>
            <tr><td>Pointer-Chasing (Linked List)</td><td>54.2 ns</td><td>18.4M accesses/s</td><td>L1/L2 cache misses, serial dependency stalls</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- WEEK 3 -->
    <div class="view-content" id="tab3">
      <div class="header-pill">PHASE 2: ZERO-ALLOCATION</div>
      <h2 class="week-title">Week 3: Zero-Allocation Matching Engine Core</h2>
      <p class="week-subtitle">Pre-allocated SlabAllocator, 131,072-level DirectPriceLadder, and 2-level 64-bit hierarchical bitmasks for single-cycle O(1) Best Bid/Ask discovery.</p>

      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">9.56M</div>
          <div class="stat-label">Matching ops/s (8.5x)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">47 ns</div>
          <div class="stat-label">Median Latency (p50)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">O(1)</div>
          <div class="stat-label">BBO Bit-Scan (LZCNT)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">0 Bytes</div>
          <div class="stat-label">Heap Allocation / Order</div>
        </div>
      </div>
    </div>

    <!-- WEEK 4 -->
    <div class="view-content" id="tab4">
      <div class="header-pill">PHASE 2: LATENCY PROFILING</div>
      <h2 class="week-title">Week 4: Gil Tene's Coordinated Omission & Tail Profiling</h2>
      <p class="week-subtitle">High Dynamic Range (HDR) latency histogram with backfilling algorithm exposing the 1,450x hidden tail latency spike in closed-loop benchmarks.</p>
      
      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">1.67 ms</div>
          <div class="stat-label">True Phase 1 p99.9 Tail</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">1,450x</div>
          <div class="stat-label">Hidden Tail Factor</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">5.7 µs</div>
          <div class="stat-label">Phase 2 Open-Loop Tail</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">1 Cycle</div>
          <div class="stat-label">HDR Bucket Indexing</div>
        </div>
      </div>
    </div>

    <!-- WEEK 5 -->
    <div class="view-content" id="tab5">
      <div class="header-pill">PHASE 3: CONCURRENCY</div>
      <h2 class="week-title">Week 5: Lock-Free Single-Writer Matching Engine</h2>
      <p class="week-subtitle">LMAX Disruptor-style multi-queue architecture with hardware thread affinity pinning, dedicated SPSC ring buffers, and MESI false sharing eradication.</p>
      
      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">7.75M</div>
          <div class="stat-label">4-Core Throughput</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">87 ns</div>
          <div class="stat-label">Gateway Ingress (p50)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">30 µs</div>
          <div class="stat-label">Ingress p99 (98% Drop)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">alignas(64)</div>
          <div class="stat-label">Cursor Padding</div>
        </div>
      </div>
    </div>

    <!-- WEEK 6 -->
    <div class="view-content" id="tab6">
      <div class="header-pill">PHASE 4: WIRE PROTOCOLS</div>
      <h2 class="week-title">Week 6: Binary Protocols (NASDAQ OUCH 5.0 & ITCH 5.0)</h2>
      <p class="week-subtitle">Zero-copy binary packet deserialization directly over network buffers with single-cycle hardware BSWAP intrinsics, outperforming JSON by 400%.</p>
      
      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">25.4M</div>
          <div class="stat-label">OUCH msgs/s</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">12 ns</div>
          <div class="stat-label">OUCH Parse Latency</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">4.0x</div>
          <div class="stat-label">Throughput vs JSON</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">48-bit</div>
          <div class="stat-label">ITCH Nanosecond TS</div>
        </div>
      </div>
    </div>

    <!-- WEEK 7 -->
    <div class="view-content" id="tab7">
      <div class="header-pill">PHASE 5: EXCHANGE MECHANICS</div>
      <h2 class="week-title">Week 7: Discrete Call Auctions & CME Pro-Rata Matching</h2>
      <p class="week-subtitle">Walrasian equilibrium opening cross with 4-tier tie breaking, CME Pro-Rata allocation with largest fractional remainder, Icebergs, and Self-Trade Prevention.</p>
      
      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">10,000</div>
          <div class="stat-label">Cross in 23.99 ms</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">22 ns</div>
          <div class="stat-label">FIFO Median Latency</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">501 ns</div>
          <div class="stat-label">Pro-Rata Median</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">4 STP</div>
          <div class="stat-label">Wash-Trading Rules</div>
        </div>
      </div>
    </div>

    <!-- WEEK 8 -->
    <div class="view-content" id="tab8">
      <div class="header-pill">PHASE 6: MICROSTRUCTURE</div>
      <h2 class="week-title">Week 8: Sasha Stoikov Micro-Price & VPIN Toxicity</h2>
      <p class="week-subtitle">Stoikov's queue-imbalance Micro-Price estimator, Volume-Synchronized Probability of Toxicity (VPIN), and Avellaneda-Stoikov inventory market maker model.</p>
      
      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">21.3M</div>
          <div class="stat-label">Micro-Price evals/s</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">19 ns</div>
          <div class="stat-label">Micro-Price Latency</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">17.6M</div>
          <div class="stat-label">VPIN evals/s</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">19.6M</div>
          <div class="stat-label">Avellaneda Bot ops/s</div>
        </div>
      </div>
    </div>

    <!-- WEEK 9 -->
    <div class="view-content" id="tab9">
      <div class="header-pill">PHASE 7: HARDENING</div>
      <h2 class="week-title">Week 9: Memory-Mapped Journaling & L3 Visualizer</h2>
      <p class="week-subtitle">Zero-syscall append-only memory-mapped transaction log (MapViewOfFile/mmap) with 100% deterministic crash recovery and Level 3 ASCII market depth dashboard.</p>
      
      <div class="stat-row">
        <div class="stat-card">
          <div class="stat-val">7.64M</div>
          <div class="stat-label">Journal writes/sec</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">335.3 MB/s</div>
          <div class="stat-label">Persistence Bandwidth</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">20 ns</div>
          <div class="stat-label">Journal Write (p50)</div>
        </div>
        <div class="stat-card">
          <div class="stat-val">253 ms</div>
          <div class="stat-label">1M Order Crash Replay</div>
        </div>
      </div>
    </div>

    <!-- WEEK 10 -->
    <div class="view-content" id="tab10">
      <div class="header-pill">PHASE 8: SUPERDAY MASTERY</div>
      <h2 class="week-title">Week 10: Superday Mastery, Resume & Git Progression</h2>
      <p class="week-subtitle">Institutional resume bullet points for Tier-1 quantitative firms, the 5 deadliest interview trap defenses, and the 24-day 2-files-per-day GitHub roadmap.</p>
      
      <div class="card" style="margin-bottom: 24px;">
        <div class="card-title"><span class="card-title-icon">🎯</span> Interactive Superday Interview Defense Flashcards</div>
        
        <div class="qa-box" onclick="this.classList.toggle('open')">
          <div class="qa-q">
            <span>Q1: Why does std::mutex destroy tail latency under multi-core load?</span>
            <span class="qa-toggle">+</span>
          </div>
          <div class="qa-a">
            Under lock contention, the operating system kernel deschedules the losing thread into a sleep state. Waking it back up requires an OS interrupt and context switch costing 5–50µs, blowing p99 tail latency past 1.94 milliseconds. Our lock-free SPSC Single-Writer engine reduced p99 latency by 98% (down to 30µs).
          </div>
        </div>

        <div class="qa-box" onclick="this.classList.toggle('open')">
          <div class="qa-q">
            <span>Q2: What is Coordinated Omission and how was it corrected?</span>
            <span class="qa-toggle">+</span>
          </div>
          <div class="qa-a">
            Closed-loop benchmarks wait for each response before issuing the next request. If the engine pauses for 1ms due to a malloc page fault, the benchmark pauses too, measuring fewer requests during the stall. Gil Tene's backfilling algorithm inserts virtual delayed requests at the expected arrival rate D, revealing the true tail blowout (1,450x spike from 1.15µs to 1.67ms).
          </div>
        </div>

        <div class="qa-box" onclick="this.classList.toggle('open')">
          <div class="qa-q">
            <span>Q3: How does Sasha Stoikov's Micro-Price predict future price moves?</span>
            <span class="qa-toggle">+</span>
          </div>
          <div class="qa-a">
            Standard mid-price assumes symmetric 50/50 tick probability. Stoikov's Micro-Price calculates queue imbalance I = Q_b / (Q_b + Q_a) and weights fair value: MicroPrice = I * P_ask + (1 - I) * P_bid. If the bid queue is 90% of total volume, fair price skews 90% towards the ask.
          </div>
        </div>

        <div class="qa-box" onclick="this.classList.toggle('open')">
          <div class="qa-q">
            <span>Q4: How does memory-mapped journaling guarantee zero state loss?</span>
            <span class="qa-toggle">+</span>
          </div>
          <div class="qa-a">
            MapViewOfFile / mmap maps disk storage directly into process virtual memory. Hot-path appends execute in user-space via pointer arithmetic without syscall context switches. Sequence numbers and a 64-byte header allow replaying 1,000,000 transactions in 253ms with bit-for-bit identical order book state.
          </div>
        </div>
      </div>
    </div>
  </main>

  <script>
    function switchTab(weekNum) {
      document.querySelectorAll('.nav-item').forEach((el, idx) => {
        el.classList.toggle('active', idx === weekNum - 1);
      });
      document.querySelectorAll('.view-content').forEach((el, idx) => {
        el.classList.toggle('active', idx === weekNum - 1);
      });
    }
  </script>
</body>
</html>
"""

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated complete interactive 10-week course at: {html_path} ({os.path.getsize(html_path)} bytes)")

if __name__ == "__main__":
    generate_interactive_course()
