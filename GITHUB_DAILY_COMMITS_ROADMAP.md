# GitHub Daily Commit & Push Roadmap (28-Day Sequence: 2 Commits Per Day)

## Overview & Daily Workflow
All code, benchmarks, unit tests, and documentation across all 10 weeks are **100% completed, compiled, and verified on local branch `dev`**.

Your remote repository (`https://github.com/sky4infy/Limit-order-Book.git`) is currently clean on branch `main` at commit `9d0d335`.

To build a consistent, highly active GitHub contribution streak, follow this exact schedule: **Each morning, open PowerShell/Terminal in `d:\Limit Order Book` and copy-paste the commands for that day.**

Each day commits **2 files one by one**, producing **2 distinct institutional commits every day** and pushing them to `origin/main`.

---

## Daily Command Template

```powershell
git checkout main
git checkout dev -- <FILE_1>
git commit -m "<COMMIT_MESSAGE_1>"
git checkout dev -- <FILE_2>
git commit -m "<COMMIT_MESSAGE_2>"
git push origin main
```

---

## Complete Day-by-Day Sequence

### 📅 DAY 1 (Week 4: Coordinated Omission Benchmark & Architecture)
```powershell
git checkout main
git checkout dev -- benchmark/CoordinatedOmissionBenchmark.cpp
git commit -m "perf(telemetry): implement open-loop Coordinated Omission benchmark harness"
git checkout dev -- WEEK_4_LATENCY_PROFILING_AND_COORDINATED_OMISSION.md
git commit -m "docs(telemetry): architectural walkthrough of Gil Tene Coordinated Omission"
git push origin main
```

### 📅 DAY 2 (Week 4: Interview Defense & PDF Study Guide)
```powershell
git checkout main
git checkout dev -- WEEK_4_INTERVIEW_PREPARATION_AND_DEFENSE.md
git commit -m "docs(week4): add telemetry and latency profiling interview defense guide"
git checkout dev -- generate_week4_pdfs.py
git commit -m "build(week4): add automated ReportLab PDF generator for Week 4 study guide"
git push origin main
```

### 📅 DAY 3 (Week 5: Core Affinity & SPSC Ring Buffer)
```powershell
git checkout main
git checkout dev -- src/lockfree/ThreadAffinity.hpp
git commit -m "feat(concurrency): add cross-platform CPU core affinity pinning with SetThreadAffinityMask"
git checkout dev -- src/lockfree/SpscRingBuffer.hpp
git commit -m "feat(concurrency): implement cacheline-padded lock-free SPSC circular ring buffer"
git push origin main
```

### 📅 DAY 4 (Week 5: Single-Writer Architecture & Concurrency Tests)
```powershell
git checkout main
git checkout dev -- src/lockfree/SingleWriterEngine.hpp
git commit -m "feat(concurrency): add LMAX Disruptor-style Single-Writer thread matching engine"
git checkout dev -- test/SpscRingBufferTests.cpp
git commit -m "test(concurrency): add multi-threaded SPSC stress tests and FIFO ordering validation"
git push origin main
```

### 📅 DAY 5 (Week 5: Multi-Core Contention Benchmark & Architecture)
```powershell
git checkout main
git checkout dev -- benchmark/MultiThreadedContentionBenchmark.cpp
git commit -m "perf(concurrency): benchmark mutex lock contention vs lock-free single-writer queue"
git checkout dev -- WEEK_5_LOCK_FREE_CONCURRENCY_AND_SINGLE_WRITER.md
git commit -m "docs(concurrency): architectural analysis of false sharing and acquire-release semantics"
git push origin main
```

### 📅 DAY 6 (Week 5: Concurrency Interview Defense & Study Guide)
```powershell
git checkout main
git checkout dev -- WEEK_5_INTERVIEW_PREPARATION_AND_DEFENSE.md
git commit -m "docs(week5): add lock-free concurrency and memory model interview defense guide"
git checkout dev -- generate_week5_pdfs.py
git commit -m "build(week5): add automated ReportLab PDF generator for Week 5 concurrency guide"
git push origin main
```

### 📅 DAY 7 (Week 6: Hardware BSWAP Endian & NASDAQ OUCH 5.0)
```powershell
git checkout main
git checkout dev -- src/protocol/Endian.hpp
git commit -m "feat(protocol): add hardware BSWAP intrinsics for big-endian to little-endian conversion"
git checkout dev -- src/protocol/Ouch5Messages.hpp
git commit -m "feat(protocol): implement packed NASDAQ OUCH 5.0 binary order entry wire protocol"
git push origin main
```

### 📅 DAY 8 (Week 6: NASDAQ ITCH 5.0 & Zero-Copy Binary Codec)
```powershell
git checkout main
git checkout dev -- src/protocol/Itch5Messages.hpp
git commit -m "feat(protocol): implement packed NASDAQ TotalView-ITCH 5.0 tick feed wire protocol"
git checkout dev -- src/protocol/ProtocolCodec.hpp
git commit -m "feat(protocol): implement zero-copy binary parser and packet deserializer"
git push origin main
```

