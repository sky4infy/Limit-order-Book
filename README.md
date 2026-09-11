# Ultra-Low-Latency Limit Order Book & HFT Engine (C++20)

[![C++20](https://img.shields.io/badge/Language-Modern%20C%2B%2B20-00599C.svg?style=flat&logo=c%2B%2B)](https://en.cppreference.com/w/cpp/20)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%2F%20Linux-blue.svg)](https://github.com/sky4infy/Limit-order-Book)
[![Build](https://img.shields.io/badge/Build-MSVC%20%2F%20GCC%20%2F%20Clang-success.svg)](build.bat)
[![Architecture](https://img.shields.io/badge/Architecture-Mechanical%20Sympathy-orange.svg)](#architecture--engineering-progression)

An institutional-grade, sub-microsecond **Limit Order Book & Electronic Trading Venue** developed from the ground up in Modern C++20. Designed with **mechanical sympathy** to demonstrate cache-conscious data structures, zero-allocation memory design, lock-free concurrency, and Wall Street binary exchange protocols (NASDAQ ITCH 5.0 / OUCH 5.0).

---

## 📊 Phase 1 Empirical Benchmark Results

Measured directly on hardware using x86 cycle counters (`__rdtsc()`) across **100,000 synthetic orders** (calibrated CPU frequency: ~2.50 GHz):

| Performance Metric | Phase 1 (Textbook Baseline) | Phase 2 Target (Zero-Alloc Slab) | Phase 3 Target (Lock-Free SPSC) |
| :--- | :--- | :--- | :--- |
| **Throughput** | **4,761,905 orders/sec** | ~8,000,000 orders/sec | **> 12,000,000 orders/sec** |
| **p50 (Median) Latency** | **149.8 nanoseconds** | < 100 nanoseconds | **< 60 nanoseconds** |
| **p90 Latency** | **297.7 nanoseconds** | < 180 nanoseconds | **< 120 nanoseconds** |
| **p99 Latency** | **585.7 nanoseconds** | < 350 nanoseconds | **< 250 nanoseconds** |
| **p99.9 Latency** | **2,740.8 nanoseconds** (2.7 µs) | < 800 nanoseconds | **< 450 nanoseconds** |
| **Max Outlier Latency** | **273,349.9 nanoseconds** (273.3 µs) | < 5 microseconds | **< 2.5 microseconds** |

> **The 1,824x Profiling Epiphany:** While median latency is **149.8 ns**, the worst-case outlier spikes to **273.3 µs**. This empirical delta proves the cost of dynamic heap allocation (`malloc`/`new`) and Red-Black tree pointer chasing in `std::map`, providing the concrete justification for Phase 2's **Contiguous Slab Allocator** and **Direct Array Ladder**.

---

## 🏛 Architecture & Evolutionary Progression

```
+---------------------------------------------------------------------------------------------------+
| PHASE 1: The "Textbook" Baseline (COMPLETED & VERIFIED)                                           |
| - Data Structures: std::map<Price, std::list<Order>> (Red-Black tree + FIFO doubly-linked list)  |
| - Logic: FIFO Price-Time priority, exact fills, partial fills, multi-level sweeps, cancellations  |
| - Benchmarking: Cycle-accurate RDTSC hardware timestamping & percentile extraction                |
+---------------------------------------------------------------------------------------------------+
                                                  |
                         [BOTTLENECK EXPOSED: Heap Allocator Lock & Cache Misses]
                                                  v
+---------------------------------------------------------------------------------------------------+
| PHASE 2: Mechanical Sympathy & Zero-Allocation (IN PROGRESS)                                      |
| - Memory: Contiguous Slab Allocator / Object Pool (0 malloc on hot path)                          |
| - Data Structures: Flat Direct-Indexed Price Array (O(1) BBO) + Intrusive Doubly-Linked List      |
| - Precision: Fixed-point 64-bit integer tick arithmetic (replaces IEEE 754 floats)                |
+---------------------------------------------------------------------------------------------------+
                                                  |
                         [BOTTLENECK EXPOSED: Mutex Lock Contention & MESI Ping-Pong]
                                                  v
+---------------------------------------------------------------------------------------------------+
| PHASE 3: Single-Writer Architecture & Lock-Free Ring Buffers                                      |
| - Concurrency: Dedicated Matching Core pinned to physical CPU core (Single-Writer Principle)      |
| - IPC: Lock-Free SPSC Ring Buffers (Disruptor pattern) with acquire-release memory semantics       |
| - Hardware Alignment: 64-byte cache padding (`alignas(64)`) to eliminate False Sharing           |
| - Persistence: Zero-copy append-only Memory-Mapped Journal (mmap) for deterministic state replay  |
+---------------------------------------------------------------------------------------------------+
                                                  |
                         [CAPABILITY GAP: Institutional Protocols & Market Microstructure]
                                                  v
+---------------------------------------------------------------------------------------------------+
| PHASE 4: Institutional Exchange Venue & Microstructure Sandbox                                    |
| - Protocols: NASDAQ OUCH 5.0 (binary entry) & NASDAQ ITCH 5.0 (UDP multicast Level 3 feed)       |
| - Exchange Rules: Pre-open Call Auction (Walrasian uncrossing) & CME-style Pro-Rata Matching      |
| - Advanced Orders: Iceberg / Reserve orders, Post-Only, and 4-mode Self-Trade Prevention (STP)     |
| - Microstructure: Sasha Stoikov's Micro-Price & VPIN (Order Flow Toxicity) calculation            |
+---------------------------------------------------------------------------------------------------+
```

---

## 📁 Repository Structure

```
Limit-order-Book/
├── src/
│   ├── common/
│   │   ├── Types.hpp                   # Domain types (Side, Price, Quantity, OrderId, Trade)
│   │   └── Order.hpp                   # Active Order struct with remaining qty & lifecycle
│   └── baseline/
│       ├── OrderBookBaseline.hpp       # std::map (Red-Black Tree) + std::list (FIFO Queue)
│       └── OrderBookBaseline.cpp       # Core matching loop (spread check, execution, resting)
├── test/
│   └── BaselineTests.cpp               # 6 correctness tests (exact fills, sweeps, cancellations)
├── benchmark/
│   └── BaselineBenchmark.cpp           # Hardware RDTSC latency & throughput profiler
├── build.bat                           # One-click MSVC C++20 build, test & benchmark runner
└── CMakeLists.txt                      # Cross-platform CMake C++20 build configuration
```

---

## ⚡ Quick Start

### Prerequisites
* Windows: Visual Studio 2019 / 2022 / 2026 BuildTools (`cl.exe` with C++20 support)
* Linux: GCC 11+ or Clang 14+ (`g++ -std=c++20 -O3`)
* CMake 3.20+ (optional)

### Build & Run on Windows (One-Click)
```cmd
.\build.bat
```
This automatically:
1. Detects and initializes the native 64-bit MSVC environment (`vcvars64.bat`),
2. Compiles and executes the unit test suite (`BaselineTests.exe`),
3. Displays the console order book depth ladder,
4. Compiles and runs the 100,000-order hardware benchmark (`BaselineBenchmark.exe`).

### Build with CMake (Cross-Platform)
```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
ctest --output-on-failure
./benchmark/BaselineBenchmark
```

---

## 🧪 Unit Test Coverage

All 6 core exchange invariants are verified with 100% assertion pass rates:
* `test_passive_resting`: Verifies orders rest on bids/asks and BBO is accurate.
* `test_exact_fill`: Exact match between Buy and Sell leaves the book completely empty.
* `test_partial_fill`: Aggressive order partially consumes resting liquidity.
* `test_multi_level_price_sweep`: Large orders sweep across multiple price levels.
* `test_fifo_time_priority`: Strict timestamp priority execution for identical price levels.
* `test_order_cancellation`: O(1) order cancellation and price level pruning.

---

## 👤 Author
**Akash** — Quantitative Engineering & Low-Latency Systems Architecture
