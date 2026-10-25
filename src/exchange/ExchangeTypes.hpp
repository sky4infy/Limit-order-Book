#pragma once

#include <cstdint>
#include <string>
#include "../common/Types.hpp"

namespace lob {

enum class StpPolicy : uint8_t {
    NONE = 0,
    CANCEL_MAKER = 1,
    CANCEL_TAKER = 2,
    DECREMENT_AND_CANCEL = 3,
    CANCEL_BOTH = 4
};

enum class AdvancedOrderType : uint8_t {
    STANDARD_LIMIT = 0,
    ICEBERG = 1,
    MARKET_ON_OPEN = 2,
    LIMIT_ON_OPEN = 3
};

struct ExecutionFill {
    uint64_t maker_order_id;
    uint64_t taker_order_id;
    uint32_t firm_id;
    Price price;
    Quantity quantity;
    bool maker_completed;
    bool taker_completed;
};

struct AuctionResult {
    Price clearing_price{0};
    Quantity matched_volume{0};
    Quantity buy_surplus{0};
    Quantity sell_surplus{0};
    Side imbalance_side{Side::BUY};
    bool valid{false};
};

} // namespace lob
