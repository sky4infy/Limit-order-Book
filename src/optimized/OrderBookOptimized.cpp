#include "OrderBookOptimized.hpp"
#include <iomanip>
#include <algorithm>
#include <iostream>

namespace lob {

OrderBookOptimized::OrderBookOptimized() = default;

std::vector<Trade> OrderBookOptimized::add_order(const OptimizedOrder& order) {
    if (order.quantity == 0) {
        return {};
    }

    if (order.side == Side::BUY) {
        return match_buy_order(order);
    } else {
        return match_sell_order(order);
    }
}

std::vector<Trade> OrderBookOptimized::add_order(const Order& order) {
    return add_order(OptimizedOrder(order.order_id, order.side, order.price, order.quantity, order.timestamp));
}

std::vector<Trade> OrderBookOptimized::match_buy_order(OptimizedOrder incoming_buy) {
    std::vector<Trade> trades;

    while (incoming_buy.quantity > 0) {
        auto best_ask_opt = ask_ladder_.get_lowest_price();
        if (!best_ask_opt.has_value()) {
            break;
        }

        Price best_ask_price = *best_ask_opt;
        if (incoming_buy.price < best_ask_price) {
            break; // Spread not crossed
        }

        PriceLevel& ask_level = ask_ladder_.get_level(best_ask_price);

        while (incoming_buy.quantity > 0 && !ask_level.is_empty()) {
            uint32_t maker_idx = ask_level.head_order_idx;
            OptimizedOrder& resting_ask = slab_.get(maker_idx);

            Quantity fill_qty = std::min(incoming_buy.quantity, resting_ask.quantity);

            trades.push_back(Trade{
                .maker_order_id = resting_ask.order_id,
                .taker_order_id = incoming_buy.order_id,
                .price = best_ask_price,
                .quantity = fill_qty,
                .timestamp = incoming_buy.timestamp
            });

            incoming_buy.quantity -= fill_qty;
            resting_ask.quantity -= fill_qty;
            ask_level.total_volume -= fill_qty;

            if (resting_ask.is_filled()) {
                ask_ladder_.unlink_order(best_ask_price, maker_idx, slab_);
                order_index_.erase(resting_ask.order_id);
                slab_.deallocate(maker_idx);
            }
        }
    }

    // Passive resting order
    if (incoming_buy.quantity > 0) {
        uint32_t new_idx = slab_.allocate();
        if (new_idx != INVALID_INDEX) {
            slab_.get(new_idx) = incoming_buy;
            bid_ladder_.append_order(incoming_buy.price, new_idx, slab_);
            order_index_.insert(incoming_buy.order_id, new_idx);
        }
    }

    return trades;
}

std::vector<Trade> OrderBookOptimized::match_sell_order(OptimizedOrder incoming_sell) {
    std::vector<Trade> trades;

    while (incoming_sell.quantity > 0) {
        auto best_bid_opt = bid_ladder_.get_highest_price();
        if (!best_bid_opt.has_value()) {
            break;
        }

        Price best_bid_price = *best_bid_opt;
        if (incoming_sell.price > best_bid_price) {
            break; // Spread not crossed
        }

        PriceLevel& bid_level = bid_ladder_.get_level(best_bid_price);

        while (incoming_sell.quantity > 0 && !bid_level.is_empty()) {
            uint32_t maker_idx = bid_level.head_order_idx;
            OptimizedOrder& resting_bid = slab_.get(maker_idx);

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
            bid_level.total_volume -= fill_qty;

            if (resting_bid.is_filled()) {
                bid_ladder_.unlink_order(best_bid_price, maker_idx, slab_);
                order_index_.erase(resting_bid.order_id);
                slab_.deallocate(maker_idx);
            }
        }
    }

    // Passive resting order
    if (incoming_sell.quantity > 0) {
        uint32_t new_idx = slab_.allocate();
        if (new_idx != INVALID_INDEX) {
            slab_.get(new_idx) = incoming_sell;
            ask_ladder_.append_order(incoming_sell.price, new_idx, slab_);
            order_index_.insert(incoming_sell.order_id, new_idx);
        }
    }

    return trades;
}

bool OrderBookOptimized::cancel_order(OrderId order_id) {
    uint32_t pool_idx = order_index_.find(order_id);
    if (pool_idx == INVALID_INDEX) {
        return false;
    }

    OptimizedOrder& ord = slab_.get(pool_idx);
    Price price = ord.price;
    Side side = ord.side;

    if (side == Side::BUY) {
        bid_ladder_.unlink_order(price, pool_idx, slab_);
    } else {
        ask_ladder_.unlink_order(price, pool_idx, slab_);
    }

    order_index_.erase(order_id);
    slab_.deallocate(pool_idx);
    return true;
}

bool OrderBookOptimized::modify_order(OrderId order_id, Quantity new_quantity) {
    if (new_quantity == 0) {
        return cancel_order(order_id);
    }

    uint32_t pool_idx = order_index_.find(order_id);
    if (pool_idx == INVALID_INDEX) {
        return false;
    }

    OptimizedOrder& ord = slab_.get(pool_idx);
    Price price = ord.price;
    Side side = ord.side;
    PriceLevel& level = (side == Side::BUY) ? bid_ladder_.get_level(price) : ask_ladder_.get_level(price);

    if (new_quantity <= ord.quantity) {
        // Size reduction: preserve FIFO priority in queue
        Quantity diff = ord.quantity - new_quantity;
        ord.quantity = new_quantity;
        level.total_volume -= diff;
    } else {
        // Size increase: loses FIFO priority, moves to queue tail
        if (side == Side::BUY) {
            bid_ladder_.unlink_order(price, pool_idx, slab_);
            ord.quantity = new_quantity;
            bid_ladder_.append_order(price, pool_idx, slab_);
        } else {
            ask_ladder_.unlink_order(price, pool_idx, slab_);
            ord.quantity = new_quantity;
            ask_ladder_.append_order(price, pool_idx, slab_);
        }
    }

    return true;
}

bool OrderBookOptimized::has_order(OrderId order_id) const noexcept {
    return order_index_.contains(order_id);
}

std::optional<OptimizedOrder> OrderBookOptimized::get_order(OrderId order_id) const noexcept {
    uint32_t pool_idx = order_index_.find(order_id);
    if (pool_idx == INVALID_INDEX) {
        return std::nullopt;
    }
    return slab_.get(pool_idx);
}

std::optional<Price> OrderBookOptimized::get_best_bid() const noexcept {
    return bid_ladder_.get_highest_price();
}

std::optional<Price> OrderBookOptimized::get_best_ask() const noexcept {
    return ask_ladder_.get_lowest_price();
}

std::optional<Price> OrderBookOptimized::get_spread() const noexcept {
    auto best_bid = get_best_bid();
    auto best_ask = get_best_ask();

    if (best_bid && best_ask && *best_ask >= *best_bid) {
        return *best_ask - *best_bid;
    }
    return std::nullopt;
}

std::optional<double> OrderBookOptimized::get_mid_price() const noexcept {
    auto best_bid = get_best_bid();
    auto best_ask = get_best_ask();

    if (best_bid && best_ask) {
        return (*best_bid + *best_ask) / 2.0;
    }
    return std::nullopt;
}

Quantity OrderBookOptimized::get_volume_at_price(Side side, Price price) const noexcept {
    if (price >= MAX_PRICES) return 0;
    const PriceLevel& level = (side == Side::BUY) ? bid_ladder_.get_level(price) : ask_ladder_.get_level(price);
    return level.total_volume;
}

Quantity OrderBookOptimized::get_total_volume(Side side) const noexcept {
    Quantity total = 0;
    const auto& ladder = (side == Side::BUY) ? bid_ladder_ : ask_ladder_;

    auto curr_opt = (side == Side::BUY) ? ladder.get_highest_price() : ladder.get_lowest_price();
    while (curr_opt.has_value()) {
        total += ladder.get_level(*curr_opt).total_volume;
        curr_opt = (side == Side::BUY) ? ladder.get_next_lower_price(*curr_opt) : ladder.get_next_higher_price(*curr_opt);
    }

    return total;
}

std::vector<LevelInfo> OrderBookOptimized::get_level_depth(Side side, size_t max_depth) const {
    std::vector<LevelInfo> depth;
    depth.reserve(max_depth);

    const auto& ladder = (side == Side::BUY) ? bid_ladder_ : ask_ladder_;
    auto curr_opt = (side == Side::BUY) ? ladder.get_highest_price() : ladder.get_lowest_price();

    while (curr_opt.has_value() && depth.size() < max_depth) {
        const PriceLevel& level = ladder.get_level(*curr_opt);
        if (!level.is_empty()) {
            depth.push_back(LevelInfo{
                .price = level.price,
                .volume = level.total_volume,
                .order_count = level.order_count
            });
        }
        curr_opt = (side == Side::BUY) ? ladder.get_next_lower_price(*curr_opt) : ladder.get_next_higher_price(*curr_opt);
    }

    return depth;
}

void OrderBookOptimized::clear() noexcept {
    slab_.reset();
    bid_ladder_.clear();
    ask_ladder_.clear();
    order_index_.clear();
}

void OrderBookOptimized::print_book(size_t depth) const {
    std::cout << "\n================= OPTIMIZED ORDER BOOK DEPTH =================\n";
    std::cout << "        ASKS (SELLERS - Lowest First)               \n";
    std::cout << "----------------------------------------------------\n";
    std::cout << "   Price ($)      Shares      Orders\n";

    auto ask_depth = get_level_depth(Side::SELL, depth);
    std::reverse(ask_depth.begin(), ask_depth.end());

    for (const auto& lvl : ask_depth) {
        std::cout << "  " << std::setw(9) << std::fixed << std::setprecision(2) << (double)lvl.price / 100.0
                  << "  " << std::setw(10) << lvl.volume
                  << "  " << std::setw(10) << lvl.order_count << "\n";
    }

    std::cout << "----------------------------------------------------\n";
    auto spread = get_spread();
    if (spread) {
        std::cout << ">>> SPREAD: $" << std::fixed << std::setprecision(2) << (double)*spread / 100.0 << " <<<\n";
    } else {
        std::cout << ">>> SPREAD: LOCKED / CROSSED / EMPTY <<<\n";
    }
    std::cout << "----------------------------------------------------\n";
    std::cout << "        BIDS (BUYERS - Highest First)               \n";
    std::cout << "----------------------------------------------------\n";

    auto bid_depth = get_level_depth(Side::BUY, depth);
    for (const auto& lvl : bid_depth) {
        std::cout << "  " << std::setw(9) << std::fixed << std::setprecision(2) << (double)lvl.price / 100.0
                  << "  " << std::setw(10) << lvl.volume
                  << "  " << std::setw(10) << lvl.order_count << "\n";
    }
    std::cout << "====================================================\n\n";
}

} // namespace lob
