#include "OrderBookBaseline.hpp"
#include <iomanip>
#include <algorithm>

namespace lob {

std::vector<Trade> OrderBookBaseline::add_order(Order order) {
    if (order.quantity == 0) {
        return {};
    }

    if (order.side == Side::BUY) {
        return match_buy_order(order);
    } else {
        return match_sell_order(order);
    }
}

std::vector<Trade> OrderBookBaseline::match_buy_order(Order& incoming_buy) {
    std::vector<Trade> trades;

    // Loop while the incoming buy order has open quantity AND there are resting asks in the book
    while (incoming_buy.quantity > 0 && !asks_.empty()) {
        auto best_ask_it = asks_.begin();
        Price best_ask_price = best_ask_it->first;

        // Price check: If the buyer's limit price is strictly LESS than the lowest seller price,
        // no match can occur. The spread is not crossed.
        if (incoming_buy.price < best_ask_price) {
            break;
        }

        // We have a match! Access the FIFO queue of resting sell orders at this price
        auto& resting_queue = best_ask_it->second;

        while (incoming_buy.quantity > 0 && !resting_queue.empty()) {
            Order& resting_ask = resting_queue.front();

            // Matched quantity is the minimum of what buyer wants and what seller offers
            Quantity fill_qty = std::min(incoming_buy.quantity, resting_ask.quantity);

            // In continuous trading, execution price is always set by the resting maker order!
            trades.push_back(Trade{
                .maker_order_id = resting_ask.order_id,
                .taker_order_id = incoming_buy.order_id,
                .price = best_ask_price,
                .quantity = fill_qty,
                .timestamp = incoming_buy.timestamp
            });

            // Decrement remaining quantities
            incoming_buy.quantity -= fill_qty;
            resting_ask.quantity -= fill_qty;

            // If the resting ask is completely filled, remove it from the queue & index
            if (resting_ask.is_filled()) {
                order_index_.erase(resting_ask.order_id);
                resting_queue.pop_front();
            }
        }

        // If all resting orders at this price level are consumed, remove the price level
        if (resting_queue.empty()) {
            asks_.erase(best_ask_it);
        }
    }

    // Passive Resting: If incoming buy order still has open quantity, insert it into the bid book
    if (incoming_buy.quantity > 0) {
        bids_[incoming_buy.price].push_back(incoming_buy);
        order_index_[incoming_buy.order_id] = {Side::BUY, incoming_buy.price};
    }

    return trades;
}

std::vector<Trade> OrderBookBaseline::match_sell_order(Order& incoming_sell) {
    std::vector<Trade> trades;

    // Loop while incoming sell order has open quantity AND there are resting bids in the book
    while (incoming_sell.quantity > 0 && !bids_.empty()) {
        auto best_bid_it = bids_.begin();
        Price best_bid_price = best_bid_it->first;

        // Price check: If the seller's limit price is strictly GREATER than the highest buyer price,
        // no match can occur. The spread is not crossed.
        if (incoming_sell.price > best_bid_price) {
            break;
        }

        // Match! Access the FIFO queue of resting buy orders at this price
        auto& resting_queue = best_bid_it->second;

        while (incoming_sell.quantity > 0 && !resting_queue.empty()) {
            Order& resting_bid = resting_queue.front();

            Quantity fill_qty = std::min(incoming_sell.quantity, resting_bid.quantity);

            trades.push_back(Trade{
                .maker_order_id = resting_bid.order_id,
                .taker_order_id = incoming_sell.order_id,
                .price = best_bid_price,
                .quantity = fill_qty,
                .timestamp = incoming_sell.timestamp
            });

            incoming_sell.quantity -= fill_qty;
            resting_bid.quantity -= fill_qty;

            if (resting_bid.is_filled()) {
                order_index_.erase(resting_bid.order_id);
                resting_queue.pop_front();
            }
        }

        if (resting_queue.empty()) {
            bids_.erase(best_bid_it);
        }
    }

    // Passive Resting: Insert leftover sell quantity into the ask book
    if (incoming_sell.quantity > 0) {
        asks_[incoming_sell.price].push_back(incoming_sell);
        order_index_[incoming_sell.order_id] = {Side::SELL, incoming_sell.price};
    }

    return trades;
}

bool OrderBookBaseline::cancel_order(OrderId order_id) {
    auto it = order_index_.find(order_id);
    if (it == order_index_.end()) {
        return false; // Order not found or already filled
    }

    Side side = it->second.first;
    Price price = it->second.second;
    order_index_.erase(it);

    if (side == Side::BUY) {
        auto map_it = bids_.find(price);
        if (map_it != bids_.end()) {
            auto& queue = map_it->second;
            for (auto q_it = queue.begin(); q_it != queue.end(); ++q_it) {
                if (q_it->order_id == order_id) {
                    queue.erase(q_it);
                    if (queue.empty()) {
                        bids_.erase(map_it);
                    }
                    return true;
                }
            }
        }
    } else {
        auto map_it = asks_.find(price);
        if (map_it != asks_.end()) {
            auto& queue = map_it->second;
            for (auto q_it = queue.begin(); q_it != queue.end(); ++q_it) {
                if (q_it->order_id == order_id) {
                    queue.erase(q_it);
                    if (queue.empty()) {
                        asks_.erase(map_it);
                    }
                    return true;
                }
            }
        }
    }

    return false;
}

std::optional<Price> OrderBookBaseline::get_best_bid() const {
    if (bids_.empty()) {
        return std::nullopt;
    }
    return bids_.begin()->first;
}

std::optional<Price> OrderBookBaseline::get_best_ask() const {
    if (asks_.empty()) {
        return std::nullopt;
    }
    return asks_.begin()->first;
}

Quantity OrderBookBaseline::get_volume_at_price(Side side, Price price) const {
    Quantity total = 0;
    if (side == Side::BUY) {
        auto it = bids_.find(price);
        if (it != bids_.end()) {
            for (const auto& ord : it->second) {
                total += ord.quantity;
            }
        }
    } else {
        auto it = asks_.find(price);
        if (it != asks_.end()) {
            for (const auto& ord : it->second) {
                total += ord.quantity;
            }
        }
    }
    return total;
}

void OrderBookBaseline::clear() {
    bids_.clear();
    asks_.clear();
    order_index_.clear();
}

void OrderBookBaseline::print_book(size_t depth) const {
    std::cout << "\n================= ORDER BOOK DEPTH =================\n";
    std::cout << "        ASKS (SELLERS - Lowest First)               \n";
    std::cout << "----------------------------------------------------\n";
    std::cout << std::setw(12) << "Price ($)" << std::setw(12) << "Shares" << std::setw(12) << "Orders" << "\n";

    // Print Asks in reverse so lowest ask is closest to spread
    std::vector<std::pair<Price, const std::list<Order>*>> top_asks;
    size_t count = 0;
    for (auto it = asks_.begin(); it != asks_.end() && count < depth; ++it, ++count) {
        top_asks.push_back({it->first, &(it->second)});
    }
    for (auto it = top_asks.rbegin(); it != top_asks.rend(); ++it) {
        Quantity vol = 0;
        for (const auto& ord : *(it->second)) vol += ord.quantity;
        std::cout << std::setw(11) << std::fixed << std::setprecision(2) << (double)it->first / 100.0
                  << " " << std::setw(12) << vol
                  << " " << std::setw(11) << it->second->size() << "\n";
    }

    // Spread Indicator
    auto bb = get_best_bid();
    auto ba = get_best_ask();
    std::cout << "----------------------------------------------------\n";
    if (bb && ba) {
        double spread = (double)(*ba - *bb) / 100.0;
        std::cout << ">>> SPREAD: $" << std::fixed << std::setprecision(2) << spread << " <<<\n";
    } else {
        std::cout << ">>> SPREAD: NO TWO-SIDED MARKET <<<\n";
    }
    std::cout << "----------------------------------------------------\n";
    std::cout << "        BIDS (BUYERS - Highest First)               \n";
    std::cout << "----------------------------------------------------\n";

    count = 0;
    for (auto it = bids_.begin(); it != bids_.end() && count < depth; ++it, ++count) {
        Quantity vol = 0;
        for (const auto& ord : it->second) vol += ord.quantity;
        std::cout << std::setw(11) << std::fixed << std::setprecision(2) << (double)it->first / 100.0
                  << " " << std::setw(12) << vol
                  << " " << std::setw(11) << it->second.size() << "\n";
    }
    std::cout << "====================================================\n\n";
}

} // namespace lob
