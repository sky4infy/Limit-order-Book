# Week 4: Latency Profiling, Hardware Timestamping & Coordinated Omission
## Eliminating Measurement Bias, Tracking True Tail Distributions, and Mastering HDR Histograms

---

## 1. Executive Summary: Why Averages Lie in Low-Latency Engineering

In electronic trading and high-frequency matching engines, **mean latency and standard deviation are dangerous illusions**:
1. **Trading Latency is Non-Gaussian (Multimodal)**: In textbook statistics, distributions are assumed to follow a Bell Curve (Normal Distribution). In computer hardware, latency follows an extreme power-law distribution with multiple distinct modes corresponding to physical hardware boundaries:
   - **L1 Cache Hit**: $\sim 1\text{ ns}$ (Mode 1)
   - **L3 Cache Miss / DRAM Access**: $\sim 60\text{ to }100\text{ ns}$ (Mode 2)
   - **Kernel System Call / Context Switch**: $\sim 1,500\text{ to }5,000\text{ ns}$ (Mode 3)
   - **OS Page Fault / Memory Allocation Lock**: $\sim 50,000\text{ to }1,000,000\text{ ns}$ (Mode 4)
2. **Standard Deviation is Meaningless**: Reporting "$\text{Mean} \pm 2\sigma$" assumes symmetry. When 99% of orders take 50ns and 1% take 5ms, the standard deviation is huge, but it gives zero actionable insight into the shape of the tail.
3. **The p99 and p99.9 Reality**: In market making, being 200 nanoseconds slow on the 99.9th percentile order means your stale quote is filled by an arbitrageur during a market crash. The tail is where all the risk and money live.

```
       TYPICAL CLOSED-LOOP BENCHMARK                     REALITY (COORDINATED OMISSION)
 ┌──────────────────────────────────────────┐      ┌──────────────────────────────────────────┐
 │ • Client sends Order 1 -> Waits for LOB  │      │ • Orders arrive at market rate from wire │
 │ • Order 2 stalls for 1 millisecond       │ ───► │ • During 1ms stall, 5,000 orders backlog │
 │ • Client PAUSES and sends no orders!     │      │ • Backlogged orders wait 1µs..1000µs     │
 │ • Reported p99: "Fast!" (Hides the stall)│      │ • Real p99: DISASTER (Severe queue blow) │
 └──────────────────────────────────────────┘      └──────────────────────────────────────────┘
```

---

## 2. Gil Tene's Coordinated Omission Explained

### The Doctor's Waiting Room Analogy
Imagine a doctor's clinic where patients are scheduled to arrive **every 10 minutes**:
- Patient 1 arrives at 9:00 AM, sees the doctor for 10 minutes, and leaves at 9:10 AM. (Wait time: 0 min).
- Patient 2 arrives at 9:10 AM. The doctor unexpectedly gets stuck on a medical emergency call that lasts **2 hours** (until 11:10 AM).
- If the clinic receptionist measures latency by only checking patients who walk into the doctor's room:
  - Patient 1: 10 minutes.
  - Patient 2: 120 minutes.
  - Naive average: $\frac{10 + 120}{2} = 65\text{ minutes}$.
  - The receptionist says: *"Only 2 patients were seen, so only 1 patient suffered a delay!"*

**What happened to Patients 3 through 14?**
They arrived at 9:20, 9:30, 9:40, 9:50, 10:00... and were forced to sit in the waiting room!
- Patient 3 waited 110 minutes!
- Patient 4 waited 100 minutes!
- Patient 12 waited 20 minutes!

**Coordinated Omission occurs when your benchmark coordinates its sending schedule with the system under test.** When the system stalls, the benchmark client stalls too, thereby **omitting** all the requests that would have arrived and suffered queueing delay during that pause.

### The Mathematical Formulation:
In an open-loop arrival schedule with scheduled arrival times $T_{\text{scheduled}}^{(i)}$ and target interval $\Delta t$:
$$\text{Queue Wait Time: } W_i = \max\left(0, T_{\text{actual}}^{(i)} - T_{\text{scheduled}}^{(i)}\right)$$
$$\text{Service Time: } S_i = T_{\text{complete}}^{(i)} - T_{\text{actual}}^{(i)}$$
$$\text{Total Experienced Latency: } L_i = S_i + W_i = T_{\text{complete}}^{(i)} - T_{\text{scheduled}}^{(i)}$$

