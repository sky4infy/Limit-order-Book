#pragma once

#include "../common/Types.hpp"
#include <vector>
#include <cmath>
#include <numeric>

namespace lob {

class MicroPriceEstimator {
public:
    /**
     * @brief Sasha Stoikov's Top-of-Book Micro-Price.
     * 
     * Computes the probability-weighted fair price adjusted for queue imbalance:
     *   Imbalance I = Q_b / (Q_b + Q_a)
     *   MicroPrice = P_b + I * (P_a - P_b) = I * P_a + (1 - I) * P_b
     * 
     * If bid queue is 90% of total volume, fair price is 90% of the way towards the ask price.
     */
    static inline double calculate_tob_micro_price(Price bid_price, Quantity bid_qty,
                                                   Price ask_price, Quantity ask_qty) noexcept 
    {
        uint64_t total_qty = static_cast<uint64_t>(bid_qty) + static_cast<uint64_t>(ask_qty);
        if (total_qty == 0) [[unlikely]] {
            return static_cast<double>(bid_price + ask_price) * 0.5;
        }

        double imbalance = static_cast<double>(bid_qty) / static_cast<double>(total_qty);
        return static_cast<double>(bid_price) + imbalance * static_cast<double>(ask_price - bid_price);
    }

    /**
     * @brief Multi-Level (L2 Depth) Weighted Micro-Price.
     * 
     * Incorporates depth across N levels with harmonic decay weights (w_k = 1 / k).
     */
    struct Level {
        Price price;
        Quantity qty;
    };

    static inline double calculate_multilevel_micro_price(
        const std::vector<Level>& bids,
        const std::vector<Level>& asks,
        size_t max_depth = 5) noexcept
    {
        if (bids.empty() || asks.empty()) return 0.0;

        size_t depth = std::min({bids.size(), asks.size(), max_depth});
        if (depth == 0) return 0.0;

        double weighted_price_sum = 0.0;
        double total_weight = 0.0;

        for (size_t k = 0; k < depth; ++k) {
            double weight = 1.0 / static_cast<double>(k + 1);
            double level_mp = calculate_tob_micro_price(bids[k].price, bids[k].qty,
                                                       asks[k].price, asks[k].qty);
            weighted_price_sum += weight * level_mp;
            total_weight += weight;
        }

        return (total_weight > 0.0) ? (weighted_price_sum / total_weight) : 0.0;
    }
};

} // namespace lob
