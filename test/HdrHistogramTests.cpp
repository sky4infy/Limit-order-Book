#include "../src/common/HdrHistogram.hpp"
#include <iostream>
#include <cassert>
#include <cmath>
#include <vector>

using namespace lob;

void test_basic_recording_and_percentiles() {
    std::cout << "[TEST] Running test_basic_recording_and_percentiles..." << std::endl;

    HdrHistogram hist(10'000'000, 3); // Track up to 10ms with 3 sig figs

    // Record values 1 through 100,000 (uniform distribution)
    const uint64_t N = 100'000;
    for (uint64_t v = 1; v <= N; ++v) {
        hist.record(v);
    }

    assert(hist.total_count() == N);
    assert(hist.min_value() == 1);
    assert(hist.max_value() == N);

    // Mean of 1..N is (N+1)/2 = 50,000.5
    double expected_mean = (N + 1.0) / 2.0;
    assert(std::abs(hist.mean() - expected_mean) < expected_mean * 0.01); // within 1%

    // Check percentiles within 0.5% resolution
    uint64_t p50 = hist.value_at_percentile(50.0);
    uint64_t p90 = hist.value_at_percentile(90.0);
    uint64_t p99 = hist.value_at_percentile(99.0);
    uint64_t p99_9 = hist.value_at_percentile(99.9);

    assert(std::abs(static_cast<double>(p50) - 50'000.0) / 50'000.0 < 0.005);
    assert(std::abs(static_cast<double>(p90) - 90'000.0) / 90'000.0 < 0.005);
    assert(std::abs(static_cast<double>(p99) - 99'000.0) / 99'000.0 < 0.005);
    assert(std::abs(static_cast<double>(p99_9) - 99'900.0) / 99'900.0 < 0.005);

    std::cout << "  -> PASSED (Uniform percentiles verified to < 0.5% error margin)" << std::endl;
}

void test_coordinated_omission_correction() {
    std::cout << "[TEST] Running test_coordinated_omission_correction (Gil Tene Scenario)..." << std::endl;

    // SCENARIO:
    // Workload: 1 order every 100 ns (10,000,000 orders/sec).
    // 99 normal orders complete in 100 ns.
    // 1 order suffers a 10,000 ns stall (e.g. malloc lock or page fault).
    
    // Naive / Closed-Loop Histogram:
    HdrHistogram naive_hist(1'000'000, 3);
    for (int i = 0; i < 99; ++i) {
        naive_hist.record(100);
    }
    naive_hist.record(10'000); // 1 stalled order

    assert(naive_hist.total_count() == 100);
    // In naive measurement, 99 out of 100 orders are 100ns!
    // So p50 is 100ns, p90 is 100ns, p99 is 100ns! The stall is completely hidden!
    assert(naive_hist.value_at_percentile(50.0) <= 105);
    assert(naive_hist.value_at_percentile(90.0) <= 105);
    assert(naive_hist.value_at_percentile(98.0) <= 105);

    // Corrected / Open-Loop Histogram:
    HdrHistogram corrected_hist(1'000'000, 3);
    const uint64_t expected_interval = 100; // 100 ns arrival interval

    for (int i = 0; i < 99; ++i) {
        corrected_hist.record_with_expected_interval(100, expected_interval);
    }
    // The 10,000 ns stall occurred. In reality, 100 arrival intervals were blocked!
    corrected_hist.record_with_expected_interval(10'000, expected_interval);

    // The corrected histogram must account for:
    // 99 fast orders + 1 stalled order + 99 omitted orders in queue = 199 total orders!
    assert(corrected_hist.total_count() == 199);

    // Now, let's observe the reality:
    // 99 orders took 100ns.
    // 100 orders suffered latencies from 100ns to 10,000ns!
    // The 90th percentile should NOT be 100ns anymore—it should reflect the massive queue!
    uint64_t corrected_p90 = corrected_hist.value_at_percentile(90.0);
    assert(corrected_p90 > 7'000); // Exposed the true tail delay!

    std::cout << "  -> PASSED: Coordinated Omission properly backfilled 99 omitted requests!" << std::endl;
    std::cout << "     Naive p90     : " << naive_hist.value_at_percentile(90.0) << " ns (Lies! Shows fast execution)" << std::endl;
    std::cout << "     Corrected p90 : " << corrected_p90 << " ns (True queue wait exposed!)" << std::endl;
}

void test_edge_cases_and_reset() {
    std::cout << "[TEST] Running test_edge_cases_and_reset..." << std::endl;

    HdrHistogram hist(1'000'000, 3);
    assert(hist.total_count() == 0);
    assert(hist.min_value() == 0);
    assert(hist.max_value() == 0);
    assert(hist.value_at_percentile(50.0) == 0);

    // Single value
    hist.record(42);
    assert(hist.total_count() == 1);
    assert(hist.min_value() == 42);
    assert(hist.max_value() == 42);
    assert(hist.value_at_percentile(50.0) == 42);

    // Saturation beyond highest trackable value
    hist.record(5'000'000); // Exceeds 1,000,000
    assert(hist.max_value() == 1'000'000); // Clamped to highest trackable

    // Reset
    hist.reset();
    assert(hist.total_count() == 0);
    assert(hist.min_value() == 0);
    assert(hist.max_value() == 0);

    std::cout << "  -> PASSED" << std::endl;
}

int main() {
    std::cout << "=====================================================" << std::endl;
    std::cout << "    WEEK 4: HDR HISTOGRAM & COORDINATED OMISSION     " << std::endl;
    std::cout << "=====================================================" << std::endl;

    test_basic_recording_and_percentiles();
    test_coordinated_omission_correction();
    test_edge_cases_and_reset();

    std::cout << "\n[PASS] All Week 4 HDR Histogram Unit Tests Passed!\n" << std::endl;
    return 0;
}
