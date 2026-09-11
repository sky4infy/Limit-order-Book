#include "../src/baseline/OrderBookBaseline.hpp"
#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>
#include <iomanip>

#ifdef _MSC_VER
#include <intrin.h>
#else
#include <x86intrin.h>
#endif

using namespace lob;

// Estimate CPU frequency to convert RDTSC cycles to nanoseconds
double estimate_tsc_frequency_ghz() {
    auto start_time = std::chrono::steady_clock::now();
    uint64_t start_cycles = __rdtsc();

    // Busy wait for ~50 milliseconds
    while (std::chrono::duration_cast<std::chrono::milliseconds>(
               std::chrono::steady_clock::now() - start_time).count() < 50) {
        // spin
    }

    auto end_time = std::chrono::steady_clock::now();
    uint64_t end_cycles = __rdtsc();

    auto elapsed_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count();
    uint64_t elapsed_cycles = end_cycles - start_cycles;

    return (double)elapsed_cycles / (double)elapsed_ns; // cycles per nanosecond (GHz)
}

int main() {
    std::cout << "========================================================\n";
    std::cout << "  WEEK 1: BASELINE LATENCY & THROUGHPUT BENCHMARK       \n";
    std::cout << "========================================================\n";

    double ghz = estimate_tsc_frequency_ghz();
    std::cout << "[INFO] Calibrating RDTSC... CPU Frequency: ~" 
              << std::fixed << std::setprecision(2) << ghz << " GHz\n";

    const size_t NUM_ORDERS = 100000;
    std::cout << "[INFO] Generating " << NUM_ORDERS << " synthetic order workload...\n";

    // Seeded generator for reproducible benchmarks
    std::mt19937 rng(42);
    std::uniform_int_distribution<uint64_t> price_dist(9900, 10100); // $99.00 to $101.00
    std::uniform_int_distribution<uint32_t> qty_dist(10, 500);
    std::uniform_int_distribution<int> side_dist(0, 1);

    // Pre-generate orders in memory so random generation is not counted in matching latency
    std::vector<Order> test_orders;
    test_orders.reserve(NUM_ORDERS);

    for (size_t i = 1; i <= NUM_ORDERS; ++i) {
        Side side = (side_dist(rng) == 0) ? Side::BUY : Side::SELL;
        Price price = price_dist(rng);
        Quantity qty = qty_dist(rng);
        test_orders.emplace_back(i, side, price, qty, 0);
    }

    std::cout << "[INFO] Warming up cache and running benchmark...\n";
    OrderBookBaseline book;
    std::vector<double> latencies_ns;
    latencies_ns.reserve(NUM_ORDERS);

    size_t total_trades_executed = 0;

    auto benchmark_start = std::chrono::high_resolution_clock::now();

    for (const auto& ord : test_orders) {
        uint64_t t0 = __rdtsc();
        auto trades = book.add_order(ord);
        uint64_t t1 = __rdtsc();

        total_trades_executed += trades.size();

        double elapsed_ns = (double)(t1 - t0) / ghz;
        latencies_ns.push_back(elapsed_ns);
    }

    auto benchmark_end = std::chrono::high_resolution_clock::now();
    auto total_duration_ms = std::chrono::duration_cast<std::chrono::milliseconds>(benchmark_end - benchmark_start).count();

    // Sort latencies to compute percentiles
    std::sort(latencies_ns.begin(), latencies_ns.end());

    double p50 = latencies_ns[size_t(NUM_ORDERS * 0.50)];
    double p90 = latencies_ns[size_t(NUM_ORDERS * 0.90)];
    double p99 = latencies_ns[size_t(NUM_ORDERS * 0.99)];
    double p999 = latencies_ns[size_t(NUM_ORDERS * 0.999)];
    double max_lat = latencies_ns.back();

    double throughput = (double)NUM_ORDERS / ((double)total_duration_ms / 1000.0);

    std::cout << "\n------------------ BENCHMARK RESULTS ------------------\n";
    std::cout << "  Orders Processed : " << NUM_ORDERS << "\n";
    std::cout << "  Trades Executed  : " << total_trades_executed << "\n";
    std::cout << "  Total Wall Time  : " << total_duration_ms << " ms\n";
    std::cout << "  Throughput       : " << std::fixed << std::setprecision(0) << throughput << " orders/sec\n";
    std::cout << "--------------------------------------------------------\n";
    std::cout << "  LATENCY PERCENTILES (Nanoseconds / Microseconds):     \n";
    std::cout << "    p50 (Median)   : " << std::setw(8) << std::fixed << std::setprecision(1) << p50 << " ns (" << p50 / 1000.0 << " us)\n";
    std::cout << "    p90            : " << std::setw(8) << std::fixed << std::setprecision(1) << p90 << " ns (" << p90 / 1000.0 << " us)\n";
    std::cout << "    p99            : " << std::setw(8) << std::fixed << std::setprecision(1) << p99 << " ns (" << p99 / 1000.0 << " us)\n";
    std::cout << "    p99.9          : " << std::setw(8) << std::fixed << std::setprecision(1) << p999 << " ns (" << p999 / 1000.0 << " us)\n";
    std::cout << "    Max (Outlier)  : " << std::setw(8) << std::fixed << std::setprecision(1) << max_lat << " ns (" << max_lat / 1000.0 << " us)\n";
    std::cout << "========================================================\n\n";

    std::cout << ">>> INTERVIEW TAKEAWAY:\n";
    std::cout << "Notice how the p99/p99.9 latencies spike significantly above p50!\n";
    std::cout << "In Phase 2, we will replace std::map and std::list with a Slab Allocator\n";
    std::cout << "and Direct Array to eliminate heap jitter and crush this tail latency.\n\n";

    return 0;
}
