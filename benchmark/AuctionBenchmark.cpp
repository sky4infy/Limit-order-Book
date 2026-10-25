#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include <random>
#include <algorithm>
#include <iomanip>
#include "../src/exchange/ExchangeTypes.hpp"
#include "../src/exchange/CallAuction.hpp"
#include "../src/exchange/ProRataMatching.hpp"
#include "../src/exchange/AdvancedOrders.hpp"
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
    double ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
    return static_cast<double>(c1 - c0) / ns;
}

void benchmark_call_auction(double ghz) {
    std::cout << "\n======================================================================\n";
    std::cout << "  BENCHMARK 1: WALRASIAN CALL AUCTION CLEARING (10,000 ORDERS CROSS)   \n";
    std::cout << "======================================================================\n";

    constexpr size_t NUM_ORDERS = 10000;
    std::mt19937_64 rng(1337);
    std::normal_distribution<double> price_dist(10000.0, 50.0); // Mean 100.00, stddev 0.50
    std::uniform_int_distribution<uint32_t> qty_dist(10, 500);

    CallAuctionEngine auction(10000);

    // Generate 10,000 synthetic pre-market orders
    for (size_t i = 0; i < NUM_ORDERS; ++i) {
        Side side = (rng() % 2 == 0) ? Side::BUY : Side::SELL;
        Price p = static_cast<Price>(std::clamp(price_dist(rng), 9800.0, 10200.0));
        Quantity q = qty_dist(rng);
        bool is_moo = (rng() % 20 == 0); // 5% MOO orders
        auction.add_order(i + 1, static_cast<uint32_t>((i % 50) + 1), side, p, q, i * 100, is_moo);
    }

    // Benchmark Clearing Price Calculation + Execution
    AuctionResult result;
    uint64_t start_cycles = rdtsc_fenced();
    auto fills = auction.execute_uncross(result);
    uint64_t end_cycles = rdtsc_fenced();

    double elapsed_ns = static_cast<double>(end_cycles - start_cycles) / ghz;
    double elapsed_ms = elapsed_ns / 1e6;

    std::cout << "Clearing Price Discovered : " << result.clearing_price << " (" << std::fixed << std::setprecision(2) << (result.clearing_price / 100.0) << ")\n";
    std::cout << "Total Volume Matched      : " << result.matched_volume << " shares across " << fills.size() << " trades\n";
    std::cout << "Remaining Imbalance       : " << (result.imbalance_side == Side::BUY ? result.buy_surplus : result.sell_surplus)
              << " shares (" << (result.imbalance_side == Side::BUY ? "BUY Surplus" : "SELL Surplus") << ")\n";
    std::cout << "Uncrossing Wall Time      : " << elapsed_ms << " ms (" << elapsed_ns << " ns)\n";
    std::cout << "Cross Calculation Latency : " << std::fixed << std::setprecision(1) << (elapsed_ns / NUM_ORDERS) << " ns per order evaluated\n";
}

