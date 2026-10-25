#include <iostream>
#include <vector>
#include <chrono>
#include <thread>
#include <random>
#include <iomanip>
#include "../src/microstructure/MicroPrice.hpp"
#include "../src/microstructure/VpinCalculator.hpp"
#include "../src/microstructure/AvellanedaStoikovBot.hpp"
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

    constexpr size_t NUM_SAMPLES = 1000000;
    std::cout << "\n================================================================================================\n";
    std::cout << "      WEEK 8: MICROSTRUCTURE SIGNAL & STRATEGY EXECUTION BENCHMARK (" << NUM_SAMPLES << " EVALS)      \n";
    std::cout << "================================================================================================\n";

    // Setup synthetic data
    std::mt19937_64 rng(1337);
    std::uniform_int_distribution<uint32_t> price_dist(9900, 10100);
    std::uniform_int_distribution<uint32_t> qty_dist(10, 500);

    std::vector<Price> test_bids(NUM_SAMPLES);
    std::vector<Price> test_asks(NUM_SAMPLES);
    std::vector<Quantity> test_bq(NUM_SAMPLES);
    std::vector<Quantity> test_aq(NUM_SAMPLES);

    for (size_t i = 0; i < NUM_SAMPLES; ++i) {
        test_bids[i] = price_dist(rng);
        test_asks[i] = test_bids[i] + 1; // 1-tick spread
        test_bq[i] = qty_dist(rng);
        test_aq[i] = qty_dist(rng);
    }

    HdrHistogram mp_hist;
    HdrHistogram vpin_hist;
    HdrHistogram as_hist;

    // 1. Benchmark Micro-Price Estimator
    volatile double sink_mp = 0.0;
    uint64_t t_mp_start = rdtsc_fenced();
    for (size_t i = 0; i < NUM_SAMPLES; ++i) {
        uint64_t t0 = rdtsc_fenced();
        double mp = MicroPriceEstimator::calculate_tob_micro_price(test_bids[i], test_bq[i], test_asks[i], test_aq[i]);
        uint64_t t1 = rdtsc_fenced();
        sink_mp += mp;

        uint64_t ns = static_cast<uint64_t>(static_cast<double>(t1 - t0) / ghz);
        mp_hist.record(ns > 0 ? ns : 1);
    }
    uint64_t t_mp_end = rdtsc_fenced();

    // 2. Benchmark VPIN Rolling Calculator
    VpinCalculator vpin(1000, 50);
    volatile double sink_vpin = 0.0;
    uint64_t t_vpin_start = rdtsc_fenced();
    for (size_t i = 0; i < NUM_SAMPLES; ++i) {
        uint64_t t0 = rdtsc_fenced();
        vpin.on_trade(test_bids[i], test_bq[i]);
        double v = vpin.calculate_vpin();
        uint64_t t1 = rdtsc_fenced();
        sink_vpin += v;

        uint64_t ns = static_cast<uint64_t>(static_cast<double>(t1 - t0) / ghz);
        vpin_hist.record(ns > 0 ? ns : 1);
    }
    uint64_t t_vpin_end = rdtsc_fenced();

    // 3. Benchmark Avellaneda-Stoikov Market Maker Quoting
    AvellanedaStoikovBot bot(0.1, 2.0, 1.5, 100);
    uint64_t t_as_start = rdtsc_fenced();
    for (size_t i = 0; i < NUM_SAMPLES; ++i) {
        double mid = static_cast<double>(test_bids[i]) + 0.5;

        uint64_t t0 = rdtsc_fenced();
        auto quotes = bot.compute_optimal_quotes(mid);
        uint64_t t1 = rdtsc_fenced();

        // Simulate occasional fill to test inventory skew updates
        if (i % 10 == 0) {
            bot.on_bid_filled(quotes.bid_price, 10);
        } else if (i % 10 == 5) {
            bot.on_ask_filled(quotes.ask_price, 10);
        }

        uint64_t ns = static_cast<uint64_t>(static_cast<double>(t1 - t0) / ghz);
        as_hist.record(ns > 0 ? ns : 1);
    }
    uint64_t t_as_end = rdtsc_fenced();

    double mp_wall_ms = (t_mp_end - t_mp_start) / (ghz * 1e6);
    double vpin_wall_ms = (t_vpin_end - t_vpin_start) / (ghz * 1e6);
    double as_wall_ms = (t_as_end - t_as_start) / (ghz * 1e6);

    double mp_throughput = NUM_SAMPLES / (mp_wall_ms / 1000.0);
    double vpin_throughput = NUM_SAMPLES / (vpin_wall_ms / 1000.0);
    double as_throughput = NUM_SAMPLES / (as_wall_ms / 1000.0);

    std::cout << std::left << std::setw(26) << "Metric" 
              << std::setw(22) << "Stoikov Micro-Price" 
              << std::setw(22) << "VPIN Toxicity Calc"
              << std::setw(22) << "Avellaneda-Stoikov" << "\n";
    std::cout << std::string(92, '-') << "\n";
    std::cout << std::setw(26) << "Samples Evaluated" 
              << std::setw(22) << NUM_SAMPLES 
              << std::setw(22) << NUM_SAMPLES 
              << std::setw(22) << NUM_SAMPLES << "\n";
    std::cout << std::setw(26) << "Wall Time (ms)" 
              << std::setw(22) << std::fixed << std::setprecision(2) << mp_wall_ms 
              << std::setw(22) << vpin_wall_ms 
              << std::setw(22) << as_wall_ms << "\n";
    std::cout << std::setw(26) << "Throughput (ops/s)" 
              << std::setw(22) << std::setprecision(0) << mp_throughput 
              << std::setw(22) << vpin_throughput 
              << std::setw(22) << as_throughput << "\n";
    std::cout << std::string(92, '-') << "\n";
    std::cout << "LATENCY PERCENTILES (All in Nanoseconds):\n";
    std::cout << std::setw(26) << "p50 (Median)" 
              << std::setw(22) << (std::to_string(mp_hist.value_at_percentile(50.0)) + " ns")
              << std::setw(22) << (std::to_string(vpin_hist.value_at_percentile(50.0)) + " ns")
              << std::setw(22) << (std::to_string(as_hist.value_at_percentile(50.0)) + " ns") << "\n";
    std::cout << std::setw(26) << "p90" 
              << std::setw(22) << (std::to_string(mp_hist.value_at_percentile(90.0)) + " ns")
              << std::setw(22) << (std::to_string(vpin_hist.value_at_percentile(90.0)) + " ns")
              << std::setw(22) << (std::to_string(as_hist.value_at_percentile(90.0)) + " ns") << "\n";
    std::cout << std::setw(26) << "p99" 
              << std::setw(22) << (std::to_string(mp_hist.value_at_percentile(99.0)) + " ns")
              << std::setw(22) << (std::to_string(vpin_hist.value_at_percentile(99.0)) + " ns")
              << std::setw(22) << (std::to_string(as_hist.value_at_percentile(99.0)) + " ns") << "\n";
    std::cout << std::setw(26) << "p99.9 (Tail)" 
              << std::setw(22) << (std::to_string(mp_hist.value_at_percentile(99.9)) + " ns")
              << std::setw(22) << (std::to_string(vpin_hist.value_at_percentile(99.9)) + " ns")
              << std::setw(22) << (std::to_string(as_hist.value_at_percentile(99.9)) + " ns") << "\n";
    std::cout << std::setw(26) << "Max (Outlier)" 
              << std::setw(22) << (std::to_string(mp_hist.max_value()) + " ns")
              << std::setw(22) << (std::to_string(vpin_hist.max_value()) + " ns")
              << std::setw(22) << (std::to_string(as_hist.max_value()) + " ns") << "\n";
    std::cout << std::string(92, '=') << "\n";

    return 0;
}
