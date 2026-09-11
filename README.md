# Limit Order Book (C++20)

A high-performance Limit Order Book implementation in Modern C++20 designed for electronic trading systems.

---

## 📌 Overview

This project implements a continuous double-auction Limit Order Book (LOB) matching buyers and sellers based on strict **Price-Time Priority (FIFO)**. 

### Core Features
* **FIFO Price-Time Matching:** Ensures orders resting at the same price level are executed in strict chronological order of arrival.
* **Order Management:** Supports Limit Orders, Market crossings (spread execution), partial fills, multi-level sweeps, and order cancellations.
* **Fixed-Point Arithmetic:** Prices are stored as 64-bit unsigned integer ticks (`uint64_t`) to eliminate IEEE 754 floating-point rounding errors and precision drift.
* **Console Depth Visualizer:** Real-time visual ladder displaying the active Bid/Ask spread, price levels, and order depth.
* **Hardware Latency Benchmarking:** Cycle-accurate latency profiler using x86 CPU hardware timers (`__rdtsc`) measuring median and tail latency percentiles (p50, p90, p99, p99.9).

---

## 📁 Repository Structure

```text
Limit-order-Book/
├── src/
│   ├── common/
│   │   ├── Types.hpp          # Domain types (Price, Quantity, OrderId, Side, Trade)
│   │   └── Order.hpp          # Order struct and lifecycle helpers
│   └── baseline/
│       ├── OrderBookBaseline.hpp  # Order book core header
│       └── OrderBookBaseline.cpp  # FIFO matching engine implementation
├── test/
│   └── BaselineTests.cpp      # Correctness unit test suite (fills, sweeps, cancels)
├── benchmark/
│   └── BaselineBenchmark.cpp  # Hardware RDTSC latency & throughput benchmark
├── build.bat                  # One-click Windows MSVC build & run script
└── CMakeLists.txt             # Cross-platform CMake C++20 build configuration
```

---

## 🚀 Quick Start

### Windows (MSVC)
Run the automated build script:
```cmd
.\build.bat
```
This compiles the code with C++20 optimizations (`/O2`), executes the unit test suite, and runs the 100,000-order latency benchmark.

### Linux / macOS (CMake)
```bash
mkdir build && cd build
cmake ..
cmake --build . --config Release
./BaselineTests
./BaselineBenchmark
```
