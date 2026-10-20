#pragma once

#include "OptimizedOrder.hpp"
#include "SlabAllocator.hpp"
#include "DirectPriceLadder.hpp"
#include "FlatOrderIndex.hpp"
#include "../common/Order.hpp"
#include "../common/Types.hpp"
#include <vector>
#include <optional>
#include <cstdint>

namespace lob {

/**
 * @brief Phase 2 Zero-Allocation Institutional Limit Order Book Matching Engine
 * 
 * Implements strict Price-Time Priority (FIFO) continuous double-auction matching
 * with zero dynamic memory allocations on the hot execution path.
 * 
 * Hardware Sympathy Architecture:
 * - Pre-allocated SlabAllocator: 1,000,000 contiguous 64-byte orders.
 * - Flat DirectPriceLadder: 131,072 directly-indexed price levels.
 * - Hierarchical 64-bit Bitmask: O(1) BBO lookup via CPU bit-scan intrinsics.
 * - FlatOrderIndex: O(1) open-addressing lookup without malloc.
 * - Intrusive FIFO Queues: Zero wrapper node allocations.
 */
class OrderBookOptimized {
public:
    static constexpr size_t POOL_CAPACITY = 1'000'000;
    static constexpr size_t MAX_PRICES    = 131'072;
    static constexpr size_t INDEX_CAPACITY = 262'144;

    OrderBookOptimized();

    // Hot-path order entry
    std::vector<Trade> add_order(const OptimizedOrder& order);
    std::vector<Trade> add_order(const Order& order);

    // Order cancellation & modification
    bool cancel_order(OrderId order_id);
    bool modify_order(OrderId order_id, Quantity new_quantity);

    // Order querying
    [[nodiscard]] bool has_order(OrderId order_id) const noexcept;
    [[nodiscard]] std::optional<OptimizedOrder> get_order(OrderId order_id) const noexcept;

    // Market Depth & BBO
    [[nodiscard]] std::optional<Price> get_best_bid() const noexcept;
    [[nodiscard]] std::optional<Price> get_best_ask() const noexcept;
    [[nodiscard]] std::optional<Price> get_spread() const noexcept;
    [[nodiscard]] std::optional<double> get_mid_price() const noexcept;

    [[nodiscard]] Quantity get_volume_at_price(Side side, Price price) const noexcept;
    [[nodiscard]] Quantity get_total_volume(Side side) const noexcept;
    [[nodiscard]] std::vector<LevelInfo> get_level_depth(Side side, size_t max_depth = 5) const;

    [[nodiscard]] size_t total_orders_count() const noexcept { return order_index_.size(); }
    [[nodiscard]] bool is_empty() const noexcept { return order_index_.is_empty(); }

    void clear() noexcept;
    void print_book(size_t depth = 5) const;

private:
    std::vector<Trade> match_buy_order(OptimizedOrder incoming_buy);
    std::vector<Trade> match_sell_order(OptimizedOrder incoming_sell);

    SlabAllocator<OptimizedOrder, POOL_CAPACITY> slab_;
    DirectPriceLadder<MAX_PRICES>                bid_ladder_;
    DirectPriceLadder<MAX_PRICES>                ask_ladder_;
    FlatOrderIndex<INDEX_CAPACITY>               order_index_;
};

} // namespace lob
