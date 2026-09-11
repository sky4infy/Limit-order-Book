#pragma once

#include "Types.hpp"
#include <iostream>

namespace lob {

// Baseline Order Struct:
// Represents an individual order submitted by a market participant.
struct Order {
    OrderId   order_id;         // Unique order ID
    Side      side;             // BUY or SELL
    Price     price;            // Fixed-point price ticks
    Quantity  quantity;         // Current open/remaining quantity
    Quantity  initial_quantity; // Original submitted quantity
    Timestamp timestamp;        // Priority timestamp

    Order(OrderId id, Side s, Price p, Quantity qty, Timestamp ts = 0)
        : order_id(id), side(s), price(p), quantity(qty), initial_quantity(qty), timestamp(ts) {}

    bool is_filled() const {
        return quantity == 0;
    }

    void print() const {
        std::cout << "[ORDER #" << order_id << "] " 
                  << side_to_string(side) << " " 
                  << quantity << " @ $" << price / 100 << "." 
                  << (price % 100 < 10 ? "0" : "") << (price % 100) 
                  << "\n";
    }
};

} // namespace lob
