#pragma once

#include "../common/Types.hpp"
#include <cmath>
#include <algorithm>
#include <iostream>

namespace lob {

struct MarketMakerQuotes {
    Price bid_price;
    Price ask_price;
    Quantity quote_size;
    double reservation_price;
    double half_spread;
};

class AvellanedaStoikovBot {
public:
    /**
     * @param gamma Risk aversion coefficient (e.g. 0.05 to 0.5)
     * @param sigma Asset price volatility (e.g. 1.5)
     * @param kappa Order arrival intensity / book liquidity density (e.g. 1.5)
     * @param quote_size Standard lot size for active quotes
     */
    AvellanedaStoikovBot(double gamma = 0.1, double sigma = 2.0, double kappa = 1.5, Quantity quote_size = 100)
        : gamma_(gamma),
          sigma_(sigma),
          kappa_(kappa),
          quote_size_(quote_size),
          inventory_(0),
          cash_(0.0),
          last_mid_price_(10000.0) {}

    /**
     * @brief Calculate optimal reservation price:
     * R(s, q, t) = s - q * gamma * sigma^2 * (T - t)
     */
    double calculate_reservation_price(double mid_price, double time_remaining = 1.0) const noexcept {
        return mid_price - static_cast<double>(inventory_) * gamma_ * (sigma_ * sigma_) * time_remaining;
    }

    /**
     * @brief Compute optimal bid and ask quotes skewed by inventory risk.
     */
    MarketMakerQuotes compute_optimal_quotes(double mid_price, double time_remaining = 1.0) {
        last_mid_price_ = mid_price;

        double reservation = calculate_reservation_price(mid_price, time_remaining);

        // Optimal total spread: s(t) = gamma * sigma^2 * (T - t) + (2 / gamma) * ln(1 + gamma / kappa)
        double spread_base = (2.0 / gamma_) * std::log(1.0 + (gamma_ / kappa_));
        double half_spread = 0.5 * spread_base;
        if (half_spread < 1.0) half_spread = 1.0; // Minimum 1 tick

        Price optimal_bid = static_cast<Price>(std::max(1.0, std::round(reservation - half_spread)));
        Price optimal_ask = static_cast<Price>(std::max(static_cast<double>(optimal_bid + 1), std::round(reservation + half_spread)));

        return MarketMakerQuotes{
            optimal_bid,
            optimal_ask,
            quote_size_,
            reservation,
            half_spread
        };
    }

    // Trade execution handlers
    void on_bid_filled(Price fill_price, Quantity qty) noexcept {
        inventory_ += static_cast<int64_t>(qty);
        cash_ -= static_cast<double>(fill_price * qty);
    }

    void on_ask_filled(Price fill_price, Quantity qty) noexcept {
        inventory_ -= static_cast<int64_t>(qty);
        cash_ += static_cast<double>(fill_price * qty);
    }

    int64_t inventory() const noexcept { return inventory_; }
    double cash() const noexcept { return cash_; }

    // Mark-to-market total portfolio value
    double mark_to_market_pnl(double current_mid) const noexcept {
        return cash_ + static_cast<double>(inventory_) * current_mid;
    }

    void set_risk_aversion(double gamma) noexcept { gamma_ = gamma; }
    void set_volatility(double sigma) noexcept { sigma_ = sigma; }
    void set_kappa(double kappa) noexcept { kappa_ = kappa; }

private:
    double gamma_;
    double sigma_;
    double kappa_;
    Quantity quote_size_;

    int64_t inventory_;
    double cash_;
    double last_mid_price_;
};

} // namespace lob
