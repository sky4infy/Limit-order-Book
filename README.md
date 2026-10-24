# High-Performance Institutional Limit Order Book (C++20)

[![Standard](https://img.shields.io/badge/C%2B%2B-20-blue.svg?logo=c%2B%2B)](https://en.cppreference.com/w/cpp/20)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/sky4infy/Limit-order-Book)
[![Compiler](https://img.shields.io/badge/Compiler-MSVC%20%7C%20Clang%20%7C%20GCC-purple.svg)](https://github.com/sky4infy/Limit-order-Book)
[![Architecture](https://img.shields.io/badge/Architecture-x86--64%20(RDTSC%20%2B%20Bit--Scan)-orange.svg)](https://github.com/sky4infy/Limit-order-Book)
[![Build Status](https://img.shields.io/badge/Build%20%26%20Tests-14%2F14%20Passing-brightgreen.svg)](https://github.com/sky4infy/Limit-order-Book)
[![Throughput](https://img.shields.io/badge/Throughput-8.08M%20ops%2Fsec-success.svg)](https://github.com/sky4infy/Limit-order-Book)
[![Latency](https://img.shields.io/badge/p50%20Latency-53%20ns-critical.svg)](https://github.com/sky4infy/Limit-order-Book)

A production-grade, low-latency institutional Limit Order Book (LOB) matching engine implemented in Modern C++20. Engineered following an **Evolutionary Systems Architecture**, this project documents and benchmarks the mechanical transition from an algorithmic textbook baseline (`std::map` + `std::list`) to an ultra-low-latency, zero-allocation matching engine optimized for modern x86 CPU memory hierarchies and hardware prefetchers.

---

## 📑 Table of Contents

- [Architectural Evolution](#-architectural-evolution)
- [Empirical Benchmark Results](#-empirical-benchmark-results)
  - [Side-by-Side Engine Comparison (100k Orders)](#1-side-by-side-engine-comparison-100000-orders)
  - [Microarchitectural Memory & Cache Benchmarks (1M Elements)](#2-microarchitectural-memory--cache-benchmarks-1000000-elements)
  - [Memory Layout & Cache-Line Alignment Findings](#3-memory-layout--cache-line-alignment-findings)
- [Key Architectural Components](#-key-architectural-components)
  - [1. Cache-Aligned Order Layout (`OptimizedOrder`)](#1-cache-aligned-order-layout-optimizedorder)
  - [2. Contiguous Slab Allocator (`SlabAllocator`)](#2-contiguous-slab-allocator-slaballocator)
  - [3. Direct Price Ladder & Bitmask (`DirectPriceLadder`)](#3-direct-price-ladder--bitmask-directpriceladder)
  - [4. Flat Open-Addressing Hash Table (`FlatOrderIndex`)](#4-flat-open-addressing-hash-table-flatorderindex)
  - [5. Zero-Allocation Matching Loop (`OrderBookOptimized`)](#5-zero-allocation-matching-loop-orderbookoptimized)
- [Architecture Comparison Matrix](#-architecture-comparison-matrix)
- [Repository Structure](#-repository-structure)
- [Quick Start & Build Guide](#-quick-start--build-guide)
  - [Windows (MSVC Automated Runner)](#windows-msvc)
  - [Cross-Platform (CMake - Linux / macOS)](#cross-platform-cmake---linux--macos)
- [API Usage Example](#-api-usage-example)
- [Testing & Functional Parity Verification](#-testing--functional-parity-verification)

---

## 🏛 Architectural Evolution

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 1: Textbook Baseline Engine                          │
│  Data Structure  : std::map<Price, std::list<Order>> (Red-Black Tree)         │
│  Memory Strategy : Dynamic heap allocations (new / malloc per trade event)    │
│  Throughput      : ~4.47M ops/sec                                             │
│  Latency Profile : p50 = 154 ns, p99 = 633 ns, Max Outlier = 372,052 ns        │
└──────────────────────────────────────┬────────────────────────────────────────┘
                                       │
            Hardware Profiling Bottlenecks Identified (RDTSC & Memory Auditing):
            ├── 12.3x pointer-chasing penalty in std::list vs contiguous memory
            ├── 4.2x latency penalty caused by cache misses / lack of prefetching
            ├── 7 bytes dead compiler padding in Order struct (40-byte unaligned)
            └── Sub-millisecond malloc & hash-table rehash tail latency jitter
                                       │
                                       ▼
┌───────────────────────────────────────────────────────────────────────────────┐
│          PHASE 2: Mechanical Sympathy & Zero-Allocation Engine                │
│  Memory Strategy : Contiguous Pre-allocated Slab Allocator (1,000,000 orders) │
│  Cache Alignment : alignas(64) 64-byte orders (exactly 1 L1 cache line)       │
│  Price Ladder    : Direct-indexed flat array (131,072 levels, O(1) tick lookup)│
│  BBO Discovery   : 2-Level 64-bit Occupancy Bitmask with CPU LZCNT / TZCNT    │
│  Order Hash Index: Flat open-addressing table with backward-shift deletion    │
│  Throughput      : ~8.08M ops/sec (+80.7% faster, 1.8x throughput)            │
│  Latency Profile : p50 = 53 ns, p99 = 304 ns, Max Outlier = 57,836 ns         │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Empirical Benchmark Results

All benchmarks were compiled with MSVC `/std:c++20 /O2` and profiled using cycle-accurate hardware counters (`__rdtsc`) calibrated against system wall clock on an x86-64 CPU (~2.50 GHz base frequency).

### 1. Side-by-Side Engine Comparison (100,000 Orders)

Tested with a deterministic sequence of **100,000 synthetic orders** spanning prices $99.00 to $101.00 (70% passive resting limit orders, 30% aggressive market/crossing limit orders):

| Metric | Phase 1 (Baseline) | Phase 2 (Zero-Allocation) | Performance Delta |
| :--- | :--- | :--- | :--- |
| **Orders Ingested** | 100,000 | 100,000 | **100% Match** |
| **Trades Executed** | 78,243 | 78,243 | **100% Exact Parity** |
| **Wall Clock Execution** | 22 ms | **12 ms** | **44.7% Reduction** |
| **Sustained Throughput** | 4,473,292 ops/sec | **8,084,205 ops/sec** | **1.8x Faster (+80.7%)** |
| **p50 Latency (Median)** | 154 ns | **53 ns** | **65.3% Lower (Sub-60 ns)** |
| **p90 Latency** | 307 ns | **160 ns** | **47.9% Lower** |
| **p99 Latency** | 633 ns | **304 ns** | **51.9% Lower** |
| **p99.9 Tail Latency** | 1,704 ns | **1,163 ns** | **31.8% Lower** |
| **Max Latency Outlier** | 372,052 ns (372 µs) | **57,836 ns (57 µs)** | **84.5% Jitter Reduction** |

> **Key Takeaway**: Phase 2 achieves **8.08+ Million orders/sec** with a median latency of **53 nanoseconds**, while cutting tail latency jitter by **84.5%** by completely removing heap allocation and tree traversal from the critical path.

---

### 2. Microarchitectural Memory & Cache Benchmarks (1,000,000 Elements)

Empirical verification of CPU cache locality and hardware prefetcher behavior:

| Benchmark Experiment | Contiguous Access | Pointer / Node Chasing | Speedup Ratio | Microarchitectural Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Vector vs List Traversal** | `0.51 ms` (0.515 ns/elem) | `6.35 ms` (6.354 ns/elem) | **12.3x Faster** | L1/L2 Spatial Cache Locality |
| **Struct Array vs Pointer Array** | `1.83 ms` (1.828 ns/elem) | `2.63 ms` (2.630 ns/elem) | **1.4x Faster** | Pointer dereference bypass |
| **Sequential vs Random Access** | `0.68 ms` (0.675 ns/elem) | `2.82 ms` (2.817 ns/elem) | **4.2x Faster** | Hardware Stream Prefetcher hit |

---

### 3. Memory Layout & Cache-Line Alignment Findings

Field offset audits in `MemoryLayoutTests.cpp` demonstrated critical hardware bottlenecks in naive C++ structs:

* **Padding Waste**: The naive 40-byte `Order` struct suffered from **7 bytes of dead compiler padding** between 1-byte `Side` and 8-byte `Price`.
* **Cache Line Splitting**: At 40 bytes per order, every second order in an array crosses a 64-byte L1 cache line boundary. Accessing that single order forces the CPU memory controller to issue **two separate L1 cache line requests**.
* **Node Overhead in `std::list`**: A standard doubly-linked list node adds **16 bytes of pointer metadata** plus allocator control blocks, consuming ~5 MB for 100,000 orders compared to ~3 MB for flat contiguous records.

---

## 🧩 Key Architectural Components

```text
               ┌────────────────────────────────────────────────────────┐
               │                  OrderBookOptimized                    │
               └───────────┬────────────────┬───────────────────────────┘
                           │                │
            ┌──────────────▼──────┐   ┌─────▼───────────────────────────┐
            │   DirectPriceLadder │   │         FlatOrderIndex          │
            │   - 131,072 levels  │   │  - Open-addressing hash table   │
            │   - 2-Level Bitmask │   │  - Power-of-2 linear probing    │
            │   - CPU lzcnt/tzcnt │   │  - Backward-shift deletion      │
            └──────────────┬──────┘   └─────────────────────────────────┘
                           │
            ┌──────────────▼────────────────────────────────────────────┐
            │             SlabAllocator<OptimizedOrder, 1M>             │
            │  - Pre-allocated contiguous pool (alignas(64))            │
            │  - Intrusive doubly-linked queue pointers (prev/next_idx) │
            │  - Free-index stack (O(1) allocate/deallocate)            │
            └───────────────────────────────────────────────────────────┘
```

### 1. Cache-Aligned Order Layout (`OptimizedOrder`)
* **Size & Alignment**: Marked `alignas(64)` and explicitly padded to **exactly 64 bytes** (one CPU cache line).
* **Intrusive Links**: Embeds 32-bit `prev_idx` and `next_idx` directly into the order struct, eliminating `std::list` heap wrappers and pointer chasing.
* **Zero Padding Waste**: Fields re-ordered in descending size order (8-byte primitives $\to$ 4-byte primitives $\to$ 1-byte enum $\to$ 23-byte explicit tail padding).

### 2. Contiguous Slab Allocator (`SlabAllocator`)
* **Pre-allocation**: Allocates a contiguous arena of 1,000,000 orders at startup.
* **O(1) Allocation/Free**: Managed via a vector-backed free index stack. Allocation is a single `pop_back()`, deallocation is a single `push_back()`.
* **Zero Hot-Path Syscalls**: 0 OS memory requests, 0 mutex contention, 0 memory fragmentation during trading hours.

### 3. Direct Price Ladder & Bitmask (`DirectPriceLadder`)
* **Direct Array Indexing**: Maps tick prices directly to array indices ($O(1)$ lookup for price levels up to 131,072 ticks).
* **Hierarchical 64-bit Bitmask**: Tracks active price occupancy in 64-bit words, summarized by a top-level mask.
* **Hardware Bit-Scan Intrinsics**: Computes Best Bid (highest set bit) using `_BitScanReverse64` (`lzcnt`) and Best Offer (lowest set bit) using `_BitScanForward64` (`tzcnt`) in **1 CPU clock cycle**.

### 4. Flat Open-Addressing Hash Table (`FlatOrderIndex`)
* **Zero Dynamic Allocation**: Replaces node-based `std::unordered_map` with a flat array of 262,144 slots.
* **Fast Probing**: Power-of-two capacity enables fast bitwise indexing (`hash & (Capacity - 1)`) with linear probing.
* **Backward-Shift Deletion**: Elements in collision chains are shifted backward upon deletion, eliminating tombstone clutter and keeping lookup chains short.

### 5. Zero-Allocation Matching Loop (`OrderBookOptimized`)
* **Strict Price-Time Priority (FIFO)**: Matches incoming aggressive market or crossing limit orders against resting maker volume at the BBO.
* **Deterministic Execution**: Generates fill trades and frees drained orders back to the slab allocator without touching the system heap.

---

## 📊 Architecture Comparison Matrix

| Architectural Feature | Phase 1: Baseline Engine | Phase 2: Optimized Engine |
| :--- | :--- | :--- |
| **Price Ladder** | `std::map<Price, ...>` (Red-Black Tree) | Direct-Indexed Contiguous Array |
| **Price Lookup** | $O(\log N)$ tree traversal | $O(1)$ direct array index |
| **BBO Discovery** | `map::rbegin()` / `map::begin()` with tree traversal | Hierarchical 64-bit bitmask (`lzcnt` / `tzcnt`) in 1 cycle |
| **Price Level Queue** | `std::list<Order>` (node-based doubly-linked list) | Intrusive doubly-linked indices in contiguous slab |
| **Order Index** | `std::unordered_map<OrderId, ...>` (bucket nodes) | `FlatOrderIndex` (open-addressing, linear probing) |
| **Memory Allocation** | Dynamic heap `malloc` / `new` per trade event | Zero allocations (pre-allocated 1M order pool) |
| **Memory Alignment** | 40 bytes, unaligned, splits across cache lines | 64 bytes (`alignas(64)`), exactly 1 L1 cache line |
| **Tail Latency Stability** | Prone to OS heap jitter and hash rehashing | Flat, deterministic, sub-microsecond p99.9 latency |

---

## 📁 Repository Structure

```text
Limit-order-Book/
├── CMakeLists.txt                         # Cross-platform CMake C++20 build configuration
├── build.bat                              # Automated 14-step Windows MSVC build & run runner
├── README.md                              # Institutional documentation & benchmark reports
├── src/
│   ├── common/
│   │   ├── Types.hpp                      # Domain types (Price, Quantity, OrderId, Side, Trade, LevelInfo)
│   │   └── Order.hpp                      # Baseline 40-byte unaligned Order struct
│   ├── baseline/
│   │   ├── OrderBookBaseline.hpp          # Baseline book header (std::map + std::list)
│   │   └── OrderBookBaseline.cpp          # Baseline FIFO matching engine implementation
│   └── optimized/
│       ├── OptimizedOrder.hpp             # 64-byte cache-aligned order (alignas(64)) + intrusive links
│       ├── SlabAllocator.hpp              # Zero-allocation contiguous object pool
│       ├── DirectPriceLadder.hpp          # Direct array + 2-level 64-bit occupancy bitmask
│       ├── FlatOrderIndex.hpp             # Zero-allocation open-addressing hash table
│       ├── OrderBookOptimized.hpp         # Phase 2 matching engine header
│       └── OrderBookOptimized.cpp         # Zero-allocation matching engine implementation
├── test/
│   ├── BaselineTests.cpp                  # Baseline functional correctness tests (fills, sweeps, cancels)
│   ├── MemoryLayoutTests.cpp              # Struct offset, padding & cache-line splitting tests
│   ├── SlabAllocatorTests.cpp             # Unit tests for SlabAllocator and FlatOrderIndex
│   └── OptimizedOrderBookTests.cpp        # Full functional parity & 50,000-order churn test suite
└── benchmark/
    ├── BaselineBenchmark.cpp              # Baseline 100,000-order RDTSC latency & throughput harness
    ├── CacheBenchmark.cpp                 # Memory locality, pointer-chasing & prefetcher benchmark
    └── PhaseComparisonBenchmark.cpp       # Side-by-side Phase 1 vs Phase 2 comparative benchmark
```

---

## 🚀 Quick Start & Build Guide

### Prerequisites
* **C++ Compiler**: Modern C++20 compliant compiler (MSVC 2019/2022 v16.10+, Clang 13+, or GCC 11+).
* **CMake**: Version 3.20 or newer (for Linux/macOS).
* **Architecture**: x86-64 CPU supporting RDTSC and bit-scan instructions.

---

### Windows (MSVC)

A comprehensive 14-step batch script automates environment configuration, compilation with `/O2`, unit testing, memory audits, and benchmarks:

```cmd
.\build.bat
```

#### What `build.bat` Executes:
1. `BaselineTests.exe` - Baseline matching engine correctness.
2. `BaselineBenchmark.exe` - Phase 1 throughput and RDTSC latency profile.
3. `MemoryLayoutTests.exe` - Struct padding, offset, and cache-line boundary validation.
4. `CacheBenchmark.exe` - Microbenchmarks comparing vector vs. list, structs vs. pointers, sequential vs. random.
5. `SlabAllocatorTests.exe` - Object pool and open-addressing hash index tests.
6. `OptimizedOrderBookTests.exe` - Phase 2 functional tests and high-volume churn verification.
7. `PhaseComparisonBenchmark.exe` - 100,000-order side-by-side performance race.

---

### Cross-Platform (CMake - Linux / macOS)

```bash
# 1. Generate build files
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release

# 2. Compile all targets
cmake --build . --config Release

# 3. Run all test suites
./BaselineTests
./MemoryLayoutTests
./SlabAllocatorTests
./OptimizedOrderBookTests

# 4. Run benchmarks
./CacheBenchmark
./BaselineBenchmark
./PhaseComparisonBenchmark
```

---

## 💻 API Usage Example

```cpp
#include "OrderBookOptimized.hpp"
#include <iostream>

int main() {
    using namespace lob;

    OrderBookOptimized book;

    // 1. Enter passive limit orders (resting liquidity)
    book.add_order(OptimizedOrder(101, Side::BUY,  15000, 500));  // Buy 500 shares @ $150.00
    book.add_order(OptimizedOrder(102, Side::BUY,  14995, 1200)); // Buy 1200 shares @ $149.95
    book.add_order(OptimizedOrder(103, Side::SELL, 15005, 800));  // Sell 800 shares @ $150.05
    book.add_order(OptimizedOrder(104, Side::SELL, 15010, 2500)); // Sell 2500 shares @ $150.10

    // 2. Query Best Bid and Offer (BBO) in single-digit nanoseconds
    std::cout << "Best Bid: $" << *book.get_best_bid() / 100.0 << "\n";
    std::cout << "Best Ask: $" << *book.get_best_ask() / 100.0 << "\n";
    std::cout << "Spread  : $" << *book.get_spread()   / 100.0 << "\n";

    // 3. Ingest an aggressive crossing order (instant zero-allocation match)
    auto fills = book.add_order(OptimizedOrder(201, Side::BUY, 15005, 300));
    for (const auto& trade : fills) {
        std::cout << "EXECUTION: " << trade.quantity << " shares @ $" 
                  << trade.price / 100.0 << " (Maker #" << trade.maker_order_id 
                  << " vs Taker #" << trade.taker_order_id << ")\n";
    }

    // 4. Cancel or amend resting orders with O(1) index lookup
    book.modify_order(102, 1000); // Decrement quantity while preserving FIFO queue priority
    book.cancel_order(104);       // Remove resting sell order

    // 5. Inspect Market Depth Snapshot
    book.print_book(5);

    return 0;
}
```

---

## 🧪 Testing & Functional Parity Verification

The test harness guarantees strict functional equivalence between Phase 1 and Phase 2:

* **Matching Parity**: Verified with identical trade executions across 100,000 pseudo-random orders.
* **FIFO Priority**: Confirms that orders at the same price execute strictly in arrival order.
* **Order Amendments**: Reducing order quantity preserves time priority; size increases relinquish priority.
* **Edge Conditions**: Tested against multi-level price sweeps, partial fills, book-draining sweeps, and high-frequency cancellation churn (50,000 cycles).

---

## 📜 License & Acknowledgments

This project is open-source under the MIT License. Developed for quantitative engineering research, high-frequency trading matching engine development, and systems programming education.