### 📅 DAY 9 (Week 6: Protocol Unit Tests & 25M msg/s Benchmark)
```powershell
git checkout main
git checkout dev -- test/ProtocolTests.cpp
git commit -m "test(protocol): add validation test suite for OUCH 5.0 and ITCH 5.0 wire packets"
git checkout dev -- benchmark/ProtocolBenchmark.cpp
git commit -m "perf(protocol): benchmark zero-copy binary parsing vs JSON at 25.4M msgs/sec"
git push origin main
```

### 📅 DAY 10 (Week 6: Binary Protocols Architecture & Interview Defense)
```powershell
git checkout main
git checkout dev -- WEEK_6_BINARY_EXCHANGE_PROTOCOLS_OUCH_AND_ITCH.md
git commit -m "docs(protocol): architectural walkthrough of NASDAQ binary protocols and framing"
git checkout dev -- WEEK_6_INTERVIEW_PREPARATION_AND_DEFENSE.md
git commit -m "docs(protocol): add exchange protocols and zero-copy deserialization interview guide"
git push origin main
```

### 📅 DAY 11 (Week 7: Exchange Microstructure Types & Week 6 PDF)
```powershell
git checkout main
git checkout dev -- src/exchange/ExchangeTypes.hpp
git commit -m "feat(exchange): define core microstructure types for auctions, STP policies, and icebergs"
git checkout dev -- generate_week6_pdfs.py
git commit -m "build(week6): add automated ReportLab PDF generator for Week 6 protocol guide"
git push origin main
```

### 📅 DAY 12 (Week 7: Walrasian Call Auction & CME Pro-Rata Matching)
```powershell
git checkout main
git checkout dev -- src/exchange/CallAuction.hpp
git commit -m "feat(exchange): implement Walrasian equilibrium call auction engine with 4-tier tie-breaking"
git checkout dev -- src/exchange/ProRataMatching.hpp
git commit -m "feat(exchange): implement CME pure and split FIFO/Pro-Rata proportional allocation"
git push origin main
```

### 📅 DAY 13 (Week 7: Iceberg Orders & Self-Trade Prevention)
```powershell
git checkout main
git checkout dev -- src/exchange/AdvancedOrders.hpp
git commit -m "feat(exchange): implement Iceberg reserve orders and 4 institutional STP policies"
git checkout dev -- test/ExchangeMechanicsTests.cpp
git commit -m "test(exchange): add unit tests for Walrasian uncrossing, Pro-Rata math, and STP"
git push origin main
```

### 📅 DAY 14 (Week 7: Auction Benchmark & Exchange Architecture)
```powershell
git checkout main
git checkout dev -- benchmark/AuctionBenchmark.cpp
git commit -m "perf(exchange): benchmark 10,000-order call auction cross and FIFO vs Pro-Rata allocation"
git checkout dev -- WEEK_7_CALL_AUCTIONS_AND_ADVANCED_EXCHANGE_MECHANICS.md
git commit -m "docs(exchange): architectural deep dive into Walrasian uncrossing and Pro-Rata mechanics"
git push origin main
```

### 📅 DAY 15 (Week 7: Exchange Interview Defense & Study Guide)
```powershell
git checkout main
git checkout dev -- WEEK_7_INTERVIEW_PREPARATION_AND_DEFENSE.md
git commit -m "docs(week7): add exchange microstructure and market design interview defense guide"
git checkout dev -- generate_week7_pdfs.py
git commit -m "build(week7): add automated ReportLab PDF generator for Week 7 exchange guide"
git push origin main
```

### 📅 DAY 16 (Week 8: Sasha Stoikov Micro-Price & Real-Time VPIN)
```powershell
git checkout main
git checkout dev -- src/microstructure/MicroPrice.hpp
git commit -m "feat(microstructure): implement Sasha Stoikov queue-imbalance Micro-Price estimator"
git checkout dev -- src/microstructure/VpinCalculator.hpp
git commit -m "feat(microstructure): implement rolling Volume-Synchronized Probability of Toxicity (VPIN)"
git push origin main
```

### 📅 DAY 17 (Week 8: Avellaneda-Stoikov Market Maker & Strategy Tests)
```powershell
git checkout main
git checkout dev -- src/microstructure/AvellanedaStoikovBot.hpp
git commit -m "feat(strategy): implement optimal dynamic limit order quoter with inventory risk skew"
git checkout dev -- test/MicrostructureTests.cpp
git commit -m "test(microstructure): add unit tests for Micro-Price, VPIN volume buckets, and quote skew"
git push origin main
```

