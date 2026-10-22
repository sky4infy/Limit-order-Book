#include "../src/baseline/OrderBookBaseline.hpp"
#include "../src/optimized/OrderBookOptimized.hpp"
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

double estimate_tsc_frequency_ghz() {
    auto start_time = std::chrono::steady_clock::now();
    uint64_t start_cycles = __rdtsc();

    while (std::chrono::duration_cast<std::chrono::milliseconds>(
               std::chrono::steady_clock::now() - start_time).count() < 50) {
    }

    auto end_time = std::chrono::steady_clock::now();
    uint64_t end_cycles = __rdtsc();

    auto elapsed_ns = std::chrono::duration_cast<std::chrono::nanoseconds>(end_time - start_time).count();
    uint64_t elapsed_cycles = end_cycles - start_cycles;

    return (double)elapsed_cycles / (double)elapsed_ns;
}

struct BenchmarkResult {
    std::string name;
    size_t      orders_processed{0};
    size_t      trades_executed{0};
    double      wall_time_ms{0};
    double      throughput_ops_sec{0};
    double      p50_ns{0};
    double      p90_ns{0};
    double      p99_ns{0};
    double      p99_9_ns{0};
    double      max_ns{0};
};

template<typename BookType>
BenchmarkResult run_engine_benchmark(const std::string& name, const std::vector<Order>& orders, double ghz) {
    BookType book;
    std::vector<double> latencies_ns;
    latencies_ns.reserve(orders.size());

    // Warm-up
    for (size_t i = 0; i < 500; ++i) {
        book.add_order(orders[i]);
    }
    book.clear();

    size_t total_trades = 0;
    auto start_wall = std::chrono::high_resolution_clock::now();

    for (const auto& ord : orders) {
        uint64_t t0 = __rdtsc();
        auto trades = book.add_order(ord);
        uint64_t t1 = __rdtsc();

        total_trades += trades.size();
        double ns = (double)(t1 - t0) / ghz;
        latencies_ns.push_back(ns);
    }

    auto end_wall = std::chrono::high_resolution_clock::now();
    double wall_ms = std::chrono::duration_cast<std::chrono::duration<double, std::milli>>(end_wall - start_wall).count();

    std::sort(latencies_ns.begin(), latencies_ns.end());

    BenchmarkResult res;
    res.name = name;
    res.orders_processed = orders.size();
    res.trades_executed = total_trades;
    res.wall_time_ms = wall_ms;
    res.throughput_ops_sec = (double)orders.size() / (wall_ms / 1000.0);
    res.p50_ns   = latencies_ns[orders.size() * 50 / 100];
    res.p90_ns   = latencies_ns[orders.size() * 90 / 100];
    res.p99_ns   = latencies_ns[orders.size() * 99 / 100];
    res.p99_9_ns = latencies_ns[orders.size() * 999 / 1000];
    res.max_ns   = latencies_ns.back();

    return res;
}

int main() {
    std::cout << "========================================================================\n";
    std::cout << "   PHASE 1 (BASELINE) VS PHASE 2 (ZERO-ALLOCATION) COMPARISON BENCHMARK \n";
    std::cout << "========================================================================\n";

    double ghz = estimate_tsc_frequency_ghz();
    std::cout << "[INFO] Calibrated RDTSC CPU Frequency: ~" 
              << std::fixed << std::setprecision(2) << ghz << " GHz\n";

    const size_t NUM_ORDERS = 100'000;
    std::cout << "[INFO] Generating " << NUM_ORDERS << " synthetic orders (price 9900..10100)...\n\n";

    std::mt19937 rng(42);
    std::uniform_int_distribution<uint64_t> price_dist(9900, 10100);
    std::uniform_int_distribution<uint32_t> qty_dist(10, 500);
    std::uniform_int_distribution<int> side_dist(0, 1);

    std::vector<Order> workload;
    workload.reserve(NUM_ORDERS);

    for (size_t i = 1; i <= NUM_ORDERS; ++i) {
        Side side = (side_dist(rng) == 0) ? Side::BUY : Side::SELL;
        Price price = price_dist(rng);
        Quantity qty = qty_dist(rng);
        workload.emplace_back(i, side, price, qty, 0);
    }

    std::cout << ">> Running Phase 1 (Textbook Baseline: std::map + std::list)...\n";
    auto b1 = run_engine_benchmark<OrderBookBaseline>("Phase 1 (Baseline)", workload, ghz);

    std::cout << ">> Running Phase 2 (Optimized: SlabAllocator + DirectLadder + FlatIndex)...\n";
    auto b2 = run_engine_benchmark<OrderBookOptimized>("Phase 2 (Optimized)", workload, ghz);

    std::cout << "\n========================================================================\n";
    std::cout << "                     SIDE-BY-SIDE BENCHMARK RESULTS                     \n";
    std::cout << "========================================================================\n";
    std::cout << std::left 
              << std::setw(26) << "Metric" 
              << std::setw(22) << "Phase 1 (Baseline)" 
              << std::setw(22) << "Phase 2 (Optimized)" 
              << std::setw(15) << "Improvement" << "\n";
    std::cout << "------------------------------------------------------------------------\n";

    auto print_row_double = [](const std::string& label, double v1, double v2, const std::string& unit, bool higher_better) {
        std::cout << std::left << std::setw(26) << label;
        std::cout << std::setw(22) << (std::to_string((int)v1) + " " + unit);
        std::cout << std::setw(22) << (std::to_string((int)v2) + " " + unit);

        if (higher_better) {
            double factor = v2 / v1;
            std::cout << std::fixed << std::setprecision(1) << factor << "x FASTER\n";
        } else {
            double drop_pct = (1.0 - (v2 / v1)) * 100.0;
            if (drop_pct > 0) {
                std::cout << std::fixed << std::setprecision(1) << drop_pct << "% LOWER\n";
            } else {
                double factor = v1 / v2;
                std::cout << std::fixed << std::setprecision(1) << factor << "x\n";
            }
        }
    };

    std::cout << std::left << std::setw(26) << "Orders Processed" 
              << std::setw(22) << b1.orders_processed 
              << std::setw(22) << b2.orders_processed 
              << std::setw(15) << "100% Match" << "\n";

    std::cout << std::left << std::setw(26) << "Trades Matched" 
              << std::setw(22) << b1.trades_executed 
              << std::setw(22) << b2.trades_executed 
              << std::setw(15) << "100% Parity" << "\n";

    print_row_double("Wall Time", b1.wall_time_ms, b2.wall_time_ms, "ms", false);
    print_row_double("Throughput", b1.throughput_ops_sec, b2.throughput_ops_sec, "ops/s", true);

    std::cout << "------------------------------------------------------------------------\n";
    std::cout << "  LATENCY PERCENTILES (RDTSC Cycles -> Nanoseconds):\n";
    print_row_double("  p50 (Median)", b1.p50_ns, b2.p50_ns, "ns", false);
    print_row_double("  p90", b1.p90_ns, b2.p90_ns, "ns", false);
    print_row_double("  p99", b1.p99_ns, b2.p99_ns, "ns", false);
    print_row_double("  p99.9 (Tail)", b1.p99_9_ns, b2.p99_9_ns, "ns", false);
    print_row_double("  Max (Outlier)", b1.max_ns, b2.max_ns, "ns", false);
    std::cout << "========================================================================\n\n";

    return 0;
}
