#pragma once

#include "../common/Types.hpp"
#include "ExchangeTypes.hpp"
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <iostream>

namespace lob {

struct IcebergState {
    uint64_t order_id;
    uint32_t firm_id;
    Side side;
    Price price;
    Quantity total_quantity;
    Quantity peak_quantity;       // Max visible display tranche
    Quantity current_displayed;   // Currently active in the ladder
    Quantity hidden_remaining;    // Hidden pool waiting for replenishment
    uint64_t current_slice_ts;    // Timestamp of the current display slice
    bool active{true};
};

enum class StpAction {
    CONTINUE_MATCHING,
    HALT_TAKER_CANCELLED,
    MAKER_CANCELLED_CONTINUE
};

class AdvancedOrderManager {
public:
    // Iceberg registration
    void register_iceberg(uint64_t order_id, uint32_t firm_id, Side side, Price price, 
                          Quantity total_qty, Quantity peak_qty, uint64_t timestamp) 
    {
        Quantity initial_display = std::min(total_qty, peak_qty);
        Quantity hidden = total_qty - initial_display;

        IcebergState state{
            order_id,
            firm_id,
            side,
            price,
            total_qty,
            peak_qty,
            initial_display,
            hidden,
            timestamp,
            true
        };
        icebergs_[order_id] = state;
    }

    bool is_iceberg(uint64_t order_id) const {
        return icebergs_.find(order_id) != icebergs_.end();
    }

    IcebergState* get_iceberg(uint64_t order_id) {
        auto it = icebergs_.find(order_id);
        if (it != icebergs_.end()) return &it->second;
        return nullptr;
    }

    // Handles execution of displayed quantity. Returns true if a new tranche was replenished.
    bool on_slice_fill(uint64_t order_id, Quantity filled_qty, uint64_t new_timestamp, Quantity& out_new_slice_qty) {
        auto it = icebergs_.find(order_id);
        if (it == icebergs_.end()) return false;

        IcebergState& ice = it->second;
        if (filled_qty >= ice.current_displayed) {
            ice.current_displayed = 0;
        } else {
            ice.current_displayed -= filled_qty;
        }

        // Replenish if displayed hit 0 and hidden reserves exist
        if (ice.current_displayed == 0 && ice.hidden_remaining > 0) {
            Quantity replenish_qty = std::min(ice.hidden_remaining, ice.peak_quantity);
            ice.current_displayed = replenish_qty;
            ice.hidden_remaining -= replenish_qty;
            ice.current_slice_ts = new_timestamp;
            out_new_slice_qty = replenish_qty;
            return true; // Slice replenished, needs re-insertion into book queue with new timestamp!
        }

        if (ice.current_displayed == 0 && ice.hidden_remaining == 0) {
            ice.active = false;
        }
        return false;
    }

    // Self-Trade Prevention Engine
    // Evaluates match between taker and maker. Returns action code and adjusts quantities.
    static StpAction evaluate_stp(
        StpPolicy policy,
        uint32_t taker_firm,
        uint32_t maker_firm,
        Quantity& taker_qty,
        Quantity& maker_qty,
        bool& out_trade_allowed)
    {
        // If different firms or policy NONE, trade proceeds normally
        if (taker_firm != maker_firm || policy == StpPolicy::NONE) {
            out_trade_allowed = true;
            return StpAction::CONTINUE_MATCHING;
        }

        // Self-trade detected!
        out_trade_allowed = false;

        switch (policy) {
            case StpPolicy::CANCEL_MAKER:
                // Maker is cancelled, taker keeps entire remaining quantity and matches next depth
                maker_qty = 0;
                return StpAction::MAKER_CANCELLED_CONTINUE;

            case StpPolicy::CANCEL_TAKER:
                // Taker is cancelled immediately, maker remains intact
                taker_qty = 0;
                return StpAction::HALT_TAKER_CANCELLED;

            case StpPolicy::CANCEL_BOTH:
                // Both orders are cancelled
                taker_qty = 0;
                maker_qty = 0;
                return StpAction::HALT_TAKER_CANCELLED;

            case StpPolicy::DECREMENT_AND_CANCEL:
                if (taker_qty == maker_qty) {
                    taker_qty = 0;
                    maker_qty = 0;
                    return StpAction::HALT_TAKER_CANCELLED;
                } else if (taker_qty > maker_qty) {
                    taker_qty -= maker_qty;
                    maker_qty = 0;
                    return StpAction::MAKER_CANCELLED_CONTINUE;
                } else {
                    maker_qty -= taker_qty;
                    taker_qty = 0;
                    return StpAction::HALT_TAKER_CANCELLED;
                }

            default:
                out_trade_allowed = true;
                return StpAction::CONTINUE_MATCHING;
        }
    }

private:
    std::unordered_map<uint64_t, IcebergState> icebergs_;
};

} // namespace lob
