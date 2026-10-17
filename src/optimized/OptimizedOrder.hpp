#pragma once

#include "../common/Types.hpp"
#include <cstdint>
#include <limits>
#include <iostream>

namespace lob {

constexpr uint32_t INVALID_INDEX = std::numeric_limits<uint32_t>::max();

/**
 * @brief Institutional Cache-Aligned Order Struct (64 Bytes = Exactly 1 Cache Line)
 * 
 * In Week 2, our memory layout tests proved that the baseline Order struct:
 * 1. Suffered from 7 bytes of dead compiler padding between 'side' and 'price'.
 * 2. Occupied 40 bytes, causing orders in an array to cross 64-byte cache line boundaries.
 * 
 * OptimizedOrder solves both:
 * - Members are arranged in descending size order to eliminate internal padding.
 * - Intrusive 'prev_idx' and 'next_idx' replace heap-allocated std::list node pointers.
 * - Exactly 64 bytes in size and 64-byte aligned (alignas(64)), guaranteeing that
 *   every order occupies exactly ONE physical cache line with zero splitting or false sharing.
 */
struct alignas(64) OptimizedOrder {
    // 8-byte aligned fields (Offset 0..23)
    OrderId   order_id{0};          // 8 bytes
    Price     price{0};             // 8 bytes
    Timestamp timestamp{0};         // 8 bytes

    // 4-byte fields (Offset 24..39)
    Quantity  quantity{0};          // 4 bytes
    Quantity  initial_quantity{0};  // 4 bytes
    uint32_t  prev_idx{INVALID_INDEX}; // 4 bytes (intrusive doubly-linked queue pointer)
    uint32_t  next_idx{INVALID_INDEX}; // 4 bytes (intrusive doubly-linked queue pointer)

    // 1-byte field (Offset 40)
    Side      side{Side::BUY};      // 1 byte

    // Explicit cache-line padding (Offsets 41..63 = 23 bytes)
    // Ensures sizeof == 64 bytes and each order is independent in the L1 data cache.
    uint8_t   padding[23]{0};

    OptimizedOrder() = default;

    OptimizedOrder(OrderId id, Side s, Price p, Quantity qty, Timestamp ts = 0)
        : order_id(id), price(p), timestamp(ts),
          quantity(qty), initial_quantity(qty),
          prev_idx(INVALID_INDEX), next_idx(INVALID_INDEX),
          side(s) {}

    bool is_filled() const {
        return quantity == 0;
    }

    void print() const {
        std::cout << "[OPTIMIZED ORDER #" << order_id << "] " 
                  << side_to_string(side) << " " 
                  << quantity << " @ $" << price / 100 << "." 
                  << (price % 100 < 10 ? "0" : "") << (price % 100) 
                  << " (prev=" << prev_idx << ", next=" << next_idx << ")\n";
    }
};

static_assert(sizeof(OptimizedOrder) == 64, "OptimizedOrder must be exactly 64 bytes (1 cache line)!");
static_assert(alignof(OptimizedOrder) == 64, "OptimizedOrder must be aligned to 64 bytes!");

} // namespace lob
