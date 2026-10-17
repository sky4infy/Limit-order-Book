#pragma once

#include "OptimizedOrder.hpp"
#include "SlabAllocator.hpp"
#include <vector>
#include <cstdint>
#include <optional>
#include <cassert>

#if defined(_MSC_VER)
#include <intrin.h>
#endif

namespace lob {

// Hardware Bit-Scan Helpers (Compile to single-cycle BSF/BSR/TZCNT/LZCNT instructions)
namespace detail {

[[nodiscard]] inline int find_first_set_bit(uint64_t mask) noexcept {
#if defined(_MSC_VER)
    unsigned long index;
    if (_BitScanForward64(&index, mask)) {
        return static_cast<int>(index);
    }
    return -1;
#else
    if (mask == 0) return -1;
    return __builtin_ctzll(mask);
#endif
}

[[nodiscard]] inline int find_last_set_bit(uint64_t mask) noexcept {
#if defined(_MSC_VER)
    unsigned long index;
    if (_BitScanReverse64(&index, mask)) {
        return static_cast<int>(index);
    }
    return -1;
#else
    if (mask == 0) return -1;
    return 63 - __builtin_clzll(mask);
#endif
}

} // namespace detail

/**
 * @brief Price Level structure containing intrusive order queue head/tail pointers
 */
struct PriceLevel {
    Price    price{0};
    Quantity total_volume{0};
    uint32_t order_count{0};
    uint32_t head_order_idx{INVALID_INDEX};
    uint32_t tail_order_idx{INVALID_INDEX};

    [[nodiscard]] bool is_empty() const noexcept {
        return head_order_idx == INVALID_INDEX;
    }
};

/**
 * @brief Direct-Indexed Flat Price Ladder with Hierarchical Occupancy Bitmask
 * 
 * Replaces std::map<Price, std::list<Order>> with an O(1) contiguous array.
 * 
 * Performance Architecture:
 * - O(1) Direct Lookup: Direct array index by tick price (Index = Price).
 * - O(1) Best Bid / Best Offer (BBO): 2-level 64-bit occupancy bitmask. Finding the
 *   highest bid or lowest ask takes literally 2 CPU instructions (clz / ctz).
 * - Zero Allocations: Price levels are pre-allocated contiguous memory.
 * - Hardware Prefetcher Friendly: Consecutive levels reside contiguously in L2/L3 cache.
 */
template<size_t MaxPriceLevels = 131'072> // Supports tick prices from 0 to 131,071 (e.g. $0.00 to $1,310.71)
class DirectPriceLadder {
public:
    static constexpr size_t L1_WORDS = (MaxPriceLevels + 63) / 64;
    static constexpr size_t L2_WORDS = (L1_WORDS + 63) / 64;

    DirectPriceLadder() {
        levels_.resize(MaxPriceLevels);
        l1_mask_.resize(L1_WORDS, 0);
        l2_mask_.resize(L2_WORDS, 0);

        for (size_t i = 0; i < MaxPriceLevels; ++i) {
            levels_[i].price = static_cast<Price>(i);
        }
    }

    [[nodiscard]] PriceLevel& get_level(Price price) noexcept {
        assert(price < MaxPriceLevels && "Price exceeds MaxPriceLevels!");
        return levels_[price];
    }

    [[nodiscard]] const PriceLevel& get_level(Price price) const noexcept {
        assert(price < MaxPriceLevels && "Price exceeds MaxPriceLevels!");
        return levels_[price];
    }

    /**
     * @brief Mark a price level active in the hierarchical occupancy bitmask
     */
    void mark_active(Price price) noexcept {
        assert(price < MaxPriceLevels);
        size_t l1_idx = price / 64;
        size_t l1_bit = price % 64;
        l1_mask_[l1_idx] |= (1ULL << l1_bit);

        size_t l2_idx = l1_idx / 64;
        size_t l2_bit = l1_idx % 64;
        l2_mask_[l2_idx] |= (1ULL << l2_bit);
    }