void benchmark_fifo_vs_pro_rata(double ghz) {
    std::cout << "\n======================================================================\n";
    std::cout << "  BENCHMARK 2: FIFO MATCHING VS CME PRO-RATA ALLOCATION (100,000 RUNS) \n";
    std::cout << "======================================================================\n";

    constexpr size_t ITERATIONS = 100000;
    HdrHistogram fifo_hist;
    HdrHistogram prorata_hist;

    std::mt19937_64 rng(42);
    std::uniform_int_distribution<uint32_t> qty_dist(50, 1000);

    // Warm-up and generate test cases
    std::vector<std::vector<ProRataRestingOrder>> test_books(ITERATIONS);
    std::vector<Quantity> test_aggressors(ITERATIONS);

    for (size_t i = 0; i < ITERATIONS; ++i) {
        test_books[i].reserve(10);
        for (uint64_t j = 0; j < 10; ++j) {
            Quantity q = qty_dist(rng);
            test_books[i].push_back({j + 1, static_cast<uint32_t>(j + 1), q, q, j * 100});
        }
        test_aggressors[i] = qty_dist(rng) * 3; // Aggressive order matching multiple resting orders
    }

    // Benchmark FIFO
    uint64_t fifo_start = rdtsc_fenced();
    for (size_t i = 0; i < ITERATIONS; ++i) {
        auto book = test_books[i];
        Quantity aggressive = test_aggressors[i];

        uint64_t t0 = rdtsc_fenced();
        // Sequential FIFO matching
        for (auto& o : book) {
            Quantity fill = std::min(o.remaining_quantity, aggressive);
            o.remaining_quantity -= fill;
            aggressive -= fill;
            if (aggressive == 0) break;
        }
        uint64_t t1 = rdtsc_fenced();

        uint64_t ns = static_cast<uint64_t>(static_cast<double>(t1 - t0) / ghz);
        fifo_hist.record(ns > 0 ? ns : 1);
    }
    uint64_t fifo_end = rdtsc_fenced();

    // Benchmark CME Pure Pro-Rata
    uint64_t pr_start = rdtsc_fenced();
    for (size_t i = 0; i < ITERATIONS; ++i) {
        auto book = test_books[i];
        Quantity aggressive = test_aggressors[i];

        uint64_t t0 = rdtsc_fenced();
        auto alloc = ProRataAllocationEngine::allocate_pure_pro_rata(book, aggressive);
        uint64_t t1 = rdtsc_fenced();

        uint64_t ns = static_cast<uint64_t>(static_cast<double>(t1 - t0) / ghz);
        prorata_hist.record(ns > 0 ? ns : 1);
    }
    uint64_t pr_end = rdtsc_fenced();

    double fifo_wall_ms = (fifo_end - fifo_start) / (ghz * 1e6);
    double pr_wall_ms = (pr_end - pr_start) / (ghz * 1e6);

    double fifo_throughput = (ITERATIONS / (fifo_wall_ms / 1000.0));
    double pr_throughput = (ITERATIONS / (pr_wall_ms / 1000.0));

    std::cout << std::left << std::setw(26) << "Metric" 
              << std::setw(22) << "FIFO Priority" 
              << std::setw(22) << "CME Pro-Rata" << "\n";
    std::cout << std::string(70, '-') << "\n";
    std::cout << std::setw(26) << "Iterations" << std::setw(22) << ITERATIONS << std::setw(22) << ITERATIONS << "\n";
    std::cout << std::setw(26) << "Wall Time (ms)" << std::setw(22) << std::fixed << std::setprecision(2) << fifo_wall_ms << std::setw(22) << pr_wall_ms << "\n";
    std::cout << std::setw(26) << "Throughput (ops/s)" << std::setw(22) << std::setprecision(0) << fifo_throughput << std::setw(22) << pr_throughput << "\n";
    std::cout << std::string(70, '-') << "\n";
    std::cout << "LATENCY (Nanoseconds):\n";
    std::cout << std::setw(26) << "p50 (Median)" << std::setw(22) << (std::to_string(fifo_hist.value_at_percentile(50.0)) + " ns") << std::setw(22) << (std::to_string(prorata_hist.value_at_percentile(50.0)) + " ns") << "\n";
    std::cout << std::setw(26) << "p90" << std::setw(22) << (std::to_string(fifo_hist.value_at_percentile(90.0)) + " ns") << std::setw(22) << (std::to_string(prorata_hist.value_at_percentile(90.0)) + " ns") << "\n";
    std::cout << std::setw(26) << "p99" << std::setw(22) << (std::to_string(fifo_hist.value_at_percentile(99.0)) + " ns") << std::setw(22) << (std::to_string(prorata_hist.value_at_percentile(99.0)) + " ns") << "\n";
    std::cout << std::setw(26) << "p99.9 (Tail)" << std::setw(22) << (std::to_string(fifo_hist.value_at_percentile(99.9)) + " ns") << std::setw(22) << (std::to_string(prorata_hist.value_at_percentile(99.9)) + " ns") << "\n";
    std::cout << std::setw(26) << "Max (Outlier)" << std::setw(22) << (std::to_string(fifo_hist.max_value()) + " ns") << std::setw(22) << (std::to_string(prorata_hist.max_value()) + " ns") << "\n";
    std::cout << std::string(70, '=') << "\n";
}

int main() {
    double ghz = estimate_tsc_ghz();
    std::cout << "Calibrated Invariant TSC Frequency: " << std::fixed << std::setprecision(3) << ghz << " GHz\n";

    benchmark_call_auction(ghz);
    benchmark_fifo_vs_pro_rata(ghz);

    return 0;
}
