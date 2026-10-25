import os

def create_course_html():
    output_path = r"d:\Limit Order Book\COURSE_WEEK_1_AND_2_INTERACTIVE.html"
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mastering HFT Order Books: Weeks 1 & 2 Complete Self-Paced Course</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #090d16;
      --bg-surface: #0f172a;
      --bg-card: #131d33;
      --bg-card-hover: #18243e;
      --border-subtle: #1e293b;
      --border-bright: #334155;
      --accent-cyan: #06b6d4;
      --accent-cyan-glow: rgba(6, 182, 212, 0.2);
      --accent-emerald: #10b981;
      --accent-emerald-glow: rgba(16, 185, 129, 0.2);
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-indigo: #6366f1;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-dim: #64748b;
      --code-bg: #070a12;
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      --font-mono: 'Fira Code', Consolas, monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-base);
      color: var(--text-main);
      line-height: 1.6;
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
      width: 7px;
      height: 7px;
    }
    ::-webkit-scrollbar-track {
      background: var(--bg-base);
    }
    ::-webkit-scrollbar-thumb {
      background: var(--border-bright);
      border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: var(--accent-cyan);
    }

    /* Layout */
    #sidebar {
      width: 320px;
      min-width: 320px;
      background: var(--bg-surface);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      height: 100%;
      z-index: 20;
    }

    #sidebar-header {
      padding: 20px;
      border-bottom: 1px solid var(--border-subtle);
      background: linear-gradient(180deg, rgba(6, 182, 212, 0.08) 0%, rgba(15, 23, 42, 0) 100%);
    }

    .badge-tag {
      display: inline-block;
      font-size: 10px;
      text-transform: uppercase;
      letter-spacing: 1px;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--accent-cyan-glow);
      color: var(--accent-cyan);
      border: 1px solid rgba(6, 182, 212, 0.4);
      margin-bottom: 8px;
    }

    #sidebar-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.3;
    }

    #progress-container {
      margin-top: 14px;
    }
    .progress-bar-bg {
      background: var(--border-subtle);
      height: 6px;
      border-radius: 3px;
      overflow: hidden;
    }
    .progress-bar-fill {
      background: linear-gradient(90deg, var(--accent-cyan), var(--accent-emerald));
      height: 100%;
      width: 0%;
      transition: width 0.3s ease;
    }
    .progress-text {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    #toc-container {
      flex: 1;
      overflow-y: auto;
      padding: 14px 12px;
    }

    .nav-group-title {
      font-size: 10.5px;
      text-transform: uppercase;
      letter-spacing: 0.8px;
      color: var(--text-dim);
      font-weight: 700;
      padding: 12px 10px 6px 10px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 10px;
      padding: 9px 12px;
      border-radius: 6px;
      font-size: 12.5px;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.15s ease;
      text-decoration: none;
      user-select: none;
    }
    .nav-item:hover {
      background: var(--bg-card);
      color: var(--text-main);
    }
    .nav-item.active {
      background: var(--bg-card);
      color: var(--accent-cyan);
      border-left: 3px solid var(--accent-cyan);
      font-weight: 600;
    }
    .nav-item .icon {
      font-size: 14px;
    }
    .nav-checkbox {
      width: 14px;
      height: 14px;
      border-radius: 3px;
      accent-color: var(--accent-emerald);
      cursor: pointer;
    }

    /* Main Container */
    #main-content {
      flex: 1;
      overflow-y: auto;
      position: relative;
      display: flex;
      flex-direction: column;
    }

    #top-nav {
      position: sticky;
      top: 0;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 12px 36px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      z-index: 10;
    }
    .quick-links {
      display: flex;
      gap: 16px;
    }
    .quick-btn {
      background: var(--bg-card);
      border: 1px solid var(--border-bright);
      color: var(--text-muted);
      font-size: 12px;
      padding: 5px 12px;
      border-radius: 5px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }
    .quick-btn:hover {
      background: var(--bg-card-hover);
      color: var(--text-main);
      border-color: var(--accent-cyan);
    }

    #content-body {
      max-width: 1040px;
      margin: 0 auto;
      padding: 40px 36px 80px 36px;
      width: 100%;
    }

    /* Typography & Content Sections */
    .section-block {
      display: none;
      animation: fadeIn 0.3s ease;
    }
    .section-block.active {
      display: block;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to { opacity: 1; transform: translateY(0); }
    }

    h1.course-h1 {
      font-size: 30px;
      font-weight: 800;
      color: var(--text-main);
      letter-spacing: -0.5px;
      margin-bottom: 10px;
      background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .course-lead {
      font-size: 15px;
      color: var(--text-muted);
      margin-bottom: 28px;
      line-height: 1.6;
    }

    h2.course-h2 {
      font-size: 20px;
      font-weight: 700;
      color: var(--text-main);
      margin: 32px 0 14px 0;
      display: flex;
      align-items: center;
      gap: 10px;
      border-bottom: 1px solid var(--border-subtle);
      padding-bottom: 8px;
    }
    h2.course-h2 span.step-number {
      background: var(--accent-cyan);
      color: #000;
      width: 24px;
      height: 24px;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 12px;
      font-weight: 800;
    }

    h3.course-h3 {
      font-size: 16px;
      font-weight: 600;
      color: var(--accent-cyan);
      margin: 22px 0 8px 0;
    }

    p {
      margin-bottom: 14px;
      color: #cbd5e1;
      font-size: 14px;
      line-height: 1.7;
    }

    /* Callout Card */
    .callout {
      background: var(--bg-card);
      border-left: 4px solid var(--accent-cyan);
      border-radius: 0 8px 8px 0;
      padding: 16px 20px;
      margin: 20px 0;
      box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    .callout.warning {
      border-left-color: var(--accent-amber);
      background: rgba(245, 158, 11, 0.05);
    }
    .callout.danger {
      border-left-color: var(--accent-rose);
      background: rgba(244, 63, 94, 0.05);
    }
    .callout.success {
      border-left-color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.05);
    }
    .callout-title {
      font-weight: 700;
      font-size: 13.5px;
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Code Blocks */
    .code-container {
      background: var(--code-bg);
      border: 1px solid var(--border-bright);
      border-radius: 8px;
      margin: 18px 0;
      overflow: hidden;
      box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
    }
    .code-header {
      background: #0b0f19;
      padding: 8px 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border-subtle);
      font-size: 11.5px;
      color: var(--text-muted);
      font-family: var(--font-mono);
    }
    .code-copy-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      cursor: pointer;
      font-size: 11px;
      transition: color 0.2s;
    }
    .code-copy-btn:hover {
      color: var(--accent-cyan);
    }
    pre.code-block {
      padding: 14px 16px;
      font-family: var(--font-mono);
      font-size: 12.5px;
      line-height: 1.55;
      color: #e2e8f0;
      overflow-x: auto;
    }
    .code-hl {
      color: var(--accent-cyan);
      font-weight: 600;
    }
    .code-comment {
      color: #64748b;
      font-style: italic;
    }
    .code-kw {
      color: #ec4899;
      font-weight: 600;
    }
    .code-num {
      color: #fbbf24;
    }
    .code-str {
      color: #34d399;
    }
    .code-fn {
      color: #60a5fa;
    }

    /* Interactive Simulator Containers */
    .interactive-card {
      background: var(--bg-card);
      border: 1px solid var(--border-bright);
      border-radius: 10px;
      padding: 24px;
      margin: 26px 0;
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .interactive-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 11px;
      font-weight: 700;
      color: #000;
      background: var(--accent-emerald);
      padding: 3px 10px;
      border-radius: 12px;
      margin-bottom: 14px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    /* Ladder Book Simulator Specifics */
    .ladder-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-top: 16px;
    }
    .ladder-col {
      background: #0b0f19;
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px;
    }
    .ladder-col-header {
      font-size: 12px;
      font-weight: 700;
      padding-bottom: 8px;
      border-bottom: 1px solid var(--border-subtle);
      display: flex;
      justify-content: space-between;
    }
    .ladder-row {
      display: flex;
      justify-content: space-between;
      padding: 7px 10px;
      margin: 4px 0;
      border-radius: 4px;
      font-family: var(--font-mono);
      font-size: 12px;
      transition: background 0.2s;
    }
    .ladder-row.ask {
      background: rgba(244, 63, 94, 0.12);
      border-left: 3px solid var(--accent-rose);
      color: #fda4af;
    }
    .ladder-row.bid {
      background: rgba(16, 185, 129, 0.12);
      border-left: 3px solid var(--accent-emerald);
      color: #6ee7b7;
    }
    .spread-indicator {
      grid-column: span 2;
      text-align: center;
      padding: 8px;
      background: rgba(6, 182, 212, 0.1);
      border: 1px dashed var(--accent-cyan);
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 13px;
      color: var(--accent-cyan);
      font-weight: 700;
    }
    .sim-controls {
      display: flex;
      gap: 10px;
      margin-top: 16px;
      flex-wrap: wrap;
    }
    .sim-input {
      background: #090d16;
      border: 1px solid var(--border-bright);
      color: var(--text-main);
      padding: 7px 10px;
      border-radius: 6px;
      font-size: 13px;
      font-family: var(--font-mono);
    }
    .sim-btn {
      background: linear-gradient(135deg, var(--accent-cyan), #0284c7);
      color: #000;
      border: none;
      padding: 7px 16px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
      transition: transform 0.1s, box-shadow 0.2s;
    }
    .sim-btn:hover {
      box-shadow: 0 0 12px var(--accent-cyan-glow);
      transform: translateY(-1px);
    }
    .sim-btn.secondary {
      background: var(--bg-card);
      color: var(--text-main);
      border: 1px solid var(--border-bright);
    }
    .sim-btn.secondary:hover {
      background: var(--bg-card-hover);
      border-color: var(--accent-cyan);
    }
    .log-terminal {
      background: #060910;
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 10px 14px;
      margin-top: 14px;
      font-family: var(--font-mono);
      font-size: 11.5px;
      max-height: 130px;
      overflow-y: auto;
      color: #94a3b8;
    }
    .log-line {
      margin: 3px 0;
    }
    .log-line.trade {
      color: var(--accent-amber);
      font-weight: 600;
    }
    .log-line.system {
      color: var(--accent-cyan);
    }

    /* Memory Layout Inspector Visualizer */
    .memory-grid {
      display: grid;
      grid-template-columns: repeat(8, 1fr);
      gap: 4px;
      margin: 18px 0;
      background: #060910;
      padding: 14px;
      border-radius: 8px;
      border: 1px solid var(--border-bright);
    }
    .mem-byte {
      height: 48px;
      border-radius: 4px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-family: var(--font-mono);
      font-size: 10px;
      cursor: pointer;
      transition: transform 0.15s, box-shadow 0.15s;
      position: relative;
    }
    .mem-byte:hover {
      transform: scale(1.08);
      z-index: 5;
      box-shadow: 0 4px 10px rgba(0,0,0,0.5);
    }
    .mem-byte .offset {
      font-size: 8px;
      opacity: 0.7;
    }
    .mem-byte.id { background: #1e3a8a; color: #93c5fd; }
    .mem-byte.side { background: #065f46; color: #6ee7b7; }
    .mem-byte.pad { 
      background: repeating-linear-gradient(45deg, #7f1d1d, #7f1d1d 5px, #991b1b 5px, #991b1b 10px);
      color: #fca5a5;
      font-weight: 700;
      border: 1px solid #f87171;
    }
    .mem-byte.price { background: #581c87; color: #d8b4fe; }
    .mem-byte.qty { background: #78350f; color: #fde68a; }
    .mem-byte.initqty { background: #854d0e; color: #fef08a; }
    .mem-byte.ts { background: #134e4a; color: #5eead4; }

    .mem-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      font-size: 11px;
      margin-top: 10px;
    }
    .mem-legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .mem-legend-box {
      width: 12px;
      height: 12px;
      border-radius: 3px;
    }

    /* Cache Line Simulator */
    .cache-line-box {
      display: flex;
      border: 2px solid var(--accent-cyan);
      border-radius: 8px;
      overflow: hidden;
      margin: 14px 0;
      background: #060910;
    }
    .cache-chunk {
      flex: 1;
      padding: 10px 4px;
      text-align: center;
      font-family: var(--font-mono);
      font-size: 11px;
      border-right: 1px solid var(--border-subtle);
    }
    .cache-chunk:last-child {
      border-right: none;
    }
    .cache-chunk.active-hit {
      background: rgba(16, 185, 129, 0.25);
      color: var(--accent-emerald);
      font-weight: 700;
    }
    .cache-chunk.active-miss {
      background: rgba(244, 63, 94, 0.25);
      color: var(--accent-rose);
      font-weight: 700;
    }

    /* Quiz Component */
    .quiz-card {
      background: var(--bg-card);
      border: 1px solid var(--border-bright);
      border-radius: 8px;
      padding: 20px;
      margin: 18px 0;
    }
    .quiz-q {
      font-size: 14.5px;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 12px;
    }
    .quiz-options {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .quiz-opt {
      background: #090d16;
      border: 1px solid var(--border-subtle);
      border-radius: 6px;
      padding: 10px 14px;
      font-size: 13px;
      cursor: pointer;
      transition: all 0.15s;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .quiz-opt:hover {
      background: var(--bg-card-hover);
      border-color: var(--border-bright);
    }
    .quiz-opt.selected {
      border-color: var(--accent-cyan);
      background: rgba(6, 182, 212, 0.1);
    }
    .quiz-opt.correct {
      border-color: var(--accent-emerald);
      background: rgba(16, 185, 129, 0.15);
      color: #6ee7b7;
    }
    .quiz-opt.incorrect {
      border-color: var(--accent-rose);
      background: rgba(244, 63, 94, 0.15);
      color: #fda4af;
    }
    .quiz-explain {
      display: none;
      margin-top: 12px;
      padding: 12px;
      border-radius: 6px;
      background: #080c14;
      font-size: 12.5px;
      border-left: 3px solid var(--accent-cyan);
    }

    /* Table Styles */
    table.data-table {
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0;
      font-size: 13px;
      background: #0b0f19;
      border-radius: 8px;
      overflow: hidden;
      border: 1px solid var(--border-subtle);
    }
    table.data-table th {
      background: #111827;
      text-align: left;
      padding: 10px 14px;
      color: var(--accent-cyan);
      font-weight: 700;
      border-bottom: 1px solid var(--border-bright);
    }
    table.data-table td {
      padding: 10px 14px;
      border-bottom: 1px solid var(--border-subtle);
      color: #cbd5e1;
    }
    table.data-table tr:last-child td {
      border-bottom: none;
    }

    /* Tabbed Code Explorer */
    .tab-bar {
      display: flex;
      gap: 4px;
      border-bottom: 1px solid var(--border-subtle);
      background: #070a12;
      padding: 6px 10px 0 10px;
      border-radius: 8px 8px 0 0;
      overflow-x: auto;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-dim);
      padding: 8px 14px;
      font-family: var(--font-mono);
      font-size: 12px;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .tab-btn:hover {
      color: var(--text-main);
    }
    .tab-btn.active {
      color: var(--accent-cyan);
      border-bottom-color: var(--accent-cyan);
      font-weight: 600;
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
    }

    .footer-nav {
      margin-top: 50px;
      display: flex;
      justify-content: space-between;
      border-top: 1px solid var(--border-subtle);
      padding-top: 24px;
    }
  </style>
</head>
<body>

  <!-- LEFT SIDEBAR -->
  <aside id="sidebar">
    <div id="sidebar-header">
      <span class="badge-tag">HFT MASTERCLASS</span>
      <h2 id="sidebar-title">Weeks 1 & 2: Financial Markets & Mechanical Sympathy</h2>
      <div id="progress-container">
        <div class="progress-bar-bg">
          <div class="progress-bar-fill" id="overall-progress"></div>
        </div>
        <div class="progress-text">
          <span>Course Completion</span>
          <span id="progress-percent">0%</span>
        </div>
      </div>
    </div>

    <div id="toc-container">
      <div class="nav-group-title">Module 0: The Starting Line</div>
      <a class="nav-item active" onclick="switchSection('mod0')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod0" onchange="updateProgress(event)">
        <span>0.1 Why HFT & Zero-Knowledge Primer</span>
      </a>

      <div class="nav-group-title">Module 1: Market Mechanics (Week 1)</div>
      <a class="nav-item" onclick="switchSection('mod1-1')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod1-1" onchange="updateProgress(event)">
        <span>1.1 What Is an Exchange & The Ladder</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod1-2')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod1-2" onchange="updateProgress(event)">
        <span>1.2 Price-Time Priority (FIFO Rule)</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod1-3')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod1-3" onchange="updateProgress(event)">
        <span>1.3 Maker vs Taker & Price Improvement</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod1-lab')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod1-lab" onchange="updateProgress(event)">
        <span style="color: var(--accent-emerald);">LAB 1: Interactive Order Book</span>
      </a>

      <div class="nav-group-title">Module 2: Modern C++20 Core Stack</div>
      <a class="nav-item" onclick="switchSection('mod2-1')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod2-1" onchange="updateProgress(event)">
        <span>2.1 Fixed-Point vs Float IEEE-754</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod2-2')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod2-2" onchange="updateProgress(event)">
        <span>2.2 Type Safety: enum class Side : uint8_t</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod2-3')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod2-3" onchange="updateProgress(event)">
        <span>2.3 std::optional & C++20 Features</span>
      </a>

      <div class="nav-group-title">Module 3: Week 1 Code Walkthrough</div>
      <a class="nav-item" onclick="switchSection('mod3-1')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod3-1" onchange="updateProgress(event)">
        <span>3.1 Types.hpp & Order.hpp Decoded</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod3-2')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod3-2" onchange="updateProgress(event)">
        <span>3.2 The 3-Layer Book Architecture</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod3-3')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod3-3" onchange="updateProgress(event)">
        <span>3.3 The 2-Loop Matching Algorithm</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod3-4')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod3-4" onchange="updateProgress(event)">
        <span>3.4 Cancellation & Amendment Rules</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod3-5')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod3-5" onchange="updateProgress(event)">
        <span>3.5 Baseline Latency & Tail Cliff (p99.9)</span>
      </a>

      <div class="nav-group-title">Module 4: Mechanical Sympathy (Week 2)</div>
      <a class="nav-item" onclick="switchSection('mod4-1')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod4-1" onchange="updateProgress(event)">
        <span>4.1 The Memory Wall: CPU vs DRAM</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod4-2')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod4-2" onchange="updateProgress(event)">
        <span>4.2 Cache Lines (64 Bytes) & Prefetching</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod4-3')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod4-3" onchange="updateProgress(event)">
        <span>4.3 14.8x Benchmark: Vector vs List</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod4-lab')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod4-lab" onchange="updateProgress(event)">
        <span style="color: var(--accent-emerald);">LAB 2: Cache Miss & Prefetch Sim</span>
      </a>

      <div class="nav-group-title">Module 5: Memory Layout & Alignment</div>
      <a class="nav-item" onclick="switchSection('mod5-1')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod5-1" onchange="updateProgress(event)">
        <span>5.1 The 7 Dead Padding Bytes in Order</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod5-2')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod5-2" onchange="updateProgress(event)">
        <span>5.2 Cache Line Splitting (1.6 Orders/Line)</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod5-3')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod5-3" onchange="updateProgress(event)">
        <span>5.3 Hot-Path Malloc & Volatile Sinks</span>
      </a>
      <a class="nav-item" onclick="switchSection('mod5-lab')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod5-lab" onchange="updateProgress(event)">
        <span style="color: var(--accent-emerald);">LAB 3: Struct Memory Layout Tool</span>
      </a>

      <div class="nav-group-title">Module 6: Connecting Week 1 to Week 2</div>
      <a class="nav-item" onclick="switchSection('mod6-1')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod6-1" onchange="updateProgress(event)">
        <span>6.1 Bottleneck Diagnosis to Phase 2 Fixes</span>
      </a>

      <div class="nav-group-title">Module 7: Interactive Master Quiz</div>
      <a class="nav-item" onclick="switchSection('mod7-quiz')">
        <input type="checkbox" class="nav-checkbox" id="chk-mod7-quiz" onchange="updateProgress(event)">
        <span style="color: var(--accent-cyan);">7.1 Mastery Certification Exam</span>
      </a>
    </div>
  </aside>

  <!-- MAIN VIEWPORT -->
  <main id="main-content">
    <header id="top-nav">
      <div style="font-size: 13px; color: var(--text-muted); font-family: var(--font-mono);">
        PROJECT: <span style="color: var(--accent-cyan);">Institutional Limit Order Book HFT Engine</span>
      </div>
      <div class="quick-links">
        <button class="quick-btn" onclick="switchSection('mod1-lab')"><span>⚡</span> Order Book Lab</button>
        <button class="quick-btn" onclick="switchSection('mod5-lab')"><span>🧩</span> Struct Padding Lab</button>
        <button class="quick-btn" onclick="switchSection('mod7-quiz')"><span>🎓</span> Knowledge Exam</button>
      </div>
    </header>

    <div id="content-body">

      <!-- MODULE 0: PRIMER -->
      <section id="mod0" class="section-block active">
        <h1 class="course-h1">Welcome to HFT: From Absolute Zero to Core Systems</h1>
        <p class="course-lead">
          You don't need a Wall Street background or 10 years of C++ to master this. We build every intuition from physical principles: how humans trade, how computer chips move electrons, and why nanoseconds decide billions of dollars.
        </p>

        <div class="callout">
          <div class="callout-title" style="color: var(--accent-cyan);">🎯 The Golden Philosophy of High-Frequency Trading</div>
          <p>
            In normal software, an algorithm with $O(1)$ complexity is considered optimal. In High-Frequency Trading (HFT), an $O(1)$ algorithm that accesses random RAM locations will be <b>15 times slower</b> than an $O(N)$ algorithm streaming contiguous memory. 
            <b>Hardware physics trumps theoretical complexity.</b>
          </p>
        </div>

        <h2 class="course-h2"><span class="step-number">1</span> What Exactly Is an Exchange?</h2>
        <p>
          Think of a farmers' market. Alice arrives with 10 apples. She says: <i>"I will sell these apples, but only if you pay me at least $1.05 each."</i> Bob arrives wanting apples. He says: <i>"I want 10 apples, but I only want to pay $1.00 each."</i>
        </p>
        <p>
          Do they trade? <b>No.</b> There is a 5-cent disagreement between Alice's minimum selling price ($1.05) and Bob's maximum buying price ($1.00). 
        </p>
        <p>
          That gap is called the <b>SPREAD</b>. Both orders sit in a notebook, waiting. That notebook is the <b>Limit Order Book (LOB)</b>.
        </p>
        <p>
          Now Charlie walks into the market in a hurry. He says: <i>"I need 10 apples right now. I don't care about getting the cheapest bargain, I'll pay $1.05!"</i> 
          Charlie's order matches with Alice's resting order. A <b>trade occurs</b>. Alice gets $10.50, Charlie gets 10 apples.
        </p>

        <h2 class="course-h2"><span class="step-number">2</span> Why C++20? Why Not Python or Java?</h2>
        <p>
          Modern CPUs execute instructions every <b>0.4 nanoseconds</b> (at 2.50 GHz).
        </p>
        <table class="data-table">
          <thead>
            <tr>
              <th>Language / Runtime</th>
              <th>Average Order Latency</th>
              <th>The Fatal HFT Flaw</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Python</b></td>
              <td>50,000 to 200,000 ns</td>
              <td>Interpreted bytecode, Global Interpreter Lock (GIL), dynamic typing overhead.</td>
            </tr>
            <tr>
              <td><b>Java / C#</b></td>
              <td>5,000 to 50,000 ns</td>
              <td><b>Garbage Collection (GC) pauses:</b> The runtime randomly stops execution for milliseconds to clean memory. An HFT firm with a 1 ms pause misses thousands of trades.</td>
            </tr>
            <tr>
              <td><b>Modern C++20</b></td>
              <td><b>10 to 800 ns</b></td>
              <td>Direct compilation to CPU machine code, deterministic memory deallocation, zero-cost abstractions, absolute control over CPU cache lines.</td>
            </tr>
          </tbody>
        </table>

        <div class="footer-nav">
          <div></div>
          <button class="sim-btn" onclick="switchSection('mod1-1')">Next: 1.1 What Is an Exchange & The Ladder →</button>
        </div>
      </section>

      <!-- MODULE 1.1 -->
      <section id="mod1-1" class="section-block">
        <h1 class="course-h1">1.1 The Order Book Ladder</h1>
        <p class="course-lead">
          Understanding the visual structure of market depth and bid-ask spreads.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> Bids vs. Asks</h2>
        <p>
          An order book is split cleanly down the middle into two opposing armies:
        </p>
        <ul>
          <li style="margin-left: 20px; margin-bottom: 8px;">
            <b style="color: var(--accent-emerald);">BIDS (Buyers):</b> Participants who want to buy. They want to pay as <i>little</i> as possible. The highest buyer is the <b>Best Bid</b> because they offer the most generous price to sellers.
          </li>
          <li style="margin-left: 20px; margin-bottom: 8px;">
            <b style="color: var(--accent-rose);">ASKS (Sellers):</b> Participants who want to sell. They want to receive as <i>much</i> as possible. The lowest seller is the <b>Best Ask</b> because they offer the cheapest bargain to buyers.
          </li>
        </ul>

        <div class="code-container">
          <div class="code-header">
            <span>Visual Concept: The Order Book Ladder</span>
          </div>
          <pre class="code-block">
        ASKS (Sellers - Sorted Ascending by Price)
────────────────────────────────────────────────────────
  $150.15   |  5,000 shares       (Deep Ask - expensive)
  $150.10   |  2,500 shares
  $150.05   |    800 shares       <span class="code-hl">&lt;-- BEST ASK (Cheapest Seller)</span>
────────────────────────────────────────────────────────
  &gt;&gt;&gt; SPREAD: $0.05 ($150.05 - $150.00) &lt;&lt;&lt;
────────────────────────────────────────────────────────
  $150.00   |    500 shares       <span class="code-hl">&lt;-- BEST BID (Highest Buyer)</span>
  $149.95   |  1,200 shares
  $149.90   |  3,000 shares       (Deep Bid - conservative)
────────────────────────────────────────────────────────
        BIDS (Buyers - Sorted Descending by Price)
          </pre>
        </div>

        <p>
          Notice how the ladder is sorted:
        </p>
        <p>
          <b>Bids</b> are sorted <b>descending</b> ($150.00 &gt; $149.95 &gt; $149.90). In our code, we implement this using:
          <br><code>std::map&lt;Price, std::list&lt;Order&gt;, std::greater&lt;Price&gt;&gt; bids_;</code>
        </p>
        <p>
          <b>Asks</b> are sorted <b>ascending</b> ($150.05 &lt; $150.10 &lt; $150.15). In our code, we implement this using:
          <br><code>std::map&lt;Price, std::list&lt;Order&gt;, std::less&lt;Price&gt;&gt; asks_;</code>
        </p>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod0')">← Previous: Primer</button>
          <button class="sim-btn" onclick="switchSection('mod1-2')">Next: 1.2 Price-Time Priority (FIFO) →</button>
        </div>
      </section>

      <!-- MODULE 1.2 -->
      <section id="mod1-2" class="section-block">
        <h1 class="course-h1">1.2 Price-Time Priority (FIFO Rule)</h1>
        <p class="course-lead">
          Why arrival time governs execution when multiple traders quote the exact same price.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> The Two Invariant Rules of Matching</h2>
        <p>
          To keep an exchange strictly fair, orders must follow a two-tier hierarchy:
        </p>
        <ol style="margin-left: 24px; margin-bottom: 16px;">
          <li style="margin-bottom: 8px;">
            <b>Price Priority:</b> The most generous order always executes first. A buyer offering $150.05 <i>always</i> beats a buyer offering $150.00, regardless of who arrived first.
          </li>
          <li>
            <b>Time Priority (FIFO):</b> If Trader A and Trader B both place a buy order at $150.00, <b>whoever arrived at the exchange first gets filled first</b>.
          </li>
        </ol>

        <div class="code-container">
          <div class="code-header">
            <span>Our Project's FIFO Test Verification (test/BaselineTests.cpp)</span>
          </div>
          <pre class="code-block">
<span class="code-comment">// Order 10 arrives at 09:00:00.000 for 100 shares @ $50.00</span>
book.add_order(Order(10, Side::BUY, 5000, 100));

<span class="code-comment">// Order 11 arrives at 09:00:00.001 for 100 shares @ $50.00 (same price!)</span>
book.add_order(Order(11, Side::BUY, 5000, 100));

<span class="code-comment">// Incoming aggressive sell for 150 shares arrives</span>
<span class="code-kw">auto</span> trades = book.add_order(Order(12, Side::SELL, 5000, 150));

<span class="code-comment">// FIFO VERIFICATION:</span>
<span class="code-comment">// Order 10 MUST fill first (100 shares full fill)</span>
<span class="code-fn">assert</span>(trades[0].maker_order_id == 10 &amp;&amp; trades[0].quantity == 100);

<span class="code-comment">// Order 11 gets the remaining 50 shares (partial fill)</span>
<span class="code-fn">assert</span>(trades[1].maker_order_id == 11 &amp;&amp; trades[1].quantity == 50);
          </pre>
        </div>

        <div class="callout success">
          <div class="callout-title">💡 How this is physically implemented in our engine</div>
          <p>
            At each price level, we use a <code>std::list&lt;Order&gt;</code>. New orders are appended to the <b>back</b> (<code>queue.push_back(order)</code>). 
            When matching, we always inspect and consume from the <b>front</b> (<code>Order&amp; resting = queue.front()</code>). 
            This guarantees perfect $O(1)$ FIFO enforcement!
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod1-1')">← Previous: The Ladder</button>
          <button class="sim-btn" onclick="switchSection('mod1-3')">Next: 1.3 Maker vs Taker →</button>
        </div>
      </section>

      <!-- MODULE 1.3 -->
      <section id="mod1-3" class="section-block">
        <h1 class="course-h1">1.3 Maker vs Taker & Price Improvement</h1>
        <p class="course-lead">
          The fundamental asymmetry between resting passive orders and incoming aggressive orders.
        </p>

        <table class="data-table">
          <thead>
            <tr>
              <th>Role</th>
              <th>Behavior</th>
              <th>Market Impact</th>
              <th>Fee Structure</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b style="color: var(--accent-cyan);">Maker (Passive)</b></td>
              <td>Places an order inside or behind the spread. The order <b>rests</b> in the book.</td>
              <td><b>Adds liquidity</b> (provides quotes for others to trade against).</td>
              <td>Usually receives a <b>rebate</b> (the exchange pays them to trade).</td>
            </tr>
            <tr>
              <td><b style="color: var(--accent-amber);">Taker (Aggressive)</b></td>
              <td>Places an order that crosses the spread, immediately matching resting orders.</td>
              <td><b>Removes liquidity</b> (consumes available shares from the book).</td>
              <td>Pays a <b>fee</b> to the exchange.</td>
            </tr>
          </tbody>
        </table>

        <h2 class="course-h2"><span class="step-number">2</span> The Rule of Execution Price: Price Improvement</h2>
        <div class="callout warning">
          <div class="callout-title">🚨 Crucial HFT Invariant</div>
          <p>
            <b>The execution price is ALWAYS the Maker's resting price, NOT the Taker's limit price.</b>
          </p>
          <p>
            <i>Scenario:</i> Seller Alice is resting in the book at <b>$100.05</b>. 
            Buyer Bob submits an aggressive buy order with a limit of <b>$100.10</b> (he is willing to pay up to $100.10).
            <br><br>
            At what price does the trade execute? 
            <br>
            <b>It executes at $100.05!</b> Bob gets $0.05 of <b>price improvement</b>. He was willing to pay $100.10, but because Alice was offering $100.05, the engine fills him at Alice's price.
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod1-2')">← Previous: FIFO</button>
          <button class="sim-btn" onclick="switchSection('mod1-lab')">Next: LAB 1 - Order Book Simulator →</button>
        </div>
      </section>

      <!-- MODULE 1.LAB: INTERACTIVE SIMULATOR -->
      <section id="mod1-lab" class="section-block">
        <h1 class="course-h1">LAB 1: Interactive Live Order Book Simulator</h1>
        <p class="course-lead">
          Test market mechanics in real time. Submit orders, trigger multi-level sweeps, watch trades match, and observe FIFO priority live.
        </p>

        <div class="interactive-card">
          <span class="interactive-badge">⚡ Real-Time Engine Active</span>
          <h3 style="color: var(--text-main); margin-bottom: 6px;">Submit an Order to the Engine</h3>
          <p style="font-size: 13px; color: var(--text-muted);">
            Choose Side, Price (in Dollars), and Quantity. If your order crosses the spread, trades will execute immediately!
          </p>

          <div class="sim-controls">
            <select id="sim-side" class="sim-input" style="font-weight: 700;">
              <option value="BUY" style="color: var(--accent-emerald);">BUY (Bid)</option>
              <option value="SELL" style="color: var(--accent-rose);">SELL (Ask)</option>
            </select>
            <input type="number" id="sim-price" class="sim-input" placeholder="Price ($)" value="150.05" step="0.05" style="width: 110px;">
            <input type="number" id="sim-qty" class="sim-input" placeholder="Qty" value="500" step="50" style="width: 90px;">
            <button class="sim-btn" onclick="submitSimOrder()">Submit Order</button>
            <button class="sim-btn secondary" onclick="resetSimBook()">Reset to Default Ladder</button>
            <button class="sim-btn secondary" onclick="runSweepDemo()">Demo: Multi-Level Sweep</button>
          </div>

          <!-- LADDER DISPLAY -->
          <div class="ladder-grid">
            <div class="ladder-col">
              <div class="ladder-col-header" style="color: var(--accent-rose);">
                <span>ASKS (Sellers)</span>
                <span>Quantity</span>
              </div>
              <div id="sim-asks-list"></div>
            </div>

            <div class="ladder-col">
              <div class="ladder-col-header" style="color: var(--accent-emerald);">
                <span>BIDS (Buyers)</span>
                <span>Quantity</span>
              </div>
              <div id="sim-bids-list"></div>
            </div>

            <div class="spread-indicator" id="sim-spread">
              SPREAD: $0.05 (Best Bid: $150.00 | Best Ask: $150.05)
            </div>
          </div>

          <!-- EXECUTION LOG -->
          <h4 style="font-size: 12px; color: var(--text-muted); margin-top: 14px; text-transform: uppercase;">
            Matching Engine Event Log
          </h4>
          <div class="log-terminal" id="sim-log">
            <div class="log-line system">[SYSTEM] Engine initialized with default 3-level book. Ready for orders.</div>
          </div>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod1-3')">← Previous: Maker vs Taker</button>
          <button class="sim-btn" onclick="switchSection('mod2-1')">Next: Module 2 - C++20 Tech Stack →</button>
        </div>
      </section>

      <!-- MODULE 2.1 -->
      <section id="mod2-1" class="section-block">
        <h1 class="course-h1">2.1 The Floating-Point Hazard: Integer Fixed-Point</h1>
        <p class="course-lead">
          Why using `double` or `float` for prices is fatal in financial engineering, and how integer ticks save the day.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> The 0.1 + 0.2 Disaster</h2>
        <p>
          Open your terminal right now and compute <code>0.1 + 0.2</code> in standard C++ or Python:
        </p>
        <div class="code-container">
          <pre class="code-block">
<span class="code-kw">double</span> a = 0.1;
<span class="code-kw">double</span> b = 0.2;
std::cout &lt;&lt; std::setprecision(20) &lt;&lt; (a + b) &lt;&lt; std::endl;
<span class="code-comment">// Output: 0.30000000000000004441</span>
          </pre>
        </div>

        <div class="callout danger">
          <div class="callout-title">💥 Why does this happen?</div>
          <p>
            Computer hardware speaks binary (powers of 2: 1/2, 1/4, 1/8, 1/16, etc.). Just like $1/3$ cannot be represented as a finite decimal in base-10 ($0.33333...$), the fraction $1/10$ ($0.1$) cannot be represented as a finite fraction in base-2. 
            It becomes an infinite repeating binary sequence: <code>0.0001100110011...</code>
          </p>
          <p>
            If you check <code>if (order.price == best_bid)</code> using <code>double</code>, the check will <b>silently fail</b> due to binary rounding noise. In real exchanges, this results in crossed books, missed fills, and SEC regulatory fines.
          </p>
        </div>

        <h2 class="course-h2"><span class="step-number">2</span> The HFT Solution: Integer Fixed-Point Ticks</h2>
        <p>
          In <code>src/common/Types.hpp</code>, we define price as a 64-bit integer:
        </p>
        <div class="code-container">
          <div class="code-header">
            <span>src/common/Types.hpp Line 18</span>
          </div>
          <pre class="code-block">
<span class="code-kw">using</span> Price = <span class="code-kw">uint64_t</span>; <span class="code-comment">// Integer ticks (e.g. 1 cent = 1 tick)</span>
          </pre>
        </div>
        <p>
          A price of <b>$150.25</b> is stored as the integer <code>15025</code>.
          <br>
          Comparisons like <code>15025 == 15025</code> or <code>15025 &gt;= 15020</code> are <b>100% exact</b>. There is zero rounding noise, zero floating-point unit (FPU) cycle cost, and integer arithmetic executes in a single clock cycle.
        </p>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod1-lab')">← Previous: Lab 1</button>
          <button class="sim-btn" onclick="switchSection('mod2-2')">Next: 2.2 enum class Side : uint8_t →</button>
        </div>
      </section>

      <!-- MODULE 2.2 -->
      <section id="mod2-2" class="section-block">
        <h1 class="course-h1">2.2 Type Safety: `enum class Side : uint8_t`</h1>
        <p class="course-lead">
          How two small keywords prevent catastrophic bugs and save megabytes of CPU cache.
        </p>

        <div class="code-container">
          <div class="code-header">
            <span>src/common/Types.hpp Lines 9-12</span>
          </div>
          <pre class="code-block">
<span class="code-kw">enum class</span> <span class="code-hl">Side</span> : <span class="code-kw">uint8_t</span> {
    BUY  = <span class="code-num">0</span>,
    SELL = <span class="code-num">1</span>
};
          </pre>
        </div>

        <h2 class="course-h2"><span class="step-number">1</span> Why `enum class` (Scoped Enum)?</h2>
        <p>
          In old C / traditional C++, a raw <code>enum</code> leaks its names into the global scope and implicitly converts to an integer:
        </p>
        <div class="code-container">
          <pre class="code-block">
<span class="code-comment">// Old C enum: DANGEROUS!</span>
<span class="code-kw">enum</span> Side { BUY, SELL };
<span class="code-kw">if</span> (BUY == 0) { ... }          <span class="code-comment">// Compiles! Implicitly converts to int.</span>
Price p = BUY + 100;           <span class="code-comment">// Compiles! Adding Side to a Price makes no physical sense!</span>
          </pre>
        </div>
        <p>
          With <code>enum class</code>, the compiler strictly enforces type safety:
        </p>
        <div class="code-container">
          <pre class="code-block">
<span class="code-comment">// Modern C++20 Scoped Enum: SAFE!</span>
<span class="code-kw">if</span> (side == 0) { ... }         <span class="code-comment">// COMPILE ERROR: Cannot compare Side to int</span>
Price p = Side::BUY + 100;     <span class="code-comment">// COMPILE ERROR: Invalid operands</span>
          </pre>
        </div>

        <h2 class="course-h2"><span class="step-number">2</span> Why `: uint8_t`?</h2>
        <p>
          By default in C++, any enum is given <b>4 bytes</b> of storage (the size of an <code>int</code>).
        </p>
        <p>
          By writing <code>: uint8_t</code>, we force the compiler to store it in just <b>1 byte</b>. 
          When managing an order book holding 1,000,000 orders:
          <br>
          $$1,000,000 \text{ orders} \times 3 \text{ bytes saved} = 3 \text{ Megabytes of memory saved!}$$
          In HFT, 3 MB is larger than an entire CPU L2 cache!
        </p>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod2-1')">← Previous: Fixed-Point</button>
          <button class="sim-btn" onclick="switchSection('mod2-3')">Next: 2.3 std::optional & C++20 →</button>
        </div>
      </section>

      <!-- MODULE 2.3 -->
      <section id="mod2-3" class="section-block">
        <h1 class="course-h1">2.3 Clean Absence with `std::optional`</h1>
        <p class="course-lead">
          Eliminating magic sentinels (-1, 0, UINT64_MAX) to make impossible states unrepresentable.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> The Problem with Sentinel Values</h2>
        <p>
          What should <code>get_best_bid()</code> return if the book has no buyers?
        </p>
        <p>
          In junior code, developers return <code>0</code> or <code>-1</code>:
        </p>
        <div class="code-container">
          <pre class="code-block">
<span class="code-comment">// Dangerous Sentinel Pattern</span>
Price best = book.get_best_bid();
<span class="code-kw">if</span> (best == 0) { ... } <span class="code-comment">// What if an oil contract or bankrupt penny stock trades at $0.00?</span>
          </pre>
        </div>

        <h2 class="course-h2"><span class="step-number">2</span> The Modern C++20 Pattern</h2>
        <div class="code-container">
          <div class="code-header">
            <span>src/baseline/OrderBookBaseline.cpp Lines 239-244</span>
          </div>
          <pre class="code-block">
std::optional&lt;Price&gt; OrderBookBaseline::get_best_bid() <span class="code-kw">const</span> {
    <span class="code-kw">if</span> (bids_.empty()) {
        <span class="code-kw">return</span> std::nullopt; <span class="code-comment">// Explicitly: No price exists!</span>
    }
    <span class="code-kw">return</span> bids_.begin()-&gt;first;
}
          </pre>
        </div>
        <p>
          The caller cannot accidentally treat absence as a valid number. The type forces explicit handling:
        </p>
        <div class="code-container">
          <pre class="code-block">
<span class="code-kw">auto</span> best = book.get_best_bid();
<span class="code-kw">if</span> (!best.has_value()) {
    <span class="code-comment">// Book is empty — clean and crash-proof</span>
}
          </pre>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod2-2')">← Previous: Type Safety</button>
          <button class="sim-btn" onclick="switchSection('mod3-1')">Next: Module 3 - Week 1 Code Walkthrough →</button>
        </div>
      </section>

      <!-- MODULE 3.1 -->
      <section id="mod3-1" class="section-block">
        <h1 class="course-h1">3.1 Code Walkthrough: Types.hpp & Order.hpp</h1>
        <p class="course-lead">
          Line-by-line breakdown of our project's fundamental data contracts.
        </p>

        <div class="tab-bar">
          <button class="tab-btn active" onclick="switchTab(event, 'tab-types')">src/common/Types.hpp</button>
          <button class="tab-btn" onclick="switchTab(event, 'tab-order')">src/common/Order.hpp</button>
        </div>

        <div id="tab-types" class="tab-content active code-container">
          <pre class="code-block">
<span class="code-comment">// src/common/Types.hpp</span>
#pragma once
#include &lt;cstdint&gt;

<span class="code-comment">// 1-byte scoped enum for trading side</span>
<span class="code-kw">enum class</span> <span class="code-hl">Side</span> : <span class="code-kw">uint8_t</span> {
    BUY = 0,
    SELL = 1
};

<span class="code-comment">// Zero-cost type aliases: clear intent, zero runtime overhead</span>
<span class="code-kw">using</span> <span class="code-hl">Price</span>     = <span class="code-kw">uint64_t</span>; <span class="code-comment">// Stored as fixed integer cents (e.g. 15025 = $150.25)</span>
<span class="code-kw">using</span> <span class="code-hl">Quantity</span>  = <span class="code-kw">uint32_t</span>; <span class="code-comment">// Share count (up to 4.29 billion per order)</span>
<span class="code-kw">using</span> <span class="code-hl">OrderId</span>   = <span class="code-kw">uint64_t</span>; <span class="code-comment">// Monotonically increasing unique ID</span>
<span class="code-kw">using</span> <span class="code-hl">Timestamp</span> = <span class="code-kw">uint64_t</span>; <span class="code-comment">// CPU clock cycles or nanoseconds</span>
          </pre>
        </div>

        <div id="tab-order" class="tab-content code-container">
          <pre class="code-block">
<span class="code-comment">// src/common/Order.hpp</span>
#pragma once
#include "Types.hpp"
#include &lt;iostream&gt;

<span class="code-kw">struct</span> <span class="code-hl">Order</span> {
    OrderId   order_id;         <span class="code-comment">// 8 bytes: Unique ID</span>
    Side      side;             <span class="code-comment">// 1 byte: BUY or SELL</span>
    <span class="code-comment">// [7 bytes of compiler padding inserted here!]</span>
    Price     price;            <span class="code-comment">// 8 bytes: Limit price</span>
    Quantity  quantity;         <span class="code-comment">// 4 bytes: Remaining unfilled shares</span>
    Quantity  initial_quantity; <span class="code-comment">// 4 bytes: Original submitted size</span>
    Timestamp timestamp;        <span class="code-comment">// 8 bytes: Arrival time</span>

    <span class="code-fn">Order</span>(OrderId id, Side s, Price p, Quantity qty, Timestamp ts = 0)
        : order_id(id), side(s), price(p), quantity(qty),
          initial_quantity(qty), timestamp(ts) {}

    <span class="code-kw">bool</span> <span class="code-fn">is_filled</span>() <span class="code-kw">const</span> { <span class="code-kw">return</span> quantity == 0; }
};
          </pre>
        </div>

        <div class="callout">
          <div class="callout-title">🔍 Why store `initial_quantity`?</div>
          <p>
            When an order partially matches (e.g., 50 shares filled out of 100), <code>quantity</code> decreases to 50. 
            We keep <code>initial_quantity = 100</code> so we can compute total execution progress, audit trades, and enforce exchange rules when an order is amended.
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod2-3')">← Previous: std::optional</button>
          <button class="sim-btn" onclick="switchSection('mod3-2')">Next: 3.2 The 3-Layer Book Architecture →</button>
        </div>
      </section>

      <!-- MODULE 3.2 -->
      <section id="mod3-2" class="section-block">
        <h1 class="course-h1">3.2 The 3-Layer Book Architecture</h1>
        <p class="course-lead">
          How our Phase 1 baseline organizes bids, asks, and order lookups.
        </p>

        <div class="code-container">
          <div class="code-header">
            <span>src/baseline/OrderBookBaseline.hpp Lines 44-46</span>
          </div>
          <pre class="code-block">
<span class="code-kw">std::map</span>&lt;Price, <span class="code-kw">std::list</span>&lt;Order&gt;, <span class="code-kw">std::greater</span>&lt;Price&gt;&gt; bids_;   <span class="code-comment">// Sorted Descending</span>
<span class="code-kw">std::map</span>&lt;Price, <span class="code-kw">std::list</span>&lt;Order&gt;, <span class="code-kw">std::less</span>&lt;Price&gt;&gt;    asks_;   <span class="code-comment">// Sorted Ascending</span>
<span class="code-kw">std::unordered_map</span>&lt;OrderId, std::pair&lt;Side, Price&gt;&gt; order_index_; <span class="code-comment">// Fast Lookup</span>
          </pre>
        </div>

        <h2 class="course-h2"><span class="step-number">1</span> Layer 1: Sorted Price Levels (std::map)</h2>
        <p>
          <code>std::map</code> is a self-balancing Red-Black binary search tree.
        </p>
        <p>
          Because bids use <code>std::greater&lt;Price&gt;</code>, the root and leftmost nodes hold the highest bids. <code>bids_.begin()</code> returns the <b>Best Bid</b> in $O(1)$ amortized time.
        </p>

        <h2 class="course-h2"><span class="step-number">2</span> Layer 2: FIFO Queues (std::list)</h2>
        <p>
          At each price level, orders are stored in a doubly-linked list.
          <br>
          Enqueuing at tail: <code>queue.push_back(order)</code> ($O(1)$).
          <br>
          Dequeuing from head: <code>queue.pop_front()</code> ($O(1)$).
        </p>

        <h2 class="course-h2"><span class="step-number">3</span> Layer 3: O(1) Fast Lookup Index (std::unordered_map)</h2>
        <p>
          When a client wants to cancel order #9821, how do we find it?
          <br>
          Without an index, we would have to scan every price level and every queue: $O(\text{Levels} \times \text{Orders})$ — disastrously slow!
          <br>
          With <code>order_index_</code>, we look up <code>order_id</code> in $O(1)$ time to get its <code>{Side, Price}</code>, allowing us to jump straight to the exact price level node in the tree.
        </p>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod3-1')">← Previous: Types & Order</button>
          <button class="sim-btn" onclick="switchSection('mod3-3')">Next: 3.3 The 2-Loop Matching Algorithm →</button>
        </div>
      </section>

      <!-- MODULE 3.3 -->
      <section id="mod3-3" class="section-block">
        <h1 class="course-h1">3.3 The 2-Loop Matching Algorithm</h1>
        <p class="course-lead">
          Dissecting the engine's core matching loop line by line.
        </p>

        <div class="code-container">
          <div class="code-header">
            <span>src/baseline/OrderBookBaseline.cpp (Simplified Buy Matcher)</span>
          </div>
          <pre class="code-block">
std::vector&lt;Trade&gt; OrderBookBaseline::match_buy_order(Order&amp; incoming_buy) {
    std::vector&lt;Trade&gt; trades;

    <span class="code-comment">// OUTER LOOP: Walk price levels from lowest ask upwards</span>
    <span class="code-kw">while</span> (incoming_buy.quantity &gt; 0 &amp;&amp; !asks_.empty()) {
        <span class="code-kw">auto</span> best_ask_it = asks_.begin();
        Price best_ask_price = best_ask_it-&gt;first;

        <span class="code-comment">// Check if spread is crossed: Can buyer pay seller's price?</span>
        <span class="code-kw">if</span> (incoming_buy.price &lt; best_ask_price) {
            <span class="code-kw">break</span>; <span class="code-comment">// Bid is lower than cheapest ask. Stop matching!</span>
        }

        <span class="code-kw">auto</span>&amp; resting_queue = best_ask_it-&gt;second;

        <span class="code-comment">// INNER LOOP: Sweep orders at this price in FIFO order</span>
        <span class="code-kw">while</span> (incoming_buy.quantity &gt; 0 &amp;&amp; !resting_queue.empty()) {
            Order&amp; resting_ask = resting_queue.front(); <span class="code-comment">// Oldest order first</span>

            Quantity fill = std::min(incoming_buy.quantity, resting_ask.quantity);

            trades.push_back(Trade{
                .maker_order_id = resting_ask.order_id,
                .taker_order_id = incoming_buy.order_id,
                .price = best_ask_price, <span class="code-comment">// MAKER'S price!</span>
                .quantity = fill,
                .timestamp = incoming_buy.timestamp
            });

            incoming_buy.quantity -= fill;
            resting_ask.quantity  -= fill;

            <span class="code-kw">if</span> (resting_ask.is_filled()) {
                order_index_.erase(resting_ask.order_id);
                resting_queue.pop_front();
            }
        }

        <span class="code-kw">if</span> (resting_queue.empty()) {
            asks_.erase(best_ask_it); <span class="code-comment">// Remove exhausted price node from tree</span>
        }
    }

    <span class="code-comment">// If unfilled quantity remains, rest passively as a new bid</span>
    <span class="code-kw">if</span> (incoming_buy.quantity &gt; 0) {
        bids_[incoming_buy.price].push_back(incoming_buy);
        order_index_[incoming_buy.order_id] = {Side::BUY, incoming_buy.price};
    }

    <span class="code-kw">return</span> trades;
}
          </pre>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod3-2')">← Previous: 3-Layer Book</button>
          <button class="sim-btn" onclick="switchSection('mod3-4')">Next: 3.4 Cancellation & Amendment →</button>
        </div>
      </section>

      <!-- MODULE 3.4 -->
      <section id="mod3-4" class="section-block">
        <h1 class="course-h1">3.4 Order Amendments & FIFO Fairness Rules</h1>
        <p class="course-lead">
          Why reducing order size keeps your priority, but increasing size sends you to the back of the line.
        </p>

        <div class="code-container">
          <div class="code-header">
            <span>src/baseline/OrderBookBaseline.cpp Lines 170-188</span>
          </div>
          <pre class="code-block">
<span class="code-kw">if</span> (new_quantity &lt;= q_it-&gt;quantity) {
    <span class="code-comment">// REDUCTION: Modify in-place. Retains queue position (FIFO preserved).</span>
    q_it-&gt;quantity = new_quantity;
} <span class="code-kw">else</span> {
    <span class="code-comment">// INCREASE: Must LOSE priority to prevent market manipulation!</span>
    Order updated_order = *q_it;
    updated_order.quantity = new_quantity;
    queue.erase(q_it);              <span class="code-comment">// Remove from current position</span>
    queue.push_back(updated_order); <span class="code-comment">// Append to TAIL of the queue</span>
}
          </pre>
        </div>

        <div class="callout warning">
          <div class="callout-title">⚖️ The Market Fairness Rationale</div>
          <p>
            If traders were allowed to increase order size without losing queue priority, a malicious high-frequency trading firm could submit a 1-share buy order at every price level at 09:00:00 AM, locking in the #1 position in line. 
            Later, when news breaks, they could balloon those orders from 1 share to 1,000,000 shares, cutting in front of everyone who waited fairly. 
            <b>Exchange regulations dictate: Any size increase must forfeit time priority!</b>
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod3-3')">← Previous: Matching Loop</button>
          <button class="sim-btn" onclick="switchSection('mod3-5')">Next: 3.5 Latency Tail Cliff →</button>
        </div>
      </section>

      <!-- MODULE 3.5 -->
      <section id="mod3-5" class="section-block">
        <h1 class="course-h1">3.5 Baseline Benchmark & The Tail Cliff</h1>
        <p class="course-lead">
          Why the average latency is a lie, and why p99.9 latency reveals the truth about your architecture.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> Empirical Results on Your Machine</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Metric</th>
              <th>Measured Result</th>
              <th>What It Means in Reality</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Throughput</b></td>
              <td><b>602,410 orders/sec</b></td>
              <td>Good baseline, but 10x slower than institutional engines (5M+ orders/sec).</td>
            </tr>
            <tr>
              <td><b>p50 (Median)</b></td>
              <td><b>838.9 ns</b></td>
              <td>50% of orders process in under 839 nanoseconds.</td>
            </tr>
            <tr>
              <td><b>p99 Latency</b></td>
              <td><b>3,843.3 ns</b></td>
              <td>1 in 100 orders takes ~4 microseconds.</td>
            </tr>
            <tr>
              <td><b style="color: var(--accent-rose);">p99.9 Latency</b></td>
              <td><b style="color: var(--accent-rose);">83,626.2 ns (83.6 µs)</b></td>
              <td><b>THE TAIL CLIFF:</b> 100x latency explosion!</td>
            </tr>
            <tr>
              <td><b style="color: var(--accent-rose);">Max Outlier</b></td>
              <td><b style="color: var(--accent-rose);">3,755,147.9 ns (3.7 ms)</b></td>
              <td>Almost 4 MILLISECONDS of stall!</td>
            </tr>
          </tbody>
        </table>

        <div class="callout danger">
          <div class="callout-title">🚨 What causes the 83 µs spike and 3.7 ms outlier?</div>
          <p>
            When <code>std::list::push_back()</code> needs to store an order, it calls <code>malloc</code>. 
            If the heap memory arena is out of chunks, <code>malloc</code> calls the OS kernel (<code>brk</code> / <code>mmap</code> system call). 
            A context switch to the Windows kernel and back costs microseconds. 
            <b>Phase 2 fixes this completely by banning heap allocation on the hot path.</b>
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod3-4')">← Previous: Amendment</button>
          <button class="sim-btn" onclick="switchSection('mod4-1')">Next: Module 4 - Mechanical Sympathy →</button>
        </div>
      </section>

      <!-- MODULE 4.1 -->
      <section id="mod4-1" class="section-block">
        <h1 class="course-h1">4.1 The Memory Wall: CPU vs DRAM</h1>
        <p class="course-lead">
          Understanding the 200-cycle stall that cripples naive algorithms on modern silicon.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> Physical Reality: Nanoseconds on the Die</h2>
        <p>
          Your CPU runs at <b>2.50 GHz</b>. That means the processor clocks every:
          $$\text{Clock Cycle} = \frac{1}{2.50 \times 10^9 \text{ s}} = 0.40 \text{ nanoseconds}$$
        </p>
        <p>
          Every 0.4 nanoseconds, the ALU executes an arithmetic instruction.
          <br>
          Now look at how long it takes to fetch data across the motherboard from main memory (DRAM):
        </p>

        <table class="data-table">
          <thead>
            <tr>
              <th>Storage Level</th>
              <th>Physical Distance</th>
              <th>Access Latency</th>
              <th>Wasted CPU Cycles</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>CPU Registers</b></td>
              <td>On execution core</td>
              <td>0.0 ns</td>
              <td>0 cycles</td>
            </tr>
            <tr>
              <td><b>L1 Cache (32 KB)</b></td>
              <td>On core die</td>
              <td>~1.0 ns</td>
              <td>2 - 3 cycles</td>
            </tr>
            <tr>
              <td><b>L2 Cache (512 KB)</b></td>
              <td>On core die</td>
              <td>~3.5 ns</td>
              <td>8 - 12 cycles</td>
            </tr>
            <tr>
              <td><b>L3 Cache (16 MB)</b></td>
              <td>Shared on chip</td>
              <td>~12.0 ns</td>
              <td>30 - 40 cycles</td>
            </tr>
            <tr>
              <td><b style="color: var(--accent-rose);">Main DRAM (16 GB)</b></td>
              <td>Off-chip via bus</td>
              <td><b style="color: var(--accent-rose);">~80.0 ns</b></td>
              <td><b style="color: var(--accent-rose);">200 CPU CYCLES WASTED!</b></td>
            </tr>
          </tbody>
        </table>

        <div class="callout warning">
          <div class="callout-title">🛑 The "Stalled Core" Trap</div>
          <p>
            When your code dereferences a pointer to an un-cached memory address (like a linked list node), 
            the CPU cannot continue arithmetic. It sits <b>completely idle for 200 clock cycles</b> waiting for electrons to travel across the memory bus.
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod3-5')">← Previous: Latency Tail</button>
          <button class="sim-btn" onclick="switchSection('mod4-2')">Next: 4.2 Cache Lines & Prefetching →</button>
        </div>
      </section>

      <!-- MODULE 4.2 -->
      <section id="mod4-2" class="section-block">
        <h1 class="course-h1">4.2 Cache Lines (64 Bytes) & Prefetching</h1>
        <p class="course-lead">
          The CPU never moves single bytes — it always transfers 64-byte blocks.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> The 64-Byte Cache Line</h2>
        <p>
          When you read an 8-byte variable <code>order.price</code>, the memory controller does not fetch 8 bytes. 
          It pulls an entire <b>64-byte Cache Line</b> containing that address into L1 cache.
        </p>
        <p>
          If your next instruction reads <code>order.quantity</code> (which sits right next to it), it is <b>already inside L1 cache</b>. It takes 1 nanosecond instead of 80 nanoseconds. This is <b>Spatial Locality</b>.
        </p>

        <h2 class="course-h2"><span class="step-number">2</span> The Hardware Stream Prefetcher</h2>
        <p>
          Modern CPUs have an on-chip circuit called the <b>Hardware Stream Prefetcher</b>.
        </p>
        <p>
          If you loop sequentially through an array (indices $0, 1, 2, 3...$), the prefetcher recognizes the constant memory stride. 
          It predicts your next reads and fetches upcoming cache lines into L1 <b>before your code even asks for them</b>. DRAM latency is completely hidden!
        </p>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod4-1')">← Previous: Memory Wall</button>
          <button class="sim-btn" onclick="switchSection('mod4-3')">Next: 4.3 14.8x Benchmark Proof →</button>
        </div>
      </section>

      <!-- MODULE 4.3 -->
      <section id="mod4-3" class="section-block">
        <h1 class="course-h1">4.3 The 14.8x Empirical Proof: Vector vs List</h1>
        <p class="course-lead">
          Hands-on data from `benchmark/CacheBenchmark.cpp` proving contiguous memory dominates pointer chasing.
        </p>

        <table class="data-table">
          <thead>
            <tr>
              <th>Experiment</th>
              <th>Structure Tested</th>
              <th>Time (1,000,000 items)</th>
              <th>Time per Element</th>
              <th>Hardware Behavior</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Experiment 1A</b></td>
              <td><code>std::vector&lt;uint64_t&gt;</code></td>
              <td><b style="color: var(--accent-emerald);">0.74 ms</b></td>
              <td><b>0.74 ns</b></td>
              <td>Contiguous memory; hardware prefetcher active; 100% cache line reuse.</td>
            </tr>
            <tr>
              <td><b>Experiment 1B</b></td>
              <td><code>std::list&lt;uint64_t&gt;</code></td>
              <td><b style="color: var(--accent-rose);">11.00 ms</b></td>
              <td><b>11.00 ns</b></td>
              <td>Pointer chasing across heap; prefetcher defeated; repeated DRAM stalls.</td>
            </tr>
            <tr>
              <td><b>Experiment 3A</b></td>
              <td>Sequential Index Access</td>
              <td><b style="color: var(--accent-emerald);">0.65 ms</b></td>
              <td><b>0.65 ns</b></td>
              <td>Predictable stride; prefetcher loads data ahead of instruction pointer.</td>
            </tr>
            <tr>
              <td><b>Experiment 3B</b></td>
              <td>Shuffled Random Access</td>
              <td><b style="color: var(--accent-rose);">6.64 ms</b></td>
              <td><b>6.64 ns</b></td>
              <td>Unpredictable jumps; prefetcher fails; 10.2x slowdown on the SAME array!</td>
            </tr>
          </tbody>
        </table>

        <div class="callout success">
          <div class="callout-title">🏆 Key Takeaway for Week 1 vs Week 2</div>
          <p>
            In Phase 1, our order book used <code>std::list&lt;Order&gt;</code> for queues. 
            Our benchmark proves that <code>std::list</code> is <b>14.8x slower</b> than contiguous memory. 
            In Phase 2, we will replace <code>std::list</code> with an <b>intrusive slab list</b> stored inside a contiguous pre-allocated array.
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod4-2')">← Previous: Cache Lines</button>
          <button class="sim-btn" onclick="switchSection('mod4-lab')">Next: LAB 2 - Cache Simulator →</button>
        </div>
      </section>

      <!-- MODULE 4.LAB: CACHE SIMULATOR -->
      <section id="mod4-lab" class="section-block">
        <h1 class="course-h1">LAB 2: Interactive Cache Miss & Prefetch Simulator</h1>
        <p class="course-lead">
          See spatial locality and pointer chasing in action with real cache lines.
        </p>

        <div class="interactive-card">
          <span class="interactive-badge">⚡ Hardware Architecture Lab</span>
          <h3>Simulate 64-Byte Cache Line Traversal</h3>
          <p style="font-size: 13px; color: var(--text-muted);">
            Each cache line holds 8 variables (8 bytes each = 64 bytes total). Compare sequential contiguous array reads vs scattered linked list reads.
          </p>

          <div class="sim-controls">
            <button class="sim-btn" onclick="runCacheSim('vector')">Simulate std::vector (Contiguous)</button>
            <button class="sim-btn secondary" onclick="runCacheSim('list')">Simulate std::list (Pointer Chasing)</button>
          </div>

          <div style="margin-top: 18px;">
            <div style="font-size: 12px; font-weight: 700; color: var(--accent-cyan);">
              Current L1 Cache Line (64 Bytes = 8 uint64_t slots):
            </div>
            <div class="cache-line-box" id="cache-slots">
              <div class="cache-chunk">[0x00] Empty</div>
              <div class="cache-chunk">[0x08] Empty</div>
              <div class="cache-chunk">[0x10] Empty</div>
              <div class="cache-chunk">[0x18] Empty</div>
              <div class="cache-chunk">[0x20] Empty</div>
              <div class="cache-chunk">[0x28] Empty</div>
              <div class="cache-chunk">[0x30] Empty</div>
              <div class="cache-chunk">[0x38] Empty</div>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 12px; margin-top: 14px;">
            <div style="background: #060910; padding: 12px; border-radius: 6px; text-align: center;">
              <div style="font-size: 11px; color: var(--text-muted);">L1 Cache Hits (1 ns)</div>
              <div id="stat-hits" style="font-size: 20px; font-weight: 800; color: var(--accent-emerald);">0</div>
            </div>
            <div style="background: #060910; padding: 12px; border-radius: 6px; text-align: center;">
              <div style="font-size: 11px; color: var(--text-muted);">DRAM Stalls (80 ns)</div>
              <div id="stat-misses" style="font-size: 20px; font-weight: 800; color: var(--accent-rose);">0</div>
            </div>
            <div style="background: #060910; padding: 12px; border-radius: 6px; text-align: center;">
              <div style="font-size: 11px; color: var(--text-muted);">Total Simulated Latency</div>
              <div id="stat-latency" style="font-size: 20px; font-weight: 800; color: var(--accent-amber);">0 ns</div>
            </div>
          </div>

          <div class="log-terminal" id="cache-log" style="margin-top: 14px;">
            <div class="log-line system">[SIM] Click a simulation button to begin cache playback.</div>
          </div>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod4-3')">← Previous: 14.8x Benchmark</button>
          <button class="sim-btn" onclick="switchSection('mod5-1')">Next: Module 5 - Memory Layout →</button>
        </div>
      </section>

      <!-- MODULE 5.1 -->
      <section id="mod5-1" class="section-block">
        <h1 class="course-h1">5.1 Struct Memory Layout: The 7 Dead Padding Bytes</h1>
        <p class="course-lead">
          Inspecting how the MSVC 64-bit compiler physically organizes `struct Order` in memory.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> Natural Alignment Rules on x86-64</h2>
        <p>
          CPUs read memory most efficiently when data types start at addresses divisible by their size:
        </p>
        <ul style="margin-left: 20px; margin-bottom: 12px;">
          <li>A 1-byte <code>uint8_t</code> can start at any byte address.</li>
          <li>A 4-byte <code>uint32_t</code> must start at an address divisible by 4 (address % 4 == 0).</li>
          <li>An 8-byte <code>uint64_t</code> must start at an address divisible by 8 (address % 8 == 0).</li>
        </ul>

        <h2 class="course-h2"><span class="step-number">2</span> The Dissection of `struct Order`</h2>
        <table class="data-table">
          <thead>
            <tr>
              <th>Byte Range</th>
              <th>Member Name</th>
              <th>Type</th>
              <th>Size</th>
              <th>Hardware Alignment Note</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>0x00 .. 0x07</code></td>
              <td><code>order_id</code></td>
              <td><code>uint64_t</code></td>
              <td>8 bytes</td>
              <td>Starts at offset 0 (divisible by 8). Perfect.</td>
            </tr>
            <tr>
              <td><code>0x08</code></td>
              <td><code>side</code></td>
              <td><code>Side (uint8_t)</code></td>
              <td>1 byte</td>
              <td>Starts at offset 8. Ends at byte offset 9.</td>
            </tr>
            <tr style="background: rgba(244, 63, 94, 0.12);">
              <td><b style="color: var(--accent-rose);">0x09 .. 0x0F</b></td>
              <td><b style="color: var(--accent-rose);">*** DEAD PADDING ***</b></td>
              <td>---</td>
              <td><b style="color: var(--accent-rose);">7 bytes</b></td>
              <td><b>WASTED!</b> The next field <code>price</code> requires offset % 8 == 0 (offset 16).</td>
            </tr>
            <tr>
              <td><code>0x10 .. 0x17</code></td>
              <td><code>price</code></td>
              <td><code>uint64_t</code></td>
              <td>8 bytes</td>
              <td>Starts at offset 16 (16 % 8 == 0).</td>
            </tr>
            <tr>
              <td><code>0x18 .. 0x1B</code></td>
              <td><code>quantity</code></td>
              <td><code>uint32_t</code></td>
              <td>4 bytes</td>
              <td>Starts at offset 24 (24 % 4 == 0).</td>
            </tr>
            <tr>
              <td><code>0x1C .. 0x1F</code></td>
              <td><code>initial_quantity</code></td>
              <td><code>uint32_t</code></td>
              <td>4 bytes</td>
              <td>Starts at offset 28 (28 % 4 == 0). Packs tightly next to quantity!</td>
            </tr>
            <tr>
              <td><code>0x20 .. 0x27</code></td>
              <td><code>timestamp</code></td>
              <td><code>uint64_t</code></td>
              <td>8 bytes</td>
              <td>Starts at offset 32 (32 % 8 == 0).</td>
            </tr>
          </tbody>
        </table>

        <div class="callout warning">
          <div class="callout-title">⚠️ The Waste Ratio</div>
          <p>
            Actual data payload: 8 + 1 + 8 + 4 + 4 + 8 = <b>33 bytes</b>.
            <br>
            Total struct size in memory: <b>40 bytes</b>.
            <br>
            <b>17.5% of our struct is dead garbage padding!</b>
          </p>
          <p>
            <b>Phase 2 Superpower:</b> In Phase 2, we can pack Self-Trade Prevention flags, Time-In-Force enums, and intrusive linked list indices directly into those 7 dead padding bytes — adding features with <b>zero increase in memory footprint!</b>
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod4-lab')">← Previous: Cache Lab</button>
          <button class="sim-btn" onclick="switchSection('mod5-2')">Next: 5.2 Cache Line Splitting →</button>
        </div>
      </section>

      <!-- MODULE 5.2 -->
      <section id="mod5-2" class="section-block">
        <h1 class="course-h1">5.2 Cache Line Splitting (1.6 Orders/Line)</h1>
        <p class="course-lead">
          Why a 40-byte struct causes double memory bus cycles on modern 64-byte architecture.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> The Math of Cache Line Splitting</h2>
        <p>
          A CPU cache line is <b>64 bytes</b>. Our <code>Order</code> struct is <b>40 bytes</b>.
          $$\frac{64 \text{ bytes per cache line}}{40 \text{ bytes per order}} = 1.6 \text{ orders per line}$$
        </p>
        <p>
          Because 1.6 is not an integer, orders stored in an array do not align cleanly with cache lines:
        </p>

        <div class="code-container">
          <pre class="code-block">
Cache Line 0 (Bytes 0 - 63):
[ Order 0: Bytes 0 - 39 (40 bytes) ] | [ Order 1 (Part 1): Bytes 40 - 63 (24 bytes) ]
                                     ▲
                            64-Byte Cache Line Boundary!
Cache Line 1 (Bytes 64 - 127):
[ Order 1 (Part 2): Bytes 64 - 79 (16 bytes) ] | [ Order 2: Bytes 80 - 119 (40 bytes) ]
          </pre>
        </div>

        <div class="callout danger">
          <div class="callout-title">💥 The Performance Penalty</div>
          <p>
            Look at <b>Order 1</b>: Its first 24 bytes live in Cache Line 0, but its remaining 16 bytes live in Cache Line 1!
            <br><br>
            When the matching engine reads <code>Order[1].timestamp</code> (which sits at byte offset 72), the CPU must issue <b>TWO separate memory transactions</b> across the bus to read a single struct. 
            This effectively cuts memory bandwidth in half for split orders.
          </p>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod5-1')">← Previous: Struct Padding</button>
          <button class="sim-btn" onclick="switchSection('mod5-3')">Next: 5.3 Hot-Path Malloc & Volatiles →</button>
        </div>
      </section>

      <!-- MODULE 5.3 -->
      <section id="mod5-3" class="section-block">
        <h1 class="course-h1">5.3 Hot-Path Malloc & Volatile Sinks</h1>
        <p class="course-lead">
          Diagnosing the death of deterministic latency and preventing compiler dead-code elimination.
        </p>

        <h2 class="course-h2"><span class="step-number">1</span> Why `malloc` Must Be Banned on the Hot Path</h2>
        <p>
          Every time Phase 1 adds an order to <code>std::list</code>, it calls <code>malloc</code> to allocate a node:
        </p>
        <ol style="margin-left: 20px; margin-bottom: 14px;">
          <li><b>Heap Lock Contention:</b> The memory allocator locks thread arenas. If another thread allocates, your thread stalls.</li>
          <li><b>Free-List Traversal:</b> The allocator searches linked bins of memory blocks.</li>
          <li><b>Memory Fragmentation:</b> Heap nodes end up scattered across completely random DRAM addresses.</li>
          <li><b>Kernel Syscalls:</b> When pools run dry, the OS kernel executes a page fault or <code>mmap</code>. This is where the <b>3.7 ms outlier</b> originates!</li>
        </ol>

        <h2 class="course-h2"><span class="step-number">2</span> The `volatile` Sink in Benchmarking</h2>
        <p>
          When you compile with <code>/O2</code> (maximum optimization), the MSVC compiler examines your code:
        </p>
        <div class="code-container">
          <pre class="code-block">
<span class="code-kw">uint64_t</span> sum = 0;
<span class="code-kw">for</span> (<span class="code-kw">const auto</span>&amp; v : vec) sum += v;
<span class="code-comment">// If sum is never printed, the compiler says:</span>
<span class="code-comment">// "This loop produces no observable effect -&gt; DELETE THE ENTIRE LOOP!"</span>
<span class="code-comment">// Your benchmark measures 0 nanoseconds (measures nothing!).</span>
          </pre>
        </div>
        <p>
          In <code>benchmark/CacheBenchmark.cpp</code>, we use a global <code>volatile</code> sink:
        </p>
        <div class="code-container">
          <div class="code-header">
            <span>benchmark/CacheBenchmark.cpp Line 41</span>
          </div>
          <pre class="code-block">
<span class="code-kw">static volatile uint64_t</span> g_sink = 0;

<span class="code-comment">// After the timed loop:</span>
g_sink = vec_sum; <span class="code-comment">// Forces the compiler to keep the loop!</span>
          </pre>
        </div>
        <p>
          The <code>volatile</code> keyword tells the compiler: <i>"This variable could be read by hardware. You are legally forbidden from optimizing away writes to it."</i>
        </p>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod5-2')">← Previous: Cache Splitting</button>
          <button class="sim-btn" onclick="switchSection('mod5-lab')">Next: LAB 3 - Struct Layout Visualizer →</button>
        </div>
      </section>

      <!-- MODULE 5.LAB: STRUCT LAYOUT VISUALIZER -->
      <section id="mod5-lab" class="section-block">
        <h1 class="course-h1">LAB 3: Struct Memory Layout & Padding Inspector</h1>
        <p class="course-lead">
          Hover over individual bytes in our 40-byte `Order` struct to inspect offsets and alignment rules.
        </p>

        <div class="interactive-card">
          <span class="interactive-badge">🧩 Memory Layout Inspector</span>
          <h3>Byte-by-Byte Memory Map of `struct Order` (40 Bytes)</h3>
          <p style="font-size: 13px; color: var(--text-muted);">
            Each box represents 1 physical byte in RAM. Red striped boxes show the 7 dead padding bytes inserted by the compiler.
          </p>

          <div class="memory-grid" id="mem-grid"></div>

          <div class="mem-legend">
            <div class="mem-legend-item"><div class="mem-legend-box" style="background: #1e3a8a;"></div><span>order_id (8B)</span></div>
            <div class="mem-legend-item"><div class="mem-legend-box" style="background: #065f46;"></div><span>side (1B)</span></div>
            <div class="mem-legend-item"><div class="mem-legend-box" style="background: #991b1b;"></div><span style="color: var(--accent-rose); font-weight: 700;">Dead Padding (7B)</span></div>
            <div class="mem-legend-item"><div class="mem-legend-box" style="background: #581c87;"></div><span>price (8B)</span></div>
            <div class="mem-legend-item"><div class="mem-legend-box" style="background: #78350f;"></div><span>quantity (4B)</span></div>
            <div class="mem-legend-item"><div class="mem-legend-box" style="background: #854d0e;"></div><span>initial_quantity (4B)</span></div>
            <div class="mem-legend-item"><div class="mem-legend-box" style="background: #134e4a;"></div><span>timestamp (8B)</span></div>
          </div>

          <div id="byte-info-box" style="background: #060910; border: 1px solid var(--border-bright); border-radius: 6px; padding: 14px; margin-top: 16px; font-size: 13px;">
            Hover over any byte above to inspect its physical memory offset and purpose.
          </div>
        </div>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod5-3')">← Previous: Volatiles</button>
          <button class="sim-btn" onclick="switchSection('mod6-1')">Next: Module 6 - Connecting Week 1 to 2 →</button>
        </div>
      </section>

      <!-- MODULE 6.1 -->
      <section id="mod6-1" class="section-block">
        <h1 class="course-h1">6.1 Connecting Week 1 to Week 2 & Phase 2 Blueprint</h1>
        <p class="course-lead">
          The complete architectural bridge: Every baseline bottleneck diagnosed and mapped to its Phase 2 zero-allocation fix.
        </p>

        <table class="data-table">
          <thead>
            <tr>
              <th>Phase 1 Baseline Component</th>
              <th>Phase 1 Data Structure</th>
              <th>Hardware Flaw Diagnosed in Week 2</th>
              <th>Phase 2 Production Solution</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Price Level Tree</b></td>
              <td><code>std::map</code> (Red-Black BST)</td>
              <td>5 to 10 pointer dereferences per lookup; tree node cache misses.</td>
              <td><b style="color: var(--accent-emerald);">Direct-Indexed Flat Array:</b> <code>PriceLevel levels[2000]</code>. $O(1)$ single array index!</td>
            </tr>
            <tr>
              <td><b>FIFO Queues</b></td>
              <td><code>std::list&lt;Order&gt;</code></td>
              <td><b>14.8x slower</b> than contiguous memory. Scattered heap nodes.</td>
              <td><b style="color: var(--accent-emerald);">Intrusive Doubly-Linked List:</b> <code>prev_idx</code> / <code>next_idx</code> stored inside the pre-allocated order slab.</td>
            </tr>
            <tr>
              <td><b>Hot-Path Allocations</b></td>
              <td><code>new Order()</code> per submission</td>
              <td>100,000 <code>malloc</code> calls; heap lock contention; <b>83 µs p99.9 spikes</b>.</td>
              <td><b style="color: var(--accent-emerald);">Contiguous Slab Allocator:</b> 1,000,000 orders pre-allocated at boot. $O(1)$ pool pop, zero syscalls!</td>
            </tr>
            <tr>
              <td><b>Order ID Lookup</b></td>
              <td><code>std::unordered_map</code></td>
              <td>Hash collision chaining; bucket pointer dereferences; rehashing stalls.</td>
              <td><b style="color: var(--accent-emerald);">Flat Direct Dense Table:</b> <code>order_index[1M]</code>.</td>
            </tr>
            <tr>
              <td><b>Struct Alignment</b></td>
              <td>40-byte unaligned <code>Order</code></td>
              <td>7 dead bytes (17.5% waste); 1.6 orders/cache line causing split bus cycles.</td>
              <td><b style="color: var(--accent-emerald);">Bit-Packed Intrusive Order:</b> Flags and queue indices packed into dead padding bytes.</td>
            </tr>
          </tbody>
        </table>

        <div class="footer-nav">
          <button class="sim-btn secondary" onclick="switchSection('mod5-lab')">← Previous: Struct Lab</button>
          <button class="sim-btn" onclick="switchSection('mod7-quiz')">Next: Module 7 - Final Exam →</button>
        </div>
      </section>

      <!-- MODULE 7: QUIZ -->
      <section id="mod7-quiz" class="section-block">
        <h1 class="course-h1">7.1 Mastery Certification Exam</h1>
        <p class="course-lead">
          Test your knowledge across market mechanics, C++20 systems programming, and hardware architecture.
        </p>

        <div id="quiz-container"></div>

        <div style="text-align: center; margin-top: 30px;">
          <button class="sim-btn" style="padding: 12px 30px; font-size: 14px;" onclick="calculateQuizScore()">Submit Exam & Calculate Score</button>
        </div>

        <div id="exam-result" style="display: none; margin-top: 24px; padding: 20px; border-radius: 8px; text-align: center;"></div>
      </section>

    </div>
  </main>

  <script>
    // Navigation State
    function switchSection(secId) {
      document.querySelectorAll('.section-block').forEach(s => s.classList.remove('active'));
      const target = document.getElementById(secId);
      if (target) target.classList.add('active');

      document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
      const activeNav = Array.from(document.querySelectorAll('.nav-item')).find(el => {
        const attr = el.getAttribute('onclick');
        return attr && attr.includes(secId);
      });
      if (activeNav) activeNav.classList.add('active');

      document.getElementById('main-content').scrollTop = 0;
    }

    function switchTab(e, tabId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      e.target.classList.add('active');
      document.getElementById(tabId).classList.add('active');
    }

    // Progress Calculation
    function updateProgress(e) {
      if (e) e.stopPropagation();
      const checkboxes = document.querySelectorAll('.nav-checkbox');
      let checked = 0;
      checkboxes.forEach(cb => { if (cb.checked) checked++; });
      const percent = Math.round((checked / checkboxes.length) * 100);
      document.getElementById('overall-progress').style.width = percent + '%';
      document.getElementById('progress-percent').innerText = percent + '%';
      
      // Save state
      const state = {};
      checkboxes.forEach(cb => { state[cb.id] = cb.checked; });
      localStorage.setItem('lob_course_progress', JSON.stringify(state));
    }

    // Restore Progress
    window.addEventListener('DOMContentLoaded', () => {
      const saved = localStorage.getItem('lob_course_progress');
      if (saved) {
        try {
          const state = JSON.parse(saved);
          for (const id in state) {
            const cb = document.getElementById(id);
            if (cb) cb.checked = state[id];
          }
        } catch(e){}
      }
      updateProgress();
      initSimBook();
      initMemoryGrid();
      initQuiz();
    });

    // ------------------------------------------------------------------------
    // LAB 1: INTERACTIVE ORDER BOOK SIMULATOR
    // ------------------------------------------------------------------------
    let simBids = [];
    let simAsks = [];
    let orderIdCounter = 1000;

    function initSimBook() {
      simBids = [
        { id: 101, price: 150.00, qty: 500 },
        { id: 102, price: 149.95, qty: 1200 },
        { id: 103, price: 149.90, qty: 3000 }
      ];
      simAsks = [
        { id: 201, price: 150.05, qty: 800 },
        { id: 202, price: 150.10, qty: 2500 },
        { id: 203, price: 150.15, qty: 5000 }
      ];
      renderSimBook();
    }

    function renderSimBook() {
      // Sort
      simBids.sort((a,b) => b.price - a.price);
      simAsks.sort((a,b) => a.price - b.price);

      const bidsContainer = document.getElementById('sim-bids-list');
      const asksContainer = document.getElementById('sim-asks-list');

      bidsContainer.innerHTML = simBids.map(b => `
        <div class="ladder-row bid">
          <span>$${b.price.toFixed(2)}</span>
          <span>${b.qty.toLocaleString()} shs</span>
        </div>
      `).join('') || '<div style="color: #64748b; font-size: 11px; padding: 6px;">No resting bids</div>';

      asksContainer.innerHTML = simAsks.map(a => `
        <div class="ladder-row ask">
          <span>$${a.price.toFixed(2)}</span>
          <span>${a.qty.toLocaleString()} shs</span>
        </div>
      `).join('') || '<div style="color: #64748b; font-size: 11px; padding: 6px;">No resting asks</div>';

      const spreadEl = document.getElementById('sim-spread');
      if (simBids.length > 0 && simAsks.length > 0) {
        const bestBid = simBids[0].price;
        const bestAsk = simAsks[0].price;
        const spread = (bestAsk - bestBid).toFixed(2);
        spreadEl.innerText = `SPREAD: $${spread} (Best Bid: $${bestBid.toFixed(2)} | Best Ask: $${bestAsk.toFixed(2)})`;
      } else {
        spreadEl.innerText = "SPREAD: UNQUOTED (One or both sides empty)";
      }
    }

    function logSim(msg, type = "normal") {
      const log = document.getElementById('sim-log');
      const line = document.createElement('div');
      line.className = `log-line ${type}`;
      line.innerText = msg;
      log.appendChild(line);
      log.scrollTop = log.scrollHeight;
    }

    function submitSimOrder() {
      const side = document.getElementById('sim-side').value;
      const price = parseFloat(document.getElementById('sim-price').value);
      let qty = parseInt(document.getElementById('sim-qty').value);
      const id = ++orderIdCounter;

      if (isNaN(price) || isNaN(qty) || qty <= 0) {
        alert("Please enter a valid price and quantity!");
        return;
      }

      logSim(`[SUBMIT] Order #${id}: ${side} ${qty} shs @ $${price.toFixed(2)}`, "system");

      if (side === "BUY") {
        // Match against asks
        while (qty > 0 && simAsks.length > 0 && price >= simAsks[0].price) {
          const restingAsk = simAsks[0];
          const fill = Math.min(qty, restingAsk.qty);
          const execPrice = restingAsk.price; // MAKER PRICE!

          logSim(`>>> [TRADE] Order #${id} bought ${fill} shs from Order #${restingAsk.id} @ $${execPrice.toFixed(2)} (Maker's price)`, "trade");

          qty -= fill;
          restingAsk.qty -= fill;
          if (restingAsk.qty === 0) {
            simAsks.shift();
          }
        }
        if (qty > 0) {
          simBids.push({ id, price, qty });
          logSim(`[RESTING] Remaining ${qty} shs of Order #${id} placed into Bid book @ $${price.toFixed(2)}`);
        }
      } else {
        // SELL: Match against bids
        while (qty > 0 && simBids.length > 0 && price <= simBids[0].price) {
          const restingBid = simBids[0];
          const fill = Math.min(qty, restingBid.qty);
          const execPrice = restingBid.price; // MAKER PRICE!

          logSim(`>>> [TRADE] Order #${id} sold ${fill} shs to Order #${restingBid.id} @ $${execPrice.toFixed(2)} (Maker's price)`, "trade");

          qty -= fill;
          restingBid.qty -= fill;
          if (restingBid.qty === 0) {
            simBids.shift();
          }
        }
        if (qty > 0) {
          simAsks.push({ id, price, qty });
          logSim(`[RESTING] Remaining ${qty} shs of Order #${id} placed into Ask book @ $${price.toFixed(2)}`);
        }
      }

      renderSimBook();
    }

    function resetSimBook() {
      initSimBook();
      logSim("[RESET] Order book restored to initial 3-level demo state.", "system");
    }

    function runSweepDemo() {
      document.getElementById('sim-side').value = "BUY";
      document.getElementById('sim-price').value = "150.15";
      document.getElementById('sim-qty').value = "4000";
      submitSimOrder();
    }

    // ------------------------------------------------------------------------
    // LAB 2: CACHE SIMULATOR
    // ------------------------------------------------------------------------
    function runCacheSim(type) {
      const slots = document.getElementById('cache-slots').children;
      const log = document.getElementById('cache-log');
      log.innerHTML = '';

      let hits = 0;
      let misses = 0;
      let latency = 0;

      if (type === 'vector') {
        // Sequential vector: 1 miss per 8 elements, 7 hits!
        for (let i = 0; i < 8; i++) {
          slots[i].className = 'cache-chunk active-hit';
          slots[i].innerText = `vec[${i}] (HIT)`;
        }
        hits = 7;
        misses = 1;
        latency = (1 * 80) + (7 * 1); // 87 ns total for 8 elements = 10.8 ns/elem

        log.innerHTML = `
          <div class="log-line system">[CACHE LINE LOAD] Loaded 64 bytes into L1 (Elements 0 through 7).</div>
          <div class="log-line trade">[L1 HIT] Elements 1, 2, 3, 4, 5, 6, 7 read directly from L1 (1 ns each!).</div>
          <div class="log-line system">[PREFETCH] Hardware stream prefetcher detected stride +1, streaming next 64 bytes.</div>
        `;
      } else {
        // List: every element is a separate heap node -> 8 DRAM misses!
        for (let i = 0; i < 8; i++) {
          slots[i].className = 'cache-chunk active-miss';
          slots[i].innerText = `node[${i}] (MISS)`;
        }
        hits = 0;
        misses = 8;
        latency = 8 * 80; // 640 ns total

        log.innerHTML = `
          <div class="log-line trade" style="color: var(--accent-rose);">[DRAM STALL] Node 0 at 0x7FFF100 -> Cache Miss (80 ns stall)</div>
          <div class="log-line trade" style="color: var(--accent-rose);">[DRAM STALL] Node 1 at 0x7FFE940 -> Cache Miss (80 ns stall)</div>
          <div class="log-line trade" style="color: var(--accent-rose);">[DRAM STALL] Node 2 at 0x7FFF820 -> Cache Miss (80 ns stall)</div>
          <div class="log-line system">[FAILURE] Prefetcher defeated: Pointer addresses are scattered randomly across heap.</div>
        `;
      }

      document.getElementById('stat-hits').innerText = hits;
      document.getElementById('stat-misses').innerText = misses;
      document.getElementById('stat-latency').innerText = latency + " ns";
    }

    // ------------------------------------------------------------------------
    // LAB 3: STRUCT MEMORY GRID
    // ------------------------------------------------------------------------
    const byteLayout = [
      // 0..7: order_id
      ...Array(8).fill({ cls: 'id', name: 'order_id', size: '8 bytes', type: 'uint64_t', desc: 'Unique monotonic 64-bit identifier' }),
      // 8: side
      { cls: 'side', name: 'side', size: '1 byte', type: 'Side (uint8_t)', desc: '1-byte enum: BUY (0) or SELL (1)' },
      // 9..15: DEAD PADDING (7 bytes)
      ...Array(7).fill({ cls: 'pad', name: 'DEAD PADDING', size: '7 bytes', type: 'Unused Padding', desc: 'Wasted padding inserted by compiler to align price to offset 16 (offset % 8 == 0)' }),
      // 16..23: price
      ...Array(8).fill({ cls: 'price', name: 'price', size: '8 bytes', type: 'Price (uint64_t)', desc: 'Fixed-point integer ticks (e.g. 15025 = $150.25)' }),
      // 24..27: quantity
      ...Array(4).fill({ cls: 'qty', name: 'quantity', size: '4 bytes', type: 'Quantity (uint32_t)', desc: 'Remaining unfilled shares in the order' }),
      // 28..31: initial_quantity
      ...Array(4).fill({ cls: 'initqty', name: 'initial_quantity', size: '4 bytes', type: 'Quantity (uint32_t)', desc: 'Original size at order submission' }),
      // 32..39: timestamp
      ...Array(8).fill({ cls: 'ts', name: 'timestamp', size: '8 bytes', type: 'Timestamp (uint64_t)', desc: 'Arrival timestamp in nanoseconds or CPU clock ticks' }),
    ];

    function initMemoryGrid() {
      const grid = document.getElementById('mem-grid');
      grid.innerHTML = byteLayout.map((b, idx) => `
        <div class="mem-byte ${b.cls}" onmouseenter="showByteInfo(${idx})">
          <span class="offset">0x${idx.toString(16).toUpperCase().padStart(2,'0')}</span>
          <span>B${idx}</span>
        </div>
      `).join('');
    }

    function showByteInfo(idx) {
      const b = byteLayout[idx];
      const box = document.getElementById('byte-info-box');
      box.innerHTML = `
        <div style="font-weight: 700; color: var(--accent-cyan); font-size: 14px; margin-bottom: 4px;">
          Byte Offset [0x${idx.toString(16).toUpperCase().padStart(2,'0')}] (Byte ${idx} of 40): ${b.name}
        </div>
        <div><b>Type:</b> <code>${b.type}</code> | <b>Total Field Size:</b> ${b.size}</div>
        <div style="color: #cbd5e1; margin-top: 4px;">${b.desc}</div>
      `;
    }

    // ------------------------------------------------------------------------
    // QUIZ DATA & LOGIC
    // ------------------------------------------------------------------------
    const quizData = [
      {
        q: "1. When an incoming BUY order with a limit of $100.10 crosses the spread and matches a resting SELL order quoting $100.05, at what execution price does the trade occur?",
        opts: [
          "A) $100.10 (The Taker's limit price)",
          "B) $100.05 (The Maker's resting price — granting price improvement)",
          "C) $100.075 (The midpoint of the two prices)",
          "D) An auction price determined at end-of-day"
        ],
        ans: 1,
        exp: "In continuous double auction limit order books, execution ALWAYS occurs at the Maker's resting price. The aggressive taker receives price improvement."
      },
      {
        q: "2. Why is using IEEE-754 binary floating-point (`double`) strictly forbidden for price representation in institutional trading engines?",
        opts: [
          "A) Because double takes 16 bytes while integers take 4 bytes",
          "B) Because decimal fractions like 0.1 cannot be represented cleanly in base-2 binary, causing rounding noise in equality comparisons",
          "C) Because C++ does not allow doubles inside structs",
          "D) Because modern CPUs do not have floating-point units"
        ],
        ans: 1,
        exp: "In binary floating-point, 0.1 + 0.2 != 0.3 due to recurring binary fractions. Equality comparisons fail silently, causing missed trades and invalid books."
      },
      {
        q: "3. What is the fundamental difference between `enum Side` and `enum class Side : uint8_t` in C++20?",
        opts: [
          "A) There is no difference; it is purely stylistic",
          "B) enum class enforces scoped type safety (cannot accidentally compare with integers) and : uint8_t forces 1-byte storage instead of 4-byte int",
          "C) enum class makes all orders execute faster on the GPU",
          "D) enum class automatically converts strings to numbers"
        ],
        ans: 1,
        exp: "enum class prevents unsafe implicit conversions to int at compile-time, and : uint8_t shrinks memory footprint from 4 bytes to 1 byte, saving cache."
      },
      {
        q: "4. If a trader modifies an existing resting order in the book by REDUCING its quantity from 500 shares to 200 shares, what happens to their position in the FIFO queue?",
        opts: [
          "A) They lose all time priority and move to the back of the queue",
          "B) They retain their exact original priority in the queue (in-place modification)",
          "C) Their order is cancelled and rejected",
          "D) They are moved to the midpoint of the queue"
        ],
        ans: 1,
        exp: "Size reductions do not harm other market participants, so exchange rules allow in-place modification while preserving FIFO queue position. Only size increases forfeit priority."
      },
      {
        q: "5. In our CacheBenchmark experiment on 1,000,000 items, how much faster was `std::vector` compared to `std::list`?",
        opts: [
          "A) About 1.2x faster",
          "B) Exactly 2.0x faster",
          "C) 14.8x faster (0.74 ms vs 11.00 ms)",
          "D) std::list was faster because it has O(1) insertions"
        ],
        ans: 2,
        exp: "std::vector achieved 0.74 ms while std::list took 11.00 ms (14.8x speedup). std::vector benefits from spatial locality and hardware prefetching, whereas std::list stalls on DRAM pointer dereferences."
      },
      {
        q: "6. How many bytes does a single CPU cache line transfer between DRAM and the processor on modern x86-64 hardware?",
        opts: [
          "A) 8 bytes",
          "B) 32 bytes",
          "C) 64 bytes",
          "D) 128 bytes"
        ],
        ans: 2,
        exp: "Modern x86-64 processors always transfer memory in 64-byte chunks known as Cache Lines."
      },
      {
        q: "7. In our 64-bit `struct Order`, why does the compiler insert 7 dead padding bytes between `side` and `price`?",
        opts: [
          "A) To make the struct look symmetric in memory",
          "B) Because price is an 8-byte uint64_t and x86-64 natural alignment requires its starting address to be divisible by 8 (offset % 8 == 0)",
          "C) Because C++ reserves 7 bytes for struct metadata",
          "D) To store the order cancellation timestamp"
        ],
        ans: 1,
        exp: "side ends at byte offset 9. An 8-byte uint64_t must start at an address divisible by 8. The next multiple of 8 is 16, so bytes 9..15 are filled with 7 padding bytes."
      },
      {
        q: "8. Why is `sizeof(Order) = 40` dangerous when traversing an array of orders?",
        opts: [
          "A) Because 40 bytes is too large to fit in RAM",
          "B) Because 64 / 40 = 1.6 orders per cache line, causing alternate orders to split across two separate cache lines and doubling memory bus traffic",
          "C) Because the CPU cannot multiply by 40",
          "D) Because 40 is not a prime number"
        ],
        ans: 1,
        exp: "Non-power-of-two struct sizes that do not divide 64 evenly cause cache line splitting, forcing two memory transactions to read a single struct."
      },
      {
        q: "9. What is the root cause of the p99.9 latency tail spike (83 µs) and maximum outlier (3.7 ms) in our baseline engine?",
        opts: [
          "A) Floating-point calculations",
          "B) Heap allocations via malloc in std::list causing memory fragmentation, lock contention, and OS kernel page fault system calls",
          "C) The CPU cooling fan slowing down",
          "D) Slow disk writes"
        ],
        ans: 1,
        exp: "Calling malloc on the hot path introduces kernel transitions, free-list searches, and lock contention, creating severe tail latency spikes."
      },
      {
        q: "10. Why is a `volatile` sink required when benchmarking C++ loops compiled with `/O2` optimization?",
        opts: [
          "A) To make the CPU run at maximum turbo frequency",
          "B) To prevent the compiler's Dead-Code Elimination (DCE) pass from deleting the entire loop when it detects the result is unused",
          "C) To convert CPU clock ticks into nanoseconds",
          "D) To clear the L1 cache before the benchmark"
        ],
        ans: 1,
        exp: "With /O2, the compiler eliminates loops whose results are never read. Writing the final sum to a volatile variable legally forbids the compiler from deleting the loop."
      }
    ];

    function initQuiz() {
      const container = document.getElementById('quiz-container');
      container.innerHTML = quizData.map((q, qIdx) => `
        <div class="quiz-card" id="qcard-${qIdx}">
          <div class="quiz-q">${q.q}</div>
          <div class="quiz-options">
            ${q.opts.map((opt, optIdx) => `
              <div class="quiz-opt" id="qopt-${qIdx}-${optIdx}" onclick="selectQuizOpt(${qIdx}, ${optIdx})">
                <input type="radio" name="q-${qIdx}" id="qrad-${qIdx}-${optIdx}" style="pointer-events: none;">
                <span>${opt}</span>
              </div>
            `).join('')}
          </div>
          <div class="quiz-explain" id="qexp-${qIdx}"></div>
        </div>
      `).join('');
    }

    const userAnswers = {};

    function selectQuizOpt(qIdx, optIdx) {
      userAnswers[qIdx] = optIdx;
      document.querySelectorAll(`[id^='qopt-${qIdx}-']`).forEach(el => el.classList.remove('selected'));
      document.getElementById(`qopt-${qIdx}-${optIdx}`).classList.add('selected');
      document.getElementById(`qrad-${qIdx}-${optIdx}`).checked = true;
    }

    function calculateQuizScore() {
      let score = 0;
      quizData.forEach((q, qIdx) => {
        const selected = userAnswers[qIdx];
        const card = document.getElementById(`qcard-${qIdx}`);
        const expBox = document.getElementById(`qexp-${qIdx}`);
        expBox.style.display = 'block';

        if (selected === q.ans) {
          score++;
          document.getElementById(`qopt-${qIdx}-${selected}`).classList.add('correct');
          expBox.innerHTML = `<span style="color: var(--accent-emerald); font-weight: 700;">✓ Correct!</span> ${q.exp}`;
          expBox.style.borderLeftColor = 'var(--accent-emerald)';
        } else {
          if (selected !== undefined) {
            document.getElementById(`qopt-${qIdx}-${selected}`).classList.add('incorrect');
          }
          document.getElementById(`qopt-${qIdx}-${q.ans}`).classList.add('correct');
          expBox.innerHTML = `<span style="color: var(--accent-rose); font-weight: 700;">✗ Incorrect.</span> ${q.exp}`;
          expBox.style.borderLeftColor = 'var(--accent-rose)';
        }
      });

      const resBox = document.getElementById('exam-result');
      resBox.style.display = 'block';
      const pct = Math.round((score / quizData.length) * 100);
      if (pct >= 80) {
        resBox.style.background = 'rgba(16, 185, 129, 0.15)';
        resBox.style.border = '1px solid var(--accent-emerald)';
        resBox.innerHTML = `
          <h2 style="color: var(--accent-emerald); margin-bottom: 8px;">🎓 Exam Passed with Distinction!</h2>
          <div style="font-size: 18px; font-weight: 700;">Score: ${score} / ${quizData.length} (${pct}%)</div>
          <p style="color: #cbd5e1; margin-top: 8px;">You have mastered Week 1 market mechanics and Week 2 computer architecture fundamentals. You are ready to build Phase 2!</p>
        `;
      } else {
        resBox.style.background = 'rgba(245, 158, 11, 0.15)';
        resBox.style.border = '1px solid var(--accent-amber)';
        resBox.innerHTML = `
          <h2 style="color: var(--accent-amber); margin-bottom: 8px;">📚 Good Effort — Review Suggested</h2>
          <div style="font-size: 18px; font-weight: 700;">Score: ${score} / ${quizData.length} (${pct}%)</div>
          <p style="color: #cbd5e1; margin-top: 8px;">Review the explanations highlighted in red and re-test yourself to reach 100% mastery.</p>
        `;
      }
      resBox.scrollIntoView({ behavior: 'smooth' });
    }
  </script>
</body>
</html>
"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {output_path} successfully. Total characters: {len(html_content)}")

if __name__ == "__main__":
    create_course_html()