    /**
     * @brief Mark a price level inactive in the bitmask when its queue becomes empty
     */
    void mark_inactive(Price price) noexcept {
        assert(price < MaxPriceLevels);
        size_t l1_idx = price / 64;
        size_t l1_bit = price % 64;
        l1_mask_[l1_idx] &= ~(1ULL << l1_bit);

        if (l1_mask_[l1_idx] == 0) {
            size_t l2_idx = l1_idx / 64;
            size_t l2_bit = l1_idx % 64;
            l2_mask_[l2_idx] &= ~(1ULL << l2_bit);
        }
    }

    /**
     * @brief Find the Highest Active Price (Best Bid) in O(1) via hardware bit scan
     */
    [[nodiscard]] std::optional<Price> get_highest_price() const noexcept {
        // Scan L2 mask downwards from top
        for (int64_t l2_idx = static_cast<int64_t>(L2_WORDS) - 1; l2_idx >= 0; --l2_idx) {
            uint64_t l2_word = l2_mask_[l2_idx];
            if (l2_word != 0) {
                int l2_bit = detail::find_last_set_bit(l2_word);
                size_t l1_idx = static_cast<size_t>(l2_idx) * 64 + static_cast<size_t>(l2_bit);

                uint64_t l1_word = l1_mask_[l1_idx];
                assert(l1_word != 0 && "L2 mask indicated active L1 word, but L1 word was 0!");
                int l1_bit = detail::find_last_set_bit(l1_word);

                Price best_price = static_cast<Price>(l1_idx * 64 + static_cast<size_t>(l1_bit));
                return best_price;
            }
        }
        return std::nullopt;
    }

    /**
     * @brief Find the Lowest Active Price (Best Ask) in O(1) via hardware bit scan
     */
    [[nodiscard]] std::optional<Price> get_lowest_price() const noexcept {
        // Scan L2 mask upwards from bottom
        for (size_t l2_idx = 0; l2_idx < L2_WORDS; ++l2_idx) {
            uint64_t l2_word = l2_mask_[l2_idx];
            if (l2_word != 0) {
                int l2_bit = detail::find_first_set_bit(l2_word);
                size_t l1_idx = l2_idx * 64 + static_cast<size_t>(l2_bit);

                uint64_t l1_word = l1_mask_[l1_idx];
                assert(l1_word != 0 && "L2 mask indicated active L1 word, but L1 word was 0!");
                int l1_bit = detail::find_first_set_bit(l1_word);

                Price best_price = static_cast<Price>(l1_idx * 64 + static_cast<size_t>(l1_bit));
                return best_price;
            }
        }
        return std::nullopt;
    }

    /**
     * @brief Find the next active price strictly below the given price
     */
    [[nodiscard]] std::optional<Price> get_next_lower_price(Price price) const noexcept {
        if (price == 0) return std::nullopt;
        size_t target_l1 = price / 64;
        size_t bit_pos = price % 64;

        // Check current L1 word below bit_pos
        if (bit_pos > 0) {
            uint64_t mask = (1ULL << bit_pos) - 1;
            uint64_t word = l1_mask_[target_l1] & mask;
            if (word != 0) {
                int bit = detail::find_last_set_bit(word);
                return static_cast<Price>(target_l1 * 64 + static_cast<size_t>(bit));
            }
        }

        if (target_l1 == 0) return std::nullopt;

        // Search previous L1 words
        size_t curr_l1 = target_l1 - 1;
        while (true) {
            size_t l2_idx = curr_l1 / 64;
            size_t l2_bit = curr_l1 % 64;
            uint64_t l2_mask = (l2_bit == 63) ? ~0ULL : ((1ULL << (l2_bit + 1)) - 1);
            uint64_t l2_word = l2_mask_[l2_idx] & l2_mask;

            if (l2_word != 0) {
                int active_l2_bit = detail::find_last_set_bit(l2_word);
                size_t active_l1 = l2_idx * 64 + static_cast<size_t>(active_l2_bit);
                uint64_t l1_word = l1_mask_[active_l1];
                int bit = detail::find_last_set_bit(l1_word);
                return static_cast<Price>(active_l1 * 64 + static_cast<size_t>(bit));
            }

            if (l2_idx == 0) break;
            curr_l1 = (l2_idx * 64) - 1;
        }

        return std::nullopt;
    }

