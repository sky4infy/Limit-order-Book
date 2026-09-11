#pragma once

#include <cstdint>
#include <string>
#include <iostream>

namespace lob {

// Order Side: Buy or Sell
// Stored as uint8_t (1 byte) instead of 4-byte int to conserve memory
enum class Side : uint8_t {
    BUY = 0,
    SELL = 1
};

inline std::string side_to_string(Side side) {
    return side == Side::BUY ? "BUY" : "SELL";
}

// Fixed-point Price representation:
// Why uint64_t instead of double?
// IEEE 754 floating point numbers cannot represent decimals precisely (e.g. 0.1 + 0.2 = 0.30000000000000004).
// In financial trading, prices are stored as integer ticks (e.g., $100.25 is stored as 10025 with tick_size = 0.01).
using Price = uint64_t;

// Order Quantity / Size (shares or contracts)
using Quantity = uint32_t;

// Unique Monotonic Order Identifier
using OrderId = uint64_t;

// Timestamp in nanoseconds or CPU clock cycles
using Timestamp = uint64_t;

// Trade Execution Event: emitted whenever an incoming order crosses the spread
// and matches with a resting passive order in the book.
struct Trade {
    OrderId maker_order_id; // Passive resting order that was already in the book
    OrderId taker_order_id; // Aggressive incoming order that took liquidity
    Price   price;          // Execution price (always determined by the maker's price)
    Quantity quantity;      // Number of shares executed
    Timestamp timestamp;

    void print() const {
        std::cout << "[TRADE] Price: " << price 
                  << " | Qty: " << quantity 
                  << " | Maker: #" << maker_order_id 
                  << " | Taker: #" << taker_order_id << "\n";
    }
};

} // namespace lob
