# Limit Order Book (C++20)

A high-performance institutional Limit Order Book (LOB) matching engine in Modern C++20 designed for electronic trading systems. Built following an **Evolutionary Systems Architecture** transitioning from a clean functional baseline to a zero-allocation, cache-aligned engine.

---

## 📌 Architecture & Evolutionary Roadmap

```
PHASE 1: Textbook Baseline (Week 1)
├── Data Structures : std::map<Price, std::list<Order>>
├── Memory          : Dynamic heap allocations (new/malloc per trade)
└── Performance     : ~4.17M ops/sec, p50: 167 ns, p99.9: 1,754 ns
          │
          ▼ [Hardware Profiling: 14.2x cache penalty & malloc tail jitter]
PHASE 2: Mechanical Sympathy & Zero-Allocation Hot Path (Weeks 2-3)
├── Memory          : Pre-allocated Contiguous Slab Allocator (1,000,000 orders)
├── Data Structures : Flat Direct-Indexed Price Ladder + Intrusive Doubly-Linked List
├── Lookup & BBO    : 2-Level 64-bit Occupancy Bitmask with CPU bit-scan intrinsics (lzcnt/tzcnt)
├── Order Index     : Zero-allocation FlatOrderIndex open-addressing hash table
└── Performance     : ~6.76M ops/sec, p50: 60 ns, p99.9: 545 ns
```

---

## ⚡ Empirical Benchmark Results: Phase 1 vs. Phase 2

Tested side-by-side with an identical workload of **100,000 synthetic orders** (price range: $99.00 to $101.00) using cycle-accurate x86 hardware timers (`__rdtsc`):

| Metric | Phase 1 (Baseline) | Phase 2 (Zero-Allocation) | Improvement |
| :--- | :--- | :--- | :--- |
| **Orders Processed** | 100,000 | 100,000 | **100% Match** |
| **Trades Executed** | 78,243 | 78,243 | **100% Parity (Zero Regressions)** |
| **Wall Clock Time** | 23 ms | 14 ms | **38.2% FASTER** |
| **Throughput** | 4,173,500 ops/sec | 6,756,848 ops/sec | **1.6x HIGHER** |
| **p50 Latency (Median)** | 167 ns | **60 ns** | **63.6% LOWER** |
| **p90 Latency** | 329 ns | **184 ns** | **44.0% LOWER** |
| **p99 Latency** | 654 ns | **347 ns** | **46.9% LOWER** |
| **p99.9 Tail Latency** | 1,754 ns | **545 ns** | **68.9% LOWER (Sub-µs tail)** |
| **Max Latency Outlier** | 411,359 ns | **60,971 ns** | **85.2% LOWER (Eliminated jitter)** |

---

## 📁 Repository Structure

```text
Limit-order-Book/
├── src/
│   ├── common/
│   │   ├── Types.hpp                   # Domain types (Price, Quantity, OrderId, Side, Trade)
│   │   └── Order.hpp                   # Baseline 40-byte Order struct
│   ├── baseline/
│   │   ├── OrderBookBaseline.hpp       # Baseline book (std::map + std::list)
│   │   └── OrderBookBaseline.cpp       # FIFO matching engine implementation
│   └── optimized/
│       ├── OptimizedOrder.hpp          # 64-byte cache-aligned order (alignas(64))
│       ├── SlabAllocator.hpp           # Zero-allocation contiguous object pool
│       ├── DirectPriceLadder.hpp       # O(1) direct array + 64-bit occupancy bitmask
│       ├── FlatOrderIndex.hpp          # Zero-allocation open-addressing hash table
│       ├── OrderBookOptimized.hpp      # Phase 2 matching engine header
│       └── OrderBookOptimized.cpp      # Zero-allocation matching engine implementation
├── test/
│   ├── BaselineTests.cpp               # Correctness test suite (fills, sweeps, cancels)
│   ├── MemoryLayoutTests.cpp           # Struct offset, padding & cache line splitting tests
│   ├── SlabAllocatorTests.cpp          # Slab allocator & flat hash table tests
│   └── OptimizedOrderBookTests.cpp     # Full parity & high-volume churn tests
├── benchmark/
│   ├── BaselineBenchmark.cpp           # Baseline RDTSC latency & throughput benchmark
│   ├── CacheBenchmark.cpp              # Cache locality, pointer-chasing & prefetcher benchmark
│   └── PhaseComparisonBenchmark.cpp    # Side-by-side Phase 1 vs Phase 2 benchmark
├── build.bat                           # Automated 14-step Windows MSVC build & run script
└── CMakeLists.txt                      # Cross-platform CMake C++20 build configuration
```

---

## 🚀 Quick Start

### Windows (MSVC)
Run the automated 14-step build script:
```cmd
.\build.bat
```
This compiles all targets with C++20 optimizations (`/O2`), executes all unit test suites, runs the hardware memory layout and cache benchmarks, and performs the side-by-side 100,000-order comparison benchmark.

### Linux / macOS (CMake)
```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
./BaselineTests
./MemoryLayoutTests
./CacheBenchmark
./SlabAllocatorTests
./OptimizedOrderBookTests
./PhaseComparisonBenchmark
```
