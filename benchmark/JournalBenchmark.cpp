#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include <random>
#include <iomanip>
#include <filesystem>
#include "../src/persistence/MemoryMappedJournal.hpp"
#include "../src/optimized/OrderBookOptimized.hpp"
#include "../src/visualization/OrderBookVisualizer.hpp"
#include "../src/common/HdrHistogram.hpp"

#if defined(_MSC_VER)
#include <intrin.h>
#else
#include <x86intrin.h>
#endif

using namespace lob;

static inline uint64_t rdtsc_fenced() {
#if defined(_MSC_VER)
    _mm_lfence();
    return __rdtsc();
#else
    asm volatile("lfence" ::: "memory");
    return __rdtsc();
#endif
}

static double estimate_tsc_ghz() {
    auto t0 = std::chrono::high_resolution_clock::now();
    uint64_t c0 = rdtsc_fenced();
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    auto t1 = std::chrono::high_resolution_clock::now();
    uint64_t c1 = rdtsc_fenced();
    double ns = static_cast<double>(std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count());
    return static_cast<double>(c1 - c0) / ns;
}

int main() {
    double ghz = estimate_tsc_ghz();
    std::cout << "Calibrated Invariant TSC Frequency: " << std::fixed << std::setprecision(3) << ghz << " GHz\n";

    constexpr size_t NUM_RECORDS = 1000000;
    std::string bench_file = "bench_journal.bin";
    if (std::filesystem::exists(bench_file)) std::filesystem::remove(bench_file);

    std::cout << "\n================================================================================================\n";
    std::cout << "   BENCHMARK 1: MEMORY-MAPPED TRANSACTION JOURNAL WRITE LATENCY (" << NUM_RECORDS << " WRITES)   \n";
    std::cout << "================================================================================================\n";

    HdrHistogram write_hist;
    size_t journal_capacity = NUM_RECORDS * sizeof(JournalRecord) + (4 * 1024 * 1024);

    uint64_t write_start = rdtsc_fenced();
    {
        MemoryMappedJournal journal(bench_file, journal_capacity);

        for (uint64_t i = 1; i <= NUM_RECORDS; ++i) {
            Side s = (i % 2 == 0) ? Side::BUY : Side::SELL;
            Price p = 10000 + (i % 100);
            Quantity q = 100;

            uint64_t t0 = rdtsc_fenced();
            journal.append(JournalEventType::ORDER_ADD, i * 100, i, 1, s, p, q);
            uint64_t t1 = rdtsc_fenced();

            uint64_t ns = static_cast<uint64_t>(static_cast<double>(t1 - t0) / ghz);
            write_hist.record(ns > 0 ? ns : 1);
        }
        journal.sync();
    }
    uint64_t write_end = rdtsc_fenced();

    double write_wall_ms = (write_end - write_start) / (ghz * 1e6);
    double write_throughput = NUM_RECORDS / (write_wall_ms / 1000.0);
    double mb_written = (NUM_RECORDS * sizeof(JournalRecord)) / (1024.0 * 1024.0);
    double write_mb_per_sec = mb_written / (write_wall_ms / 1000.0);

    std::cout << "Records Appended      : " << NUM_RECORDS << " records (" << std::fixed << std::setprecision(2) << mb_written << " MB)\n";
    std::cout << "Wall Time             : " << write_wall_ms << " ms\n";
    std::cout << "Journal Throughput    : " << std::setprecision(0) << write_throughput << " records/sec (" << std::setprecision(1) << write_mb_per_sec << " MB/s)\n";
    std::cout << "------------------------------------------------------------------------------------------------\n";
    std::cout << "APPEND LATENCY (Nanoseconds):\n";
    std::cout << "  p50 (Median)        : " << write_hist.value_at_percentile(50.0) << " ns\n";
    std::cout << "  p90                 : " << write_hist.value_at_percentile(90.0) << " ns\n";
    std::cout << "  p99                 : " << write_hist.value_at_percentile(99.0) << " ns\n";
    std::cout << "  p99.9 (Tail)        : " << write_hist.value_at_percentile(99.9) << " ns\n";
    std::cout << "  Max (Outlier)       : " << write_hist.max_value() << " ns\n";
    std::cout << "================================================================================================\n";

    // 2. Replay Benchmark
    std::cout << "\n================================================================================================\n";
    std::cout << "   BENCHMARK 2: DETERMINISTIC CRASH REPLAY & STATE RECOVERY (" << NUM_RECORDS << " RECORDS)      \n";
    std::cout << "================================================================================================\n";

    uint64_t replay_start = rdtsc_fenced();
    size_t replayed_count = 0;
    {
        MemoryMappedJournal recovery_journal(bench_file, journal_capacity);
        auto records = recovery_journal.replay_all();
        replayed_count = records.size();

        OrderBookOptimized recovered_book;
        for (const auto& rec : records) {
            recovered_book.add_order(Order(rec.order_id, static_cast<Side>(rec.side), rec.price, rec.quantity, rec.timestamp));
        }
    }
    uint64_t replay_end = rdtsc_fenced();

    double replay_wall_ms = (replay_end - replay_start) / (ghz * 1e6);
    double replay_throughput = replayed_count / (replay_wall_ms / 1000.0);

    std::cout << "Records Replayed      : " << replayed_count << " records\n";
    std::cout << "Replay Wall Time      : " << std::fixed << std::setprecision(2) << replay_wall_ms << " ms\n";
    std::cout << "Recovery Speed        : " << std::setprecision(0) << replay_throughput << " records/sec\n";
    std::cout << "================================================================================================\n";

    // 3. Live Level 3 Terminal Visualization Demo
    std::cout << "\n================================================================================================\n";
    std::cout << "   DEMO: INSTITUTIONAL LEVEL 3 TERMINAL DEPTH VISUALIZER WITH REAL-TIME MICRO-PRICE & VPIN      \n";
    std::cout << "================================================================================================\n";

    std::vector<DepthLevel> demo_bids = {
        {10050, 4500, 12},
        {10049, 3200, 8},
        {10048, 8900, 24},
        {10047, 12000, 35},
        {10046, 6700, 19},
        {10045, 15400, 42},
        {10044, 9100, 28},
        {10043, 4300, 11},
        {10042, 2100, 5},
        {10041, 1100, 3}
    };

    std::vector<DepthLevel> demo_asks = {
        {10051, 1500, 4},
        {10052, 2800, 7},
        {10053, 5400, 15},
        {10054, 7200, 21},
        {10055, 11000, 31},
        {10056, 4200, 12},
        {10057, 8500, 23},
        {10058, 6300, 17},
        {10059, 3100, 9},
        {10060, 1800, 6}
    };

    OrderBookVisualizer::render_l3_dashboard(
        std::cout,
        "NVDA (NASDAQ)",
        demo_bids,
        demo_asks,
        0.285, // Low VPIN
        158420,
        42310,
        1000000
    );

    if (std::filesystem::exists(bench_file)) std::filesystem::remove(bench_file);

    return 0;
}
