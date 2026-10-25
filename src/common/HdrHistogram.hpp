#pragma once

#include <cstdint>
#include <vector>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <iomanip>
#include <string>
#include <bit>

namespace lob {

/**
 * @brief Zero-allocation, high-precision High Dynamic Range (HDR) Latency Histogram.
 * 
 * Inspired by Gil Tene's HdrHistogram, this data structure records latency distributions
 * across a massive dynamic range (1 ns to 1 hour = 3.6e12 ns) with configurable precision
 * (e.g. 3 significant decimal digits, ~0.1% resolution) without dynamic allocations on the hot path.
 * 
 * Features:
 * - Sub-nanosecond bucket indexing using hardware LZCNT (std::countl_zero).
 * - Full support for Gil Tene's Coordinated Omission correction algorithm:
 *   record_with_expected_interval() backfills missing queue delays caused by engine stalls.
 * - Accurate percentile queries (p50, p90, p99, p99.9, p99.99, p99.999, Max).
 */
class HdrHistogram {
public:
    /**
     * @brief Construct an HDR Histogram with specified range and precision.
     * @param highest_trackable_value Max value trackable (default: 3.6e12 ns = 1 hour).
     * @param significant_figures Number of significant decimal digits (1 to 4, default: 3).
     */
    explicit HdrHistogram(uint64_t highest_trackable_value = 3'600'000'000'000ULL, 
                          uint32_t significant_figures = 3)
        : highest_trackable_value_(highest_trackable_value),
          significant_figures_(std::clamp(significant_figures, 1u, 4u)) 
    {
        init();
    }

    // Hot path: record a single latency sample
    inline void record(uint64_t value) noexcept {
        if (value > highest_trackable_value_) [[unlikely]] {
            value = highest_trackable_value_;
        }
        
        size_t idx = value_to_index(value);
        counts_[idx]++;
        total_count_++;

        if (value < min_value_) min_value_ = value;
        if (value > max_value_) max_value_ = value;
        sum_ += value;
    }

    /**
     * @brief Gil Tene's Coordinated Omission Correction.
     * 
     * In an open-loop system with expected arrival interval D:
     * If a single request takes time T > D, it blocked the system for T / D intervals.
     * Those (T / D - 1) omitted requests were delayed in the arrival queue and must be
     * accounted for at their actual experienced queue wait times:
     *   T - D, T - 2*D, ..., until < D.
     */
    inline void record_with_expected_interval(uint64_t value, uint64_t expected_interval) noexcept {
        record(value);
        if (expected_interval == 0 || value <= expected_interval) {
            return;
        }

        uint64_t missing_value = value - expected_interval;
        while (missing_value > 0) {
            record(missing_value);
            if (missing_value <= expected_interval) break;
            missing_value -= expected_interval;
        }
    }

    [[nodiscard]] uint64_t total_count() const noexcept { return total_count_; }
    [[nodiscard]] uint64_t min_value() const noexcept { return total_count_ == 0 ? 0 : min_value_; }
    [[nodiscard]] uint64_t max_value() const noexcept { return total_count_ == 0 ? 0 : max_value_; }
    
    [[nodiscard]] double mean() const noexcept {
        return total_count_ == 0 ? 0.0 : static_cast<double>(sum_) / static_cast<double>(total_count_);
    }

    /**
     * @brief Query the value at a given percentile (e.g., 50.0 for p50, 99.9 for p99.9).
     */
    [[nodiscard]] uint64_t value_at_percentile(double percentile) const noexcept {
        if (total_count_ == 0) return 0;
        if (percentile <= 0.0) return min_value_;
        if (percentile >= 100.0) return max_value_;

        const double target_count_dbl = (percentile / 100.0) * static_cast<double>(total_count_);
        const uint64_t target_count = static_cast<uint64_t>(std::ceil(target_count_dbl));

        uint64_t accumulated = 0;
        for (size_t i = 0; i < counts_.size(); ++i) {
            accumulated += counts_[i];
            if (accumulated >= target_count) {
                return highest_equivalent_value(index_to_value(i));
            }
        }
        return max_value_;
    }

    /**
     * @brief Reset all counts and statistics for reuse.
     */
    void reset() noexcept {
        std::fill(counts_.begin(), counts_.end(), 0ULL);
        total_count_ = 0;
        min_value_ = UINT64_MAX;
        max_value_ = 0;
        sum_ = 0;
    }

