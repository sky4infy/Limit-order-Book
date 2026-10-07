#include "../src/common/Order.hpp"
#include "../src/common/Types.hpp"
#include <iostream>
#include <cstddef>
#include <cassert>
#include <iomanip>
#include <new>

using namespace lob;

void print_order_layout() {
    std::cout << "===================================================================\n";
    std::cout << "         WEEK 2: STRUCT MEMORY LAYOUT & ALIGNMENT ANALYSIS          \n";
    std::cout << "===================================================================\n";

    std::cout << "1. Order Struct Field Offsets & Sizes:\n";
    std::cout << "   - sizeof(Order)          : " << sizeof(Order) << " bytes\n";
    std::cout << "   - alignof(Order)         : " << alignof(Order) << " bytes\n";
    std::cout << "   - offsetof(order_id)     : " << offsetof(Order, order_id) 
              << " (size: " << sizeof(OrderId) << " bytes)\n";
    std::cout << "   - offsetof(side)         : " << offsetof(Order, side) 
              << " (size: " << sizeof(Side) << " bytes)\n";

    size_t side_end = offsetof(Order, side) + sizeof(Side);
    size_t price_start = offsetof(Order, price);
    size_t padding_bytes = price_start - side_end;

    std::cout << "     >> PADDING DETECTED    : " << padding_bytes 
              << " wasted bytes between 'side' and 'price' for 8-byte alignment!\n";

    std::cout << "   - offsetof(price)        : " << offsetof(Order, price) 
              << " (size: " << sizeof(Price) << " bytes)\n";
    std::cout << "   - offsetof(quantity)     : " << offsetof(Order, quantity) 
              << " (size: " << sizeof(Quantity) << " bytes)\n";
    std::cout << "   - offsetof(initial_qty)  : " << offsetof(Order, initial_quantity) 
              << " (size: " << sizeof(Quantity) << " bytes)\n";
    std::cout << "   - offsetof(timestamp)    : " << offsetof(Order, timestamp) 
              << " (size: " << sizeof(Timestamp) << " bytes)\n\n";

    // Trade struct inspection
    std::cout << "2. Trade Struct Field Offsets & Sizes:\n";
    std::cout << "   - sizeof(Trade)          : " << sizeof(Trade) << " bytes\n";
    std::cout << "   - alignof(Trade)         : " << alignof(Trade) << " bytes\n";
    std::cout << "   - offsetof(maker_order_id: " << offsetof(Trade, maker_order_id) << "\n";
    std::cout << "   - offsetof(taker_order_id: " << offsetof(Trade, taker_order_id) << "\n";
    std::cout << "   - offsetof(price)        : " << offsetof(Trade, price) << "\n";
    std::cout << "   - offsetof(quantity)     : " << offsetof(Trade, quantity) << "\n";
    std::cout << "   - offsetof(timestamp)    : " << offsetof(Trade, timestamp) << "\n\n";

    // Cache line calculation
    constexpr size_t CACHE_LINE_SIZE = 64;
    std::cout << "3. CPU Cache Line Interaction (64-byte L1 Cache Line):\n";
    std::cout << "   - Cache Line Size        : " << CACHE_LINE_SIZE << " bytes\n";
    std::cout << "   - Order Size             : " << sizeof(Order) << " bytes\n";
    std::cout << "   - Orders per Cache Line  : " 
              << (double)CACHE_LINE_SIZE / sizeof(Order) << " orders\n";

    std::cout << "\n   [CRITICAL INSIGHT: Cache Line Splitting]\n";
    std::cout << "   In an array of Order structs: \n";
    std::cout << "   - Order[0]: occupies bytes 0..39 (fits within Cache Line 0)\n";
    std::cout << "   - Order[1]: occupies bytes 40..79 (CROSSES boundary! Bytes 40..63 in Line 0, Bytes 64..79 in Line 1)\n";
    std::cout << "   >>> Traversing Order[1] forces the CPU to fetch TWO cache lines instead of one!\n";
    std::cout << "   >>> In Phase 2, we will design our Slab Allocator to align orders cleanly or embed intrusive indices.\n\n";

    std::cout << "4. Heap Overhead in Baseline (std::list & std::map):\n";
    size_t list_node_approx = sizeof(Order) + 2 * sizeof(void*); // prev + next pointers
    std::cout << "   - Approximate std::list<Order> node size : " << list_node_approx << " bytes\n";
    std::cout << "   - Node pointer overhead per order       : " 
              << (2 * sizeof(void*)) << " bytes (+ malloc header)\n";
    std::cout << "   - Heap memory for 100,000 orders in std::list : ~" 
              << (list_node_approx * 100000) / (1024 * 1024) << " MB (vs " 
              << (sizeof(Order) * 100000) / (1024 * 1024) << " MB contiguous flat data)\n";
    std::cout << "===================================================================\n";
}

void verify_assertions() {
    assert(sizeof(Order) == 40);
    assert(alignof(Order) == 8);
    assert(offsetof(Order, order_id) == 0);
    assert(offsetof(Order, side) == 8);
    assert(offsetof(Order, price) == 16);
    assert(offsetof(Order, quantity) == 24);
    assert(offsetof(Order, initial_quantity) == 28);
    assert(offsetof(Order, timestamp) == 32);

    assert(sizeof(Trade) == 40);
    assert(alignof(Trade) == 8);
}

int main() {
    print_order_layout();
    verify_assertions();
    std::cout << "\n[PASS] All Memory Layout & Alignment assertions verified successfully!\n\n";
    return 0;
}
