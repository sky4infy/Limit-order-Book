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

class OrderBookBaseline {
public:
    OrderBookBaseline() = default;

    std::vector<Trade> add_order(Order order);
    bool cancel_order(OrderId order_id);

    std::optional<Price> get_best_bid() const;
    std::optional<Price> get_best_ask() const;

    Quantity get_volume_at_price(Side side, Price price) const;
    size_t total_orders_count() const { return order_index_.size(); }
    bool is_empty() const { return order_index_.empty(); }

    void clear();
    void print_book(size_t depth = 5) const;

private:
    std::vector<Trade> match_buy_order(Order& incoming_buy);
    std::vector<Trade> match_sell_order(Order& incoming_sell);

    std::map<Price, std::list<Order>, std::greater<Price>> bids_;
    std::map<Price, std::list<Order>, std::less<Price>> asks_;
    std::unordered_map<OrderId, std::pair<Side, Price>> order_index_;
};

} // namespace lob
