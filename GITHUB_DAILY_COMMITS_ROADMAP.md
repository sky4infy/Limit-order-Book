# GitHub Daily 2-File Commit & Push Roadmap (24-Day Sequence)

## Overview & Workflow Strategy
All code, benchmarks, unit tests, and documentation across all 10 weeks are **100% completed, compiled, and verified on local branch `dev`**.

Your remote repository (`https://github.com/sky4infy/Limit-order-Book.git`) is currently clean on branch `main` at commit `9d0d335`.

To maintain an active daily contribution streak on GitHub while keeping your repository clean and professional, follow this exact schedule: **Each morning, open your terminal and run the 3 commands for that day.**

---

## Daily Command Cheatsheet

```bash
# General template for any day:
git checkout main
git checkout dev -- <file1> <file2>
git commit -m "<Commit Message>"
git push origin main
```

---

## Complete 24-Day Schedule

| Day | Milestone / Phase | File 1 to Commit | File 2 to Commit | Exact Commit Message |
|:---:|---|---|---|---|
| **Day 1** | Week 4: Coordinated Omission | `benchmark/CoordinatedOmissionBenchmark.cpp` | `WEEK_4_LATENCY_PROFILING_AND_COORDINATED_OMISSION.md` | `perf(week4): Coordinated Omission open-loop benchmark harness and architectural analysis` |
| **Day 2** | Week 4: Interview & Study Guide | `WEEK_4_INTERVIEW_PREPARATION_AND_DEFENSE.md` | `generate_week4_pdfs.py` | `docs(week4): Latency profiling interview defense and ReportLab study guide generator` |
| **Day 3** | Week 5: Concurrency & Affinity | `src/lockfree/ThreadAffinity.hpp` | `src/lockfree/SpscRingBuffer.hpp` | `feat(week5): Hardware core affinity pinning and cache-aligned lock-free SPSC ring buffer` |
| **Day 4** | Week 5: Single-Writer Engine | `src/lockfree/SingleWriterEngine.hpp` | `test/SpscRingBufferTests.cpp` | `feat(week5): LMAX Disruptor-style Single-Writer matching engine and SPSC stress tests` |
| **Day 5** | Week 5: Multi-Core Benchmark | `benchmark/MultiThreadedContentionBenchmark.cpp` | `WEEK_5_LOCK_FREE_CONCURRENCY_AND_SINGLE_WRITER.md` | `perf(week5): Mutex contention vs lock-free single-writer benchmark and architecture docs` |
| **Day 6** | Week 5: Interview & Study Guide | `WEEK_5_INTERVIEW_PREPARATION_AND_DEFENSE.md` | `generate_week5_pdfs.py` | `docs(week5): Lock-free concurrency interview defense and PDF study generator` |
| **Day 7** | Week 6: Endian & OUCH 5.0 | `src/protocol/Endian.hpp` | `src/protocol/Ouch5Messages.hpp` | `feat(week6): Hardware BSWAP endianness intrinsics and packed NASDAQ OUCH 5.0 wire structs` |
| **Day 8** | Week 6: ITCH 5.0 & Codec | `src/protocol/Itch5Messages.hpp` | `src/protocol/ProtocolCodec.hpp` | `feat(week6): NASDAQ TotalView-ITCH 5.0 wire packets and zero-copy binary codec` |
| **Day 9** | Week 6: Protocol Benchmark | `test/ProtocolTests.cpp` | `benchmark/ProtocolBenchmark.cpp` | `perf(week6): Zero-copy binary protocol vs JSON parsing benchmark and validation suite` |
| **Day 10** | Week 6: Protocol Docs | `WEEK_6_BINARY_EXCHANGE_PROTOCOLS_OUCH_AND_ITCH.md` | `WEEK_6_INTERVIEW_PREPARATION_AND_DEFENSE.md` | `docs(week6): Exchange binary protocols walkthrough and institutional interview guide` |
| **Day 11** | Week 6-7 Bridge | `generate_week6_pdfs.py` | `src/exchange/ExchangeTypes.hpp` | `feat(week7): Week 6 PDF generator and advanced exchange microstructure types` |
| **Day 12** | Week 7: Auction & Pro-Rata | `src/exchange/CallAuction.hpp` | `src/exchange/ProRataMatching.hpp` | `feat(week7): Walrasian equilibrium call auction engine and CME pro-rata allocation` |
| **Day 13** | Week 7: Advanced Orders | `src/exchange/AdvancedOrders.hpp` | `test/ExchangeMechanicsTests.cpp` | `feat(week7): Iceberg reserve orders, Self-Trade Prevention (STP), and unit test suite` |
| **Day 14** | Week 7: Auction Benchmark | `benchmark/AuctionBenchmark.cpp` | `WEEK_7_CALL_AUCTIONS_AND_ADVANCED_EXCHANGE_MECHANICS.md` | `perf(week7): Call auction uncrossing and FIFO vs Pro-Rata benchmark with architecture docs` |
| **Day 15** | Week 7: Interview & Study Guide | `WEEK_7_INTERVIEW_PREPARATION_AND_DEFENSE.md` | `generate_week7_pdfs.py` | `docs(week7): Exchange mechanics interview defense and Week 7 PDF study generator` |
| **Day 16** | Week 8: Micro-Price & VPIN | `src/microstructure/MicroPrice.hpp` | `src/microstructure/VpinCalculator.hpp` | `feat(week8): Sasha Stoikov micro-price estimator and rolling VPIN toxicity calculator` |
| **Day 17** | Week 8: Avellaneda-Stoikov | `src/microstructure/AvellanedaStoikovBot.hpp` | `test/MicrostructureTests.cpp` | `feat(week8): Avellaneda-Stoikov inventory market maker bot and microstructure unit tests` |
| **Day 18** | Week 8: Quant Benchmark | `benchmark/MicrostructureBenchmark.cpp` | `WEEK_8_MARKET_MICROSTRUCTURE_AND_QUANTITATIVE_STRATEGIES.md` | `perf(week8): 20M ops/s quantitative microstructure benchmark and strategy docs` |
| **Day 19** | Week 8: Interview & Study Guide | `WEEK_8_INTERVIEW_PREPARATION_AND_DEFENSE.md` | `generate_week8_pdfs.py` | `docs(week8): Market microstructure interview defense and Week 8 PDF study generator` |
| **Day 20** | Week 9: Journal & Visualizer | `src/persistence/MemoryMappedJournal.hpp` | `src/visualization/OrderBookVisualizer.hpp` | `feat(week9): Memory-mapped transaction journal and terminal Level 3 depth visualizer` |
| **Day 21** | Week 9: Replay Benchmark | `test/JournalReplayTests.cpp` | `benchmark/JournalBenchmark.cpp` | `test(week9): Deterministic crash replay test and 7.6M writes/s journal benchmark` |
| **Day 22** | Week 9: Persistence Docs | `WEEK_9_SYSTEM_HARDENING_DETERMINISM_AND_JOURNALING.md` | `WEEK_9_INTERVIEW_PREPARATION_AND_DEFENSE.md` | `docs(week9): System hardening, persistence architecture, and interview defense guide` |
| **Day 23** | Week 9-10 Bridge | `generate_week9_pdfs.py` | `package_weeks.py` | `build(week9): Week 9 PDF generator and multi-week study packaging automation` |
| **Day 24** | Week 10: Superday & Course | `WEEK_10_SUPERDAY_INTERVIEW_DEFENSE_AND_RESUME.md` | `COURSE_COMPLETE_10_WEEKS_INTERACTIVE.html` | `docs(week10): Superday interview mastery, quantitative resume, and interactive web course` |

---

## Example: Executing Day 1 Tomorrow Morning

```powershell
git checkout main
git checkout dev -- benchmark/CoordinatedOmissionBenchmark.cpp WEEK_4_LATENCY_PROFILING_AND_COORDINATED_OMISSION.md
git commit -m "perf(week4): Coordinated Omission open-loop benchmark harness and architectural analysis"
git push origin main
```
That's it! 10 seconds every morning maintains an active green contribution graph for nearly an entire month with institutional C++ commits.
