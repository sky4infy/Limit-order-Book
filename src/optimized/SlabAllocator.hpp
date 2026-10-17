#pragma once

#include "OptimizedOrder.hpp"
#include <vector>
#include <cstdint>
#include <stdexcept>
#include <cassert>

namespace lob {

/**
 * @brief Zero-Allocation Contiguous Slab Allocator (Object Pool)
 * 
 * Pre-allocates a contiguous pool of objects at startup, completely eliminating
 * dynamic OS calls (malloc/free, new/delete) on the critical trading path.
 * 
 * Key Performance Features:
 * - O(1) Allocation: Pops an index from a pre-filled contiguous free stack.
 * - O(1) Deallocation: Pushes the freed index back onto the free stack.
 * - Contiguous Memory: All objects sit in adjacent cache lines in physical RAM,
 *   maximizing CPU hardware prefetcher efficiency and cache hit rates.
 * - Zero Hot-Path Sycalls: 0 locks, 0 kernel transitions, 0 latency tail spikes.
 */
template<typename T, size_t Capacity = 1'000'000>
class SlabAllocator {
public:
    SlabAllocator() {
        pool_.resize(Capacity);
        free_stack_.reserve(Capacity);
        reset();
    }

    /**
     * @brief Allocate an object from the pool in O(1)
     * @return The 32-bit pool index of the allocated slot, or INVALID_INDEX if exhausted
     */
    [[nodiscard]] uint32_t allocate() noexcept {
        if (free_stack_.empty()) [[unlikely]] {
            return INVALID_INDEX;
        }

        uint32_t idx = free_stack_.back();
        free_stack_.pop_back();
        return idx;
    }

    /**
     * @brief Return an object back to the free pool in O(1)
     * @param index The 32-bit pool index to reclaim
     */
    void deallocate(uint32_t index) noexcept {
        assert(index < Capacity && "Deallocating out-of-bounds index!");
        free_stack_.push_back(index);
    }

    /**
     * @brief Access an allocated object by pool index
     */
    [[nodiscard]] T& get(uint32_t index) noexcept {
        assert(index < Capacity && "Accessing out-of-bounds index!");
        return pool_[index];
    }

    [[nodiscard]] const T& get(uint32_t index) const noexcept {
        assert(index < Capacity && "Accessing out-of-bounds index!");
        return pool_[index];
    }

    [[nodiscard]] T& operator[](uint32_t index) noexcept {
        return pool_[index];
    }

    [[nodiscard]] const T& operator[](uint32_t index) const noexcept {
        return pool_[index];
    }

    /**
     * @brief Reset the allocator to initial state (all slots freed)
     */
    void reset() noexcept {
        free_stack_.clear();
        // Fill free stack in reverse order so index 0 is allocated first (spatial cache locality)
        for (int64_t i = static_cast<int64_t>(Capacity) - 1; i >= 0; --i) {
            free_stack_.push_back(static_cast<uint32_t>(i));
        }
    }

    [[nodiscard]] size_t size() const noexcept {
        return Capacity - free_stack_.size();
    }

    [[nodiscard]] size_t available() const noexcept {
        return free_stack_.size();
    }

    [[nodiscard]] constexpr size_t capacity() const noexcept {
        return Capacity;
    }

    [[nodiscard]] bool is_empty() const noexcept {
        return free_stack_.size() == Capacity;
    }

    [[nodiscard]] bool is_full() const noexcept {
        return free_stack_.empty();
    }

private:
    std::vector<T> pool_;
    std::vector<uint32_t> free_stack_;
};

} // namespace lob
