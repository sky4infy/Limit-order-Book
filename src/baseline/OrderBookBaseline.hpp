#pragma once

#include "../common/Order.hpp"
#include "../common/Types.hpp"
#include <map>
#include <list>
#include <vector>
#include <unordered_map>
#include <optional>
#include <functional>

namespace lob {

// Phase 1 Baseline Limit Order Book:
// Built using textbook standard C++ STL containers:
// - std::map: Red-Black self-balancing binary search tree (stores price levels in sorted order)
// - std::list: Doubly-linked list (stores orders at each price level in FIFO time priority)
//
// INTERVIEW LESSON:
// While clean, safe, and 100% semantically correct, this design causes:
// 1. Heap fragmentation and allocator locks (every list node and map node is dynamically allocated on the heap).
// 2. Cache misses: Nodes are scattered randomly in memory, causing pointer-chasing stalls.
class OrderBookBaseline {
public:
    OrderBookBaseline() = default;

    // Add a new order: matches immediately if crossing the spread;
    // rests remaining quantity in the book if unfilled.
    // Returns list of executed trades.
    std::vector<Trade> add_order(Order order);

    // Cancel an existing resting order by its OrderId.
    // Returns true if successfully found and canceled, false otherwise.
    bool cancel_order(OrderId order_id);

    // BBO (Best Bid and Offer) Queries
    std::optional<Price> get_best_bid() const;
    std::optional<Price> get_best_ask() const;

    // Depth Queries
    Quantity get_volume_at_price(Side side, Price price) const;
    size_t total_orders_count() const { return order_index_.size(); }
    bool is_empty() const { return order_index_.empty(); }

    // Clear entire book
    void clear();

    // Print order book depth to console
    void print_book(size_t depth = 5) const;

private:
    // Internal matching routines
    std::vector<Trade> match_buy_order(Order& incoming_buy);
    std::vector<Trade> match_sell_order(Order& incoming_sell);

    // Bids: sorted DESCENDING (highest buying price first)
    std::map<Price, std::list<Order>, std::greater<Price>> bids_;

    // Asks: sorted ASCENDING (lowest selling price first)
    std::map<Price, std::list<Order>, std::less<Price>> asks_;

    // Order Index for fast cancellation: OrderId -> (Side, Price)
    std::unordered_map<OrderId, std::pair<Side, Price>> order_index_;
};

} // namespace lob
