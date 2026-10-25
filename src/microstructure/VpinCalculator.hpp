#pragma once

#include "../common/Types.hpp"
#include <vector>
#include <cmath>
#include <algorithm>
#include <deque>

namespace lob {

class VpinCalculator {
public:
    struct Bucket {
        Quantity buy_volume{0};
        Quantity sell_volume{0};
        
        Quantity total_volume() const { return buy_volume + sell_volume; }
        Quantity imbalance() const {
            return (buy_volume >= sell_volume) ? (buy_volume - sell_volume) : (sell_volume - buy_volume);
        }
    };

    /**
     * @param bucket_size Fixed volume per bucket (V_bucket).
     * @param window_size Number of buckets in the rolling historical window (N, typically 50).
     */
    explicit VpinCalculator(Quantity bucket_size = 5000, size_t window_size = 50)
        : bucket_size_(bucket_size),
          window_size_(window_size),
          current_bucket_{0, 0},
          last_trade_price_(0),
          last_trade_side_(Side::BUY)
    {
        completed_buckets_.resize(window_size_, {0, 0});
    }

    /**
     * @brief Process an incoming trade and update rolling volume buckets.
     * Uses the Tick Rule / Lee-Ready trade classifier.
     */
    void on_trade(Price price, Quantity quantity) {
        if (quantity == 0) return;

        // Determine trade initiator side using the Tick Rule
        Side side = last_trade_side_;
        if (last_trade_price_ != 0) {
            if (price > last_trade_price_) {
                side = Side::BUY;
            } else if (price < last_trade_price_) {
                side = Side::SELL;
            }
        }
        last_trade_price_ = price;
        last_trade_side_ = side;

        Quantity remaining = quantity;
        while (remaining > 0) {
            Quantity space_in_bucket = bucket_size_ - current_bucket_.total_volume();
            Quantity fill_amount = std::min(remaining, space_in_bucket);

            if (side == Side::BUY) {
                current_bucket_.buy_volume += fill_amount;
            } else {
                current_bucket_.sell_volume += fill_amount;
            }
            remaining -= fill_amount;

            // If current bucket is completely full, commit to rolling window
            if (current_bucket_.total_volume() >= bucket_size_) {
                rolling_imbalance_sum_ -= completed_buckets_[bucket_index_].imbalance();
                completed_buckets_[bucket_index_] = current_bucket_;
                rolling_imbalance_sum_ += current_bucket_.imbalance();

                bucket_index_ = (bucket_index_ + 1) % window_size_;
                if (filled_buckets_count_ < window_size_) {
                    filled_buckets_count_++;
                }

                current_bucket_ = {0, 0};
            }
        }
    }

    /**
     * @brief Calculate the current VPIN metric [0.0, 1.0].
     * VPIN = sum(|V_B - V_S|) / (N * V_bucket)
     */
    double calculate_vpin() const noexcept {
        if (filled_buckets_count_ == 0) return 0.0;

        uint64_t total_volume = static_cast<uint64_t>(filled_buckets_count_) * bucket_size_;
        return static_cast<double>(rolling_imbalance_sum_) / static_cast<double>(total_volume);
    }

    bool is_toxic(double toxicity_threshold = 0.70) const noexcept {
        return calculate_vpin() >= toxicity_threshold;
    }

    Quantity bucket_size() const noexcept { return bucket_size_; }
    size_t filled_buckets() const noexcept { return filled_buckets_count_; }
    size_t window_size() const noexcept { return window_size_; }

    void reset() {
        std::fill(completed_buckets_.begin(), completed_buckets_.end(), Bucket{0, 0});
        current_bucket_ = {0, 0};
        bucket_index_ = 0;
        filled_buckets_count_ = 0;
        rolling_imbalance_sum_ = 0;
        last_trade_price_ = 0;
        last_trade_side_ = Side::BUY;
    }

private:
    Quantity bucket_size_;
    size_t window_size_;
    std::vector<Bucket> completed_buckets_;
    size_t bucket_index_{0};
    size_t filled_buckets_count_{0};
    uint64_t rolling_imbalance_sum_{0};
    Bucket current_bucket_;

    Price last_trade_price_;
    Side last_trade_side_;
};

} // namespace lob