### Gil Tene's Backfilling Algorithm:
When a service request takes duration $T > \Delta t$, it effectively held up $\lfloor T / \Delta t \rfloor$ subsequent requests. In [src/common/HdrHistogram.hpp](file:///d:/Limit%20Order%20Book/src/common/HdrHistogram.hpp), we implement this via `record_with_expected_interval()`:
```cpp
void record_with_expected_interval(uint64_t value, uint64_t expected_interval) noexcept {
    record(value);
    if (expected_interval == 0 || value <= expected_interval) return;

    uint64_t missing_value = value - expected_interval;
    while (missing_value > 0) {
        record(missing_value);
        if (missing_value <= expected_interval) break;
        missing_value -= expected_interval;
    }
}
```

---

## 3. High Dynamic Range (HDR) Histogram Architecture

Tracking percentiles from $1\text{ ns}$ to $1\text{ hour}$ ($3.6 \times 10^{12}\text{ ns}$) cannot be done by storing every timestamp in a `std::vector<double>`:
- Storing $100,000,000$ order timestamps requires **800 MB of RAM** and requires $O(N \log N)$ sorting, polluting CPU cache and skewing the benchmark itself.
- A standard linear histogram with 1ns bins would require an array of **3.6 trillion entries** (unusable).

### How HdrHistogram Solves This in Sub-Microsecond Hardware Time:
1. **Logarithmic Bucketing with Linear Sub-Buckets**:
   - The value range is split into powers-of-two buckets (magnitude ranges).
   - Within each bucket, values are divided into a fixed number of linear sub-buckets (e.g. 1024 or 2048), guaranteeing a constant relative precision (e.g. 3 significant figures, or $< 0.1\%$ error).
2. **Single-Instruction Indexing via `LZCNT` / `std::countl_zero`**:
   - Determining which bucket a 64-bit value falls into is simply counting leading zero bits:
   ```cpp
   uint32_t bits = 64 - std::countl_zero(value); // Translates to x86 LZCNT instruction!
   ```
   - Zero branching, zero memory allocation, and zero locks on the hot recording path!

---

## 4. Hardware Timestamping Physics: `__rdtsc` vs Speculative Execution

The x86 `__rdtsc` instruction reads the CPU Time Stamp Counter (TSC). However, using `__rdtsc` naively in modern out-of-order execution (OoO) processors is flawed:

### The Pitfall: Speculative Instruction Reordering
Modern superscalar processors (Intel Alder Lake / AMD Zen) execute instructions out-of-order. If you write:
```cpp
uint64_t t0 = __rdtsc();
book.add_order(ord);
uint64_t t1 = __rdtsc();
```
The CPU's out-of-order execution engine may schedule `t1` **before** `book.add_order(ord)` has retired its store instructions! You end up measuring a duration smaller than physical reality.

### The Solution: Pipeline Serialization (`_mm_lfence()`)
By inserting a load fence instruction (`LFENCE`) before reading the TSC, we force the CPU execution pipeline to retire all preceding instructions before sampling the clock:
```cpp
inline uint64_t rdtsc_fenced() noexcept {
#ifdef _MSC_VER
    _mm_lfence();
    return __rdtsc();
#else
    asm volatile("lfence" ::: "memory");
    return __rdtsc();
#endif
}
```

---

## 5. Empirical Benchmark Results: Phase 1 vs Phase 2 Under Open-Loop Load

From our dedicated benchmark harness [benchmark/CoordinatedOmissionBenchmark.cpp](file:///d:/Limit%20Order%20Book/benchmark/CoordinatedOmissionBenchmark.cpp) running 100,000 synthetic orders with an open-loop arrival schedule (target: 5M orders/sec, 200ns expected interval):

| Metric | Phase 1 Naive (Closed-Loop) | Phase 1 Corrected (Open-Loop) | Phase 2 Naive (Closed-Loop) | Phase 2 Corrected (Open-Loop) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Recorded Samples** | 100,000 | **92,092,218** (Queue Blowout!) | 100,000 | **119,910** (Stable Queue) |
| **Wall Time** | 22.2 ms | - | 15.2 ms | - |
| **Throughput** | 4.50M ops/s | - | 6.59M ops/s | - |
| **p50 (Median)** | 156 ns | **319,231 ns (319 µs)** | 117 ns | **100 ns** |
| **p90** | 291 ns | **1,065,983 ns (1.06 ms)** | 197 ns | **304 ns** |
| **p99** | 581 ns | **1,509,375 ns (1.51 ms)** | 350 ns | **3,173 ns (3.1 µs)** |
| **p99.9 (Tail)** | 1,151 ns | **1,670,143 ns (1.67 ms)** | 518 ns | **5,695 ns (5.7 µs)** |
| **Max (Outlier)** | 323,094 ns | **1,735,121 ns (1.74 ms)** | 28,586 ns | **11,022 ns (11.0 µs)** |

### Architectural Takeaways:
1. **The Closed-Loop Mirage**: In Phase 1 Naive, p99.9 was reported as $1,151\text{ ns}$ (barely 1.1 µs). But under open-loop load with Coordinated Omission corrected, the true p99.9 was **$1,670,143\text{ ns}$ (1.67 MILLISECONDS)**! The closed-loop benchmark hid a **1,450x latency spike**!
2. **Phase 2 Zero-Allocation Resilience**: Phase 2's pre-allocated `SlabAllocator` and $O(1)$ `DirectPriceLadder` prevented kernel heap lock contention. Even under open-loop market pressure, its corrected p99.9 stayed strictly at **5.7 microseconds**, and its corrected median was **100 nanoseconds**.
