#include "../src/common/Order.hpp"
#include "../src/common/Types.hpp"
#include <iostream>
#include <vector>
#include <list>
#include <numeric>
#include <random>
#include <chrono>
#include <iomanip>
#include <algorithm>

#ifdef _MSC_VER
#include <intrin.h>
#else
#include <x86intrin.h>
#endif

using namespace lob;

// Cycle calibration helper
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

// Volatile sink to prevent compiler optimizing away traversal loops
static volatile uint64_t g_sink = 0;

int main() {
    std::cout << "===================================================================\n";
    std::cout << "      WEEK 2: MECHANICAL SYMPATHY & CACHE LOCALITY BENCHMARK       \n";
    std::cout << "===================================================================\n";

    double ghz = estimate_tsc_frequency_ghz();
    std::cout << "[INFO] Calibrating RDTSC... CPU Frequency: ~" 
              << std::fixed << std::setprecision(2) << ghz << " GHz\n";

    const size_t NUM_ITEMS = 1'000'000;
    std::cout << "[INFO] Benchmark Dataset Size: " << NUM_ITEMS << " elements\n\n";

    // -------------------------------------------------------------------------
    // EXPERIMENT 1: Contiguous Vector vs Heap-Scattered Linked List
    // -------------------------------------------------------------------------
    std::cout << "-------------------------------------------------------------------\n";
    std::cout << " [EXP 1] std::vector<uint64_t> (Contiguous) vs std::list<uint64_t> \n";
    std::cout << "-------------------------------------------------------------------\n";

    std::vector<uint64_t> vec_data;
    vec_data.reserve(NUM_ITEMS);
    for (size_t i = 0; i < NUM_ITEMS; ++i) {
        vec_data.push_back(i + 1);
    }

    std::list<uint64_t> list_data;
    for (size_t i = 0; i < NUM_ITEMS; ++i) {
        list_data.push_back(i + 1);
    }

    // Warm-up caches
    uint64_t sum_warmup = 0;
    for (const auto& v : vec_data) sum_warmup += v;
    for (const auto& l : list_data) sum_warmup += l;
    g_sink = sum_warmup;

    // Test 1A: Contiguous std::vector
    uint64_t t0 = __rdtsc();
    uint64_t vec_sum = 0;
    for (const auto& val : vec_data) {
        vec_sum += val;
    }
    uint64_t t1 = __rdtsc();
    g_sink = vec_sum;

    uint64_t vec_cycles = t1 - t0;
    double vec_ns = (double)vec_cycles / ghz;
    double vec_ns_per_elem = vec_ns / (double)NUM_ITEMS;

    // Test 1B: Pointer-chasing std::list
    uint64_t t2 = __rdtsc();
    uint64_t list_sum = 0;
    for (const auto& val : list_data) {
        list_sum += val;
    }
    uint64_t t3 = __rdtsc();
    g_sink = list_sum;

    uint64_t list_cycles = t3 - t2;
    double list_ns = (double)list_cycles / ghz;
    double list_ns_per_elem = list_ns / (double)NUM_ITEMS;

    std::cout << "  1A. std::vector<uint64_t> : " 
              << std::setw(8) << std::fixed << std::setprecision(2) << vec_ns / 1'000'000.0 << " ms (" 
              << vec_cycles << " cycles, " 
              << std::setprecision(3) << vec_ns_per_elem << " ns/elem)\n";

    std::cout << "  1B. std::list<uint64_t>   : " 
              << std::setw(8) << std::fixed << std::setprecision(2) << list_ns / 1'000'000.0 << " ms (" 
              << list_cycles << " cycles, " 
              << std::setprecision(3) << list_ns_per_elem << " ns/elem)\n";

    std::cout << "  >>> RESULT: Contiguous std::vector is " 
              << std::setprecision(1) << (list_ns / vec_ns) 
              << "x FASTER than std::list due to CPU cache locality!\n\n";

    // -------------------------------------------------------------------------
    // EXPERIMENT 2: Contiguous Order Objects vs Heap-Allocated Pointers (Order*)
    // -------------------------------------------------------------------------
    std::cout << "-------------------------------------------------------------------\n";
    std::cout << " [EXP 2] std::vector<Order> (Contiguous) vs std::vector<Order*>   \n";
    std::cout << "-------------------------------------------------------------------\n";

    std::vector<Order> contiguous_orders;
    contiguous_orders.reserve(NUM_ITEMS);
    for (size_t i = 1; i <= NUM_ITEMS; ++i) {
        contiguous_orders.emplace_back(i, Side::BUY, 10000 + (i % 100), 100, i * 10);
    }

    std::vector<Order*> pointer_orders;
    pointer_orders.reserve(NUM_ITEMS);
    for (size_t i = 1; i <= NUM_ITEMS; ++i) {
        pointer_orders.push_back(new Order(i, Side::BUY, 10000 + (i % 100), 100, i * 10));
    }

    // Test 2A: Contiguous Order Structs
    uint64_t t4 = __rdtsc();
    uint64_t contig_qty_sum = 0;
    for (const auto& ord : contiguous_orders) {
        contig_qty_sum += ord.quantity + ord.price;
    }
    uint64_t t5 = __rdtsc();
    g_sink = contig_qty_sum;

    uint64_t contig_cycles = t5 - t4;
    double contig_ns = (double)contig_cycles / ghz;
    double contig_ns_per_elem = contig_ns / (double)NUM_ITEMS;

    // Test 2B: Heap-Allocated Order Pointers
    uint64_t t6 = __rdtsc();
    uint64_t ptr_qty_sum = 0;
    for (const auto* ord : pointer_orders) {
        ptr_qty_sum += ord->quantity + ord->price;
    }
    uint64_t t7 = __rdtsc();
    g_sink = ptr_qty_sum;

    uint64_t ptr_cycles = t7 - t6;
    double ptr_ns = (double)ptr_cycles / ghz;
    double ptr_ns_per_elem = ptr_ns / (double)NUM_ITEMS;

    std::cout << "  2A. Contiguous Order[]   : " 
              << std::setw(8) << std::fixed << std::setprecision(2) << contig_ns / 1'000'000.0 << " ms (" 
              << contig_cycles << " cycles, " 
              << std::setprecision(3) << contig_ns_per_elem << " ns/elem)\n";

    std::cout << "  2B. Heap Pointers (Order*): " 
              << std::setw(8) << std::fixed << std::setprecision(2) << ptr_ns / 1'000'000.0 << " ms (" 
              << ptr_cycles << " cycles, " 
              << std::setprecision(3) << ptr_ns_per_elem << " ns/elem)\n";

    std::cout << "  >>> RESULT: Contiguous memory is " 
              << std::setprecision(1) << (ptr_ns / contig_ns) 
              << "x FASTER than pointer dereferencing on the hot path!\n\n";

    // Clean up heap orders
    for (auto* p : pointer_orders) {
        delete p;
    }
    pointer_orders.clear();

    // -------------------------------------------------------------------------
    // EXPERIMENT 3: Sequential vs Random Access (Hardware Prefetcher Impact)
    // -------------------------------------------------------------------------
    std::cout << "-------------------------------------------------------------------\n";
    std::cout << " [EXP 3] Hardware Prefetcher: Sequential vs Random Array Access    \n";
    std::cout << "-------------------------------------------------------------------\n";

    std::vector<size_t> indices(NUM_ITEMS);
    std::iota(indices.begin(), indices.end(), 0);

    // Test 3A: Sequential Index Access (Prefetcher engages)
    uint64_t t8 = __rdtsc();
    uint64_t seq_sum = 0;
    for (size_t i = 0; i < NUM_ITEMS; ++i) {
        seq_sum += vec_data[indices[i]];
    }
    uint64_t t9 = __rdtsc();
    g_sink = seq_sum;

    uint64_t seq_cycles = t9 - t8;
    double seq_ns = (double)seq_cycles / ghz;
    double seq_ns_per_elem = seq_ns / (double)NUM_ITEMS;

    // Shuffle indices to completely defeat the CPU hardware prefetcher
    std::mt19937_64 rng(1337);
    std::shuffle(indices.begin(), indices.end(), rng);

    // Test 3B: Random Index Access (Prefetcher defeated -> CPU stalls on L3/DRAM)
    uint64_t t10 = __rdtsc();
    uint64_t rand_sum = 0;
    for (size_t i = 0; i < NUM_ITEMS; ++i) {
        rand_sum += vec_data[indices[i]];
    }
    uint64_t t11 = __rdtsc();
    g_sink = rand_sum;

    uint64_t rand_cycles = t11 - t10;
    double rand_ns = (double)rand_cycles / ghz;
    double rand_ns_per_elem = rand_ns / (double)NUM_ITEMS;

    std::cout << "  3A. Sequential Traversal : " 
              << std::setw(8) << std::fixed << std::setprecision(2) << seq_ns / 1'000'000.0 << " ms (" 
              << seq_cycles << " cycles, " 
              << std::setprecision(3) << seq_ns_per_elem << " ns/elem)\n";

    std::cout << "  3B. Random Traversal     : " 
              << std::setw(8) << std::fixed << std::setprecision(2) << rand_ns / 1'000'000.0 << " ms (" 
              << rand_cycles << " cycles, " 
              << std::setprecision(3) << rand_ns_per_elem << " ns/elem)\n";

    std::cout << "  >>> RESULT: Hardware prefetching delivers a " 
              << std::setprecision(1) << (rand_ns / seq_ns) 
              << "x SPEEDUP over random pointer-hopping!\n";
    std::cout << "===================================================================\n\n";

    return 0;
}