    /**
     * @brief Find the next active price strictly above the given price
     */
    [[nodiscard]] std::optional<Price> get_next_higher_price(Price price) const noexcept {
        if (price + 1 >= MaxPriceLevels) return std::nullopt;
        size_t target_l1 = (price + 1) / 64;
        size_t bit_pos = (price + 1) % 64;

        // Check current L1 word at or above bit_pos
        uint64_t mask = (bit_pos == 0) ? ~0ULL : (~0ULL << bit_pos);
        uint64_t word = l1_mask_[target_l1] & mask;
        if (word != 0) {
            int bit = detail::find_first_set_bit(word);
            return static_cast<Price>(target_l1 * 64 + static_cast<size_t>(bit));
        }

        // Search subsequent L1 words
        size_t curr_l1 = target_l1 + 1;
        while (curr_l1 < L1_WORDS) {
            size_t l2_idx = curr_l1 / 64;
            size_t l2_bit = curr_l1 % 64;
            uint64_t l2_mask = (l2_bit == 0) ? ~0ULL : (~0ULL << l2_bit);
            uint64_t l2_word = l2_mask_[l2_idx] & l2_mask;

            if (l2_word != 0) {
                int active_l2_bit = detail::find_first_set_bit(l2_word);
                size_t active_l1 = l2_idx * 64 + static_cast<size_t>(active_l2_bit);
                uint64_t l1_word = l1_mask_[active_l1];
                int bit = detail::find_first_set_bit(l1_word);
                return static_cast<Price>(active_l1 * 64 + static_cast<size_t>(bit));
            }

            curr_l1 = (l2_idx + 1) * 64;
        }

        return std::nullopt;
    }

    /**
     * @brief Append order to the tail of a price level (FIFO Time Priority)
     */
    template<typename Pool>
    void append_order(Price price, uint32_t order_idx, Pool& pool) noexcept {
        PriceLevel& level = get_level(price);
        OptimizedOrder& ord = pool.get(order_idx);

        ord.prev_idx = level.tail_order_idx;
        ord.next_idx = INVALID_INDEX;

        if (level.tail_order_idx != INVALID_INDEX) {
            pool.get(level.tail_order_idx).next_idx = order_idx;
        } else {
            level.head_order_idx = order_idx;
        }

        level.tail_order_idx = order_idx;
        level.total_volume += ord.quantity;
        ++level.order_count;

        mark_active(price);
    }

    /**
     * @brief Unlink order from its price level in O(1)
     */
    template<typename Pool>
    void unlink_order(Price price, uint32_t order_idx, Pool& pool) noexcept {
        PriceLevel& level = get_level(price);
        OptimizedOrder& ord = pool.get(order_idx);

        if (ord.prev_idx != INVALID_INDEX) {
            pool.get(ord.prev_idx).next_idx = ord.next_idx;
        } else {
            level.head_order_idx = ord.next_idx;
        }

        if (ord.next_idx != INVALID_INDEX) {
            pool.get(ord.next_idx).prev_idx = ord.prev_idx;
        } else {
            level.tail_order_idx = ord.prev_idx;
        }

        level.total_volume -= ord.quantity;
        --level.order_count;

        ord.prev_idx = INVALID_INDEX;
        ord.next_idx = INVALID_INDEX;

        if (level.is_empty()) {
            mark_inactive(price);
        }
    }

    void clear() noexcept {
        for (auto& lvl : levels_) {
            lvl.total_volume = 0;
            lvl.order_count = 0;
            lvl.head_order_idx = INVALID_INDEX;
            lvl.tail_order_idx = INVALID_INDEX;
        }
        std::fill(l1_mask_.begin(), l1_mask_.end(), 0);
        std::fill(l2_mask_.begin(), l2_mask_.end(), 0);
    }

private:
    std::vector<PriceLevel> levels_;
    std::vector<uint64_t>   l1_mask_;
    std::vector<uint64_t>   l2_mask_;
};

} // namespace lob
