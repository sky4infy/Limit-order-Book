#pragma once

#include "OptimizedOrder.hpp"
#include <vector>
#include <cstdint>
#include <cassert>

namespace lob {

/**
 * @brief Zero-Allocation Open-Addressing Hash Table for OrderId -> PoolIndex
 * 
 * Replaces std::unordered_map on the hot path. Standard library unordered_map allocates
 * an internal bucket node on EVERY insert, defeating zero-allocation goals.
 * 
 * Performance Highlights:
 * - Pre-allocated contiguous flat array of slots.
 * - Power-of-two size with bitwise masking (hash & (Capacity - 1)).
 * - Linear probing for spatial cache locality.
 * - Backward-shift deletion to avoid tombstone degradation.
 * - ZERO dynamic memory allocations during trading.
 */
template<size_t Capacity = 262'144> // Must be power of 2
class FlatOrderIndex {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity must be a power of 2!");

public:
    struct Entry {
        OrderId  order_id{0};
        uint32_t pool_idx{INVALID_INDEX};

        [[nodiscard]] bool is_empty() const noexcept {
            return pool_idx == INVALID_INDEX;
        }
    };

    FlatOrderIndex() {
        table_.resize(Capacity);
    }

    /**
     * @brief Insert or update order_id -> pool_idx mapping
     * @return true on success, false if table is full
     */
    bool insert(OrderId order_id, uint32_t pool_idx) noexcept {
        assert(order_id != 0 && "OrderId cannot be 0!");
        assert(pool_idx != INVALID_INDEX && "Pool index cannot be INVALID_INDEX!");

        size_t idx = hash(order_id) & MASK;

        for (size_t probe = 0; probe < Capacity; ++probe) {
            Entry& entry = table_[idx];

            if (entry.is_empty()) {
                entry.order_id = order_id;
                entry.pool_idx = pool_idx;
                ++count_;
                return true;
            }

            if (entry.order_id == order_id) {
                entry.pool_idx = pool_idx; // Update existing
                return true;
            }

            idx = (idx + 1) & MASK;
        }

        return false; // Table exhausted
    }

    /**
     * @brief Lookup pool_idx for a given order_id
     * @return pool_idx if found, or INVALID_INDEX if not found
     */
    [[nodiscard]] uint32_t find(OrderId order_id) const noexcept {
        if (order_id == 0) return INVALID_INDEX;

        size_t idx = hash(order_id) & MASK;

        for (size_t probe = 0; probe < Capacity; ++probe) {
            const Entry& entry = table_[idx];

            if (entry.is_empty()) {
                return INVALID_INDEX; // Not found
            }

            if (entry.order_id == order_id) {
                return entry.pool_idx;
            }

            idx = (idx + 1) & MASK;
        }

        return INVALID_INDEX;
    }

    /**
     * @brief Remove order_id from index using backward-shift deletion (Robin Hood principle)
     * @return true if found and removed, false if not found
     */
    bool erase(OrderId order_id) noexcept {
        if (order_id == 0) return false;

        size_t idx = hash(order_id) & MASK;

        for (size_t probe = 0; probe < Capacity; ++probe) {
            Entry& entry = table_[idx];

            if (entry.is_empty()) {
                return false; // Not found
            }

            if (entry.order_id == order_id) {
                // Found: perform backward shift deletion to preserve cluster integrity
                size_t curr = idx;
                size_t next = (curr + 1) & MASK;

                while (!table_[next].is_empty()) {
                    size_t natural_slot = hash(table_[next].order_id) & MASK;
                    
                    // Check if next item's natural home is <= curr (wrapping considered)
                    bool can_shift = false;
                    if (next >= curr) {
                        can_shift = (natural_slot <= curr) || (natural_slot > next);
                    } else {
                        can_shift = (natural_slot <= curr) && (natural_slot > next);
                    }

                    if (can_shift) {
                        table_[curr] = table_[next];
                        curr = next;
                    }
                    next = (next + 1) & MASK;
                }

                // Clear the final shifted slot
                table_[curr].order_id = 0;
                table_[curr].pool_idx = INVALID_INDEX;
                --count_;
                return true;
            }

            idx = (idx + 1) & MASK;
        }

        return false;
    }

    [[nodiscard]] bool contains(OrderId order_id) const noexcept {
        return find(order_id) != INVALID_INDEX;
    }

    void clear() noexcept {
        for (auto& entry : table_) {
            entry.order_id = 0;
            entry.pool_idx = INVALID_INDEX;
        }
        count_ = 0;
    }

    [[nodiscard]] size_t size() const noexcept {
        return count_;
    }

    [[nodiscard]] bool is_empty() const noexcept {
        return count_ == 0;
    }

private:
    static constexpr size_t MASK = Capacity - 1;

    // Fast 64-bit integer mixing hash (Murmur3 / Stafford 13)
    [[nodiscard]] static constexpr size_t hash(OrderId x) noexcept {
        x ^= x >> 30;
        x *= 0xbf58476d1ce4e5b9ULL;
        x ^= x >> 27;
        x *= 0x94d049bb133111ebULL;
        x ^= x >> 31;
        return static_cast<size_t>(x);
    }

    std::vector<Entry> table_;
    size_t count_{0};
};

} // namespace lob
