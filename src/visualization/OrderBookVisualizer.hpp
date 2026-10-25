#pragma once

#include "../common/Types.hpp"
#include "../microstructure/MicroPrice.hpp"
#include "../microstructure/VpinCalculator.hpp"
#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <algorithm>

namespace lob {

struct DepthLevel {
    Price price;
    Quantity quantity;
    size_t order_count;
};

class OrderBookVisualizer {
public:
    static void render_l3_dashboard(
        std::ostream& os,
        const std::string& symbol,
        const std::vector<DepthLevel>& bids,
        const std::vector<DepthLevel>& asks,
        double vpin_metric,
        uint64_t total_orders,
        uint64_t total_trades,
        uint64_t journal_seq)
    {
        os << "\n====================================================================================================\n";
        os << "                       INSTITUTIONAL L3 MARKET DEPTH & RISK MONITOR: " << symbol << "\n";
        os << "====================================================================================================\n";

        Price best_bid = bids.empty() ? 0 : bids[0].price;
        Price best_ask = asks.empty() ? 0 : asks[0].price;
        Quantity best_bid_qty = bids.empty() ? 0 : bids[0].quantity;
        Quantity best_ask_qty = asks.empty() ? 0 : asks[0].quantity;

        double mid = (best_bid > 0 && best_ask > 0) ? (static_cast<double>(best_bid + best_ask) * 0.5) : 0.0;
        double micro_price = (best_bid > 0 && best_ask > 0) 
            ? MicroPriceEstimator::calculate_tob_micro_price(best_bid, best_bid_qty, best_ask, best_ask_qty)
            : mid;

        int64_t spread_ticks = (best_bid > 0 && best_ask > 0) ? (static_cast<int64_t>(best_ask) - static_cast<int64_t>(best_bid)) : 0;
        double spread_bps = (mid > 0.0) ? ((static_cast<double>(spread_ticks) / mid) * 10000.0) : 0.0;

        // Header Metrics
        os << "  Best Bid : " << std::setw(8) << best_bid << " (" << std::setw(6) << best_bid_qty << " shs) | "
           << "Spread : " << spread_ticks << " ticks (" << std::fixed << std::setprecision(1) << spread_bps << " bps)\n";
        os << "  Best Ask : " << std::setw(8) << best_ask << " (" << std::setw(6) << best_ask_qty << " shs) | "
           << "Mid: " << std::fixed << std::setprecision(2) << mid << " | Micro-Price: " << micro_price << "\n";

        // VPIN Toxicity Gauge
        std::string toxicity_label;
        if (vpin_metric < 0.35) {
            toxicity_label = "[NORMAL - NOISE FLOW]";
        } else if (vpin_metric < 0.70) {
            toxicity_label = "[ELEVATED - MONITORING]";
        } else {
            toxicity_label = "[CRITICAL - TOXIC RUN DETECTED]";
        }

        os << "  VPIN Toxicity : " << std::fixed << std::setprecision(3) << vpin_metric << " " << toxicity_label << " | "
           << "Engine Seq: #" << journal_seq << " | Fills: " << total_trades << "\n";
        os << "----------------------------------------------------------------------------------------------------\n";

        // Ladder Visualization
        os << std::left << std::setw(28) << "          BIDS (BUY)" 
           << " | " 
           << std::left << std::setw(28) << "          ASKS (SELL)" << "\n";
        os << "  Orders   Qty      Price    Depth   |   Price    Qty     Orders   Depth\n";
        os << "-------------------------------------+--------------------------------------------------------------\n";

        size_t max_rows = std::min<size_t>(10, std::max(bids.size(), asks.size()));
        Quantity max_depth_vol = 1;
        for (const auto& b : bids) max_depth_vol = std::max(max_depth_vol, b.quantity);
        for (const auto& a : asks) max_depth_vol = std::max(max_depth_vol, a.quantity);

        for (size_t i = 0; i < max_rows; ++i) {
            // Bid side
            if (i < bids.size()) {
                size_t bar_len = static_cast<size_t>((static_cast<double>(bids[i].quantity) / max_depth_vol) * 10);
                std::string bar(bar_len, '#');
                os << "  #" << std::setw(5) << bids[i].order_count 
                   << std::setw(8) << bids[i].quantity 
                   << std::setw(9) << bids[i].price 
                   << std::left << std::setw(10) << bar;
            } else {
                os << std::string(36, ' ');
            }

            os << " | ";

            // Ask side
            if (i < asks.size()) {
                size_t bar_len = static_cast<size_t>((static_cast<double>(asks[i].quantity) / max_depth_vol) * 10);
                std::string bar(bar_len, '#');
                os << "  " << std::setw(8) << asks[i].price 
                   << std::setw(8) << asks[i].quantity 
                   << "#" << std::setw(6) << asks[i].order_count 
                   << std::left << std::setw(10) << bar;
            }

            os << "\n";
        }

        os << "====================================================================================================\n";
    }
};

} // namespace lob
