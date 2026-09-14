#pragma once

#include <cstdint>
#include <string>
#include <iostream>

namespace lob {

enum class Side : uint8_t {
    BUY = 0,
    SELL = 1
};

inline std::string side_to_string(Side side) {
    return side == Side::BUY ? "BUY" : "SELL";
}

using Price = uint64_t;
using Quantity = uint32_t;
using OrderId = uint64_t;
using Timestamp = uint64_t;

struct Trade {
    OrderId maker_order_id;
    OrderId taker_order_id;
    Price   price;
    Quantity quantity;
    Timestamp timestamp;

    void print() const {
        std::cout << "[TRADE] Price: " << price 
                  << " | Qty: " << quantity 
                  << " | Maker: #" << maker_order_id 
                  << " | Taker: #" << taker_order_id << "\n";
    }
};

struct LevelInfo {
    Price price;
    Quantity volume;
    size_t order_count;
};

} // namespace lob