    /**
     * @brief Print a formatted percentile distribution table.
     */
    void print_percentile_table(std::ostream& os, const std::string& title = "LATENCY DISTRIBUTION", double scale_factor = 1.0, const std::string& unit = "ns") const {
        os << "\n====================================================================\n";
        os << "  " << title << "\n";
        os << "====================================================================\n";
        os << "  Total Samples : " << total_count_ << "\n";
        os << "  Min           : " << std::fixed << std::setprecision(2) << (min_value() * scale_factor) << " " << unit << "\n";
        os << "  Mean          : " << std::fixed << std::setprecision(2) << (mean() * scale_factor) << " " << unit << "\n";
        os << "  Max           : " << std::fixed << std::setprecision(2) << (max_value() * scale_factor) << " " << unit << "\n";
        os << "--------------------------------------------------------------------\n";
        os << "  Percentile          Value (" << unit << ")           Total Count <= Value\n";
        os << "--------------------------------------------------------------------\n";

        static const double percentiles[] = {
            10.0, 25.0, 50.0, 75.0, 90.0, 95.0, 99.0, 99.9, 99.99, 99.999, 100.0
        };

        for (double p : percentiles) {
            uint64_t val = (p == 100.0) ? max_value() : value_at_percentile(p);
            os << "  p" << std::left << std::setw(17) << (std::to_string(p).substr(0, p >= 99.0 ? 6 : 4))
               << std::right << std::setw(12) << std::fixed << std::setprecision(1) << (val * scale_factor)
               << " " << unit << "\n";
        }
        os << "====================================================================\n";
    }

private:
    uint64_t highest_trackable_value_;
    uint32_t significant_figures_;

    uint32_t sub_bucket_count_{0};
    uint32_t sub_bucket_half_count_{0};
    uint32_t sub_bucket_half_count_magnitude_{0};
    uint32_t sub_bucket_mask_{0};
    uint32_t bucket_count_{0};

    std::vector<uint64_t> counts_;
    uint64_t total_count_{0};
    uint64_t min_value_{UINT64_MAX};
    uint64_t max_value_{0};
    uint64_t sum_{0};

    void init() {
        // Compute sub_bucket_count = 2^(ceil(log2(10^significant_figures)))
        // 1 sigfig -> 16
        // 2 sigfig -> 128
        // 3 sigfig -> 1024 or 2048
        // 4 sigfig -> 16384
        uint32_t largest_value_with_sig_figs = static_cast<uint32_t>(std::pow(10, significant_figures_));
        uint32_t sub_bucket_count_mag = static_cast<uint32_t>(std::ceil(std::log2(largest_value_with_sig_figs)));
        if (sub_bucket_count_mag < 1) sub_bucket_count_mag = 1;

        sub_bucket_half_count_magnitude_ = sub_bucket_count_mag;
        sub_bucket_count_ = 1u << (sub_bucket_half_count_magnitude_ + 1);
        sub_bucket_half_count_ = sub_bucket_count_ / 2;
        sub_bucket_mask_ = sub_bucket_count_ - 1;

        // Number of buckets required to cover highest_trackable_value
        // Determine bit width of highest_trackable_value
        uint32_t highest_val_bits = 64 - std::countl_zero(highest_trackable_value_);
        if (highest_val_bits <= (sub_bucket_half_count_magnitude_ + 1)) {
            bucket_count_ = 1;
        } else {
            bucket_count_ = highest_val_bits - (sub_bucket_half_count_magnitude_ + 1) + 1;
        }

        // Total array length
        size_t total_slots = (bucket_count_ + 1) * (sub_bucket_count_ / 2);
        counts_.assign(total_slots, 0ULL);
    }

    [[nodiscard]] inline size_t value_to_index(uint64_t value) const noexcept {
        if (value < sub_bucket_count_) {
            return static_cast<size_t>(value);
        }

        // Number of bits needed to represent value
        uint32_t bits = 64 - std::countl_zero(value);
        uint32_t bucket_index = bits - (sub_bucket_half_count_magnitude_ + 1);
        if (bucket_index >= bucket_count_) {
            bucket_index = bucket_count_ - 1;
        }

        uint32_t sub_bucket_index = static_cast<uint32_t>(value >> bucket_index) & sub_bucket_mask_;
        
        // Offset in the counts array:
        // First bucket has sub_bucket_count slots.
        // Subsequent buckets add sub_bucket_half_count slots each.
        size_t index = (static_cast<size_t>(bucket_index) + 1) * sub_bucket_half_count_ + (sub_bucket_index & (sub_bucket_half_count_ - 1));
        if (index >= counts_.size()) [[unlikely]] {
            index = counts_.size() - 1;
        }
        return index;
    }

    [[nodiscard]] inline uint64_t index_to_value(size_t index) const noexcept {
        if (index < sub_bucket_count_) {
            return static_cast<uint64_t>(index);
        }

        uint32_t bucket_index = static_cast<uint32_t>((index / sub_bucket_half_count_) - 1);
        uint32_t sub_bucket_index = static_cast<uint32_t>(index % sub_bucket_half_count_) + sub_bucket_half_count_;

        return static_cast<uint64_t>(sub_bucket_index) << bucket_index;
    }

    [[nodiscard]] inline uint64_t highest_equivalent_value(uint64_t value) const noexcept {
        if (value < sub_bucket_count_) {
            return value;
        }
        uint32_t bits = 64 - std::countl_zero(value);
        uint32_t bucket_index = bits - (sub_bucket_half_count_magnitude_ + 1);
        uint64_t unit_size = 1ULL << bucket_index;
        return value + unit_size - 1;
    }
};

} // namespace lob