### 📅 DAY 18 (Week 8: 20M eval/s Microstructure Benchmark & Strategy Docs)
```powershell
git checkout main
git checkout dev -- benchmark/MicrostructureBenchmark.cpp
git commit -m "perf(microstructure): benchmark 1,000,000 evaluations of Micro-Price, VPIN, and quoter"
git checkout dev -- WEEK_8_MARKET_MICROSTRUCTURE_AND_QUANTITATIVE_STRATEGIES.md
git commit -m "docs(microstructure): mathematical derivation of Stoikov Micro-Price and Avellaneda model"
git push origin main
```

### 📅 DAY 19 (Week 8: Strategy Interview Defense & Study Guide)
```powershell
git checkout main
git checkout dev -- WEEK_8_INTERVIEW_PREPARATION_AND_DEFENSE.md
git commit -m "docs(week8): add quantitative market making and order flow toxicity interview guide"
git checkout dev -- generate_week8_pdfs.py
git commit -m "build(week8): add automated ReportLab PDF generator for Week 8 quantitative guide"
git push origin main
```

### 📅 DAY 20 (Week 9: Memory-Mapped Journal & L3 Terminal Visualizer)
```powershell
git checkout main
git checkout dev -- src/persistence/MemoryMappedJournal.hpp
git commit -m "feat(persistence): implement zero-syscall append-only memory-mapped transaction journal"
git checkout dev -- src/visualization/OrderBookVisualizer.hpp
git commit -m "feat(visualization): implement live Level 3 ASCII market depth terminal visualizer"
git push origin main
```

### 📅 DAY 21 (Week 9: Replay Tests & 10M writes/s Journal Benchmark)
```powershell
git checkout main
git checkout dev -- test/JournalReplayTests.cpp
git commit -m "test(persistence): add unit tests for checksum integrity and 100% crash recovery replay"
git checkout dev -- benchmark/JournalBenchmark.cpp
git commit -m "perf(persistence): benchmark 1M journal writes (10.2M/s) and sub-second crash replay"
git push origin main
```

### 📅 DAY 22 (Week 9: Persistence Architecture & Interview Defense)
```powershell
git checkout main
git checkout dev -- WEEK_9_SYSTEM_HARDENING_DETERMINISM_AND_JOURNALING.md
git commit -m "docs(persistence): architectural deep dive into memory-mapped zero-syscall persistence"
git checkout dev -- WEEK_9_INTERVIEW_PREPARATION_AND_DEFENSE.md
git commit -m "docs(persistence): add crash recovery determinism and journaling interview defense"
git push origin main
```

### 📅 DAY 23 (Week 9-10 Bridge: Study Packaging & Core Engine Updates)
```powershell
git checkout main
git checkout dev -- generate_week9_pdfs.py
git commit -m "build(week9): add automated ReportLab PDF generator for Week 9 persistence guide"
git checkout dev -- package_weeks.py
git commit -m "build(tooling): add multi-week study package generator and zip bundler"
git push origin main
```

### 📅 DAY 24 (Engine Hardening: Order Model & Build System)
```powershell
git checkout main
git checkout dev -- src/common/Order.hpp
git commit -m "refactor(common): optimize baseline Order struct constructors and timestamp fidelity"
git checkout dev -- CMakeLists.txt
git commit -m "build(cmake): expand CMake configuration with all 10-week libraries, tests, and benchmarks"
git push origin main
```

### 📅 DAY 25 (Engine Automation: 38-Step Runner & Git Filtering)
```powershell
git checkout main
git checkout dev -- build.bat
git commit -m "build(scripts): update automated MSVC runner to comprehensive 38-step verification suite"
git checkout dev -- .gitignore
git commit -m "chore(git): configure clean repository filtering for compiler artifacts and journals"
git push origin main
```

### 📅 DAY 26 (Week 10: Superday Mastery & Quant Resume)
```powershell
git checkout main
git checkout dev -- WEEK_10_SUPERDAY_INTERVIEW_DEFENSE_AND_RESUME.md
git commit -m "docs(week10): add Superday interview trap defenses and institutional quantitative resume"
git checkout dev -- generate_week10_pdfs.py
git commit -m "build(week10): add automated ReportLab PDF generator for Week 10 Superday guide"
git push origin main
```

### 📅 DAY 27 (Week 10: Interactive Web Course & Contribution Roadmap)
```powershell
git checkout main
git checkout dev -- COURSE_COMPLETE_10_WEEKS_INTERACTIVE.html
git commit -m "docs(course): add interactive 10-week dark-mode web course with flashcards and depth charts"
git checkout dev -- GITHUB_DAILY_COMMITS_ROADMAP.md
git commit -m "docs(roadmap): add 28-day daily contribution roadmap and commit sequence guide"
git push origin main
```

### 📅 DAY 28 (Project Completion: Master Repository Showcase)
```powershell
git checkout main
git checkout dev -- README.md
git commit -m "docs(readme): comprehensive 10-week institutional showcase, 38/38 builds, and master benchmarks"
git push origin main
```
