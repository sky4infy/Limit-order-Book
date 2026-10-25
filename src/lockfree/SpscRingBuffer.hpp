#pragma once

#include <cstdint>
#include <atomic>
#include <vector>
#include <type_traits>
#include <new>
#include <cassert>

namespace lob {

/**
 * @brief Ultra-low-latency Single-Producer Single-Consumer (SPSC) Lock-Free Ring Buffer.
 * 
 * Architectural Highlights:
 * 1. Zero Contention: Lock-free, wait-free ring buffer using acquire-release memory semantics.
 * 2. False Sharing Eradication: Producers and Consumers never touch the same 64-byte cache line.
 *    Cursors and local cached cursors are isolated with explicit alignas(64) boundaries.
 * 3. Shadow Cursors (Batching Optimization):
 *    - Producer caches consumer's read cursor locally, avoiding atomic loads on every push.
 *    - Consumer caches producer's write cursor locally, avoiding atomic loads on every pop.
 * 4. Fast Modulo: Capacity is enforced as a compile-time power of 2, converting integer division
 *    into a single-cycle bitwise AND operation (index & (Capacity - 1)).
 */
template<typename T, size_t Capacity = 65536>
class SpscRingBuffer {
    static_assert((Capacity & (Capacity - 1)) == 0, "Capacity must be a power of 2!");
    static_assert(Capacity >= 2, "Capacity must be at least 2!");

public:
    static constexpr size_t MASK = Capacity - 1;

    SpscRingBuffer() {
        buffer_ = static_cast<T*>(::operator new[](Capacity * sizeof(T)));
        // Default initialize or zero-initialize elements if required
        for (size_t i = 0; i < Capacity; ++i) {
            new (&buffer_[i]) T();
        }
    }

    ~SpscRingBuffer() {
        for (size_t i = 0; i < Capacity; ++i) {
            buffer_[i].~T();
        }
        ::operator delete[](buffer_);
    }

    // Disable copies
    SpscRingBuffer(const SpscRingBuffer&) = delete;
    SpscRingBuffer& operator=(const SpscRingBuffer&) = delete;

    /**
     * @brief Producer Hot Path: Try to push an item without blocking.
     * @return true if pushed, false if buffer is full.
     */
    inline bool try_push(const T& item) noexcept {
        const uint64_t current_write = write_cursor_.load(std::memory_order_relaxed);

        // Check if buffer is full using local cached read cursor first (avoids cross-core cache load)
        if (current_write - cached_read_cursor_ >= Capacity) {
            // Reload consumer's atomic read cursor with acquire barrier
            cached_read_cursor_ = read_cursor_.load(std::memory_order_acquire);
            if (current_write - cached_read_cursor_ >= Capacity) {
                return false; // Queue is genuinely full
            }
        }

        // Store item into buffer
        buffer_[current_write & MASK] = item;

        // Publish to consumer with release semantics
        write_cursor_.store(current_write + 1, std::memory_order_release);
        return true;
    }

    /**
     * @brief Producer Hot Path: Emplace item in-place without copy.
     */
    template<typename... Args>
    inline bool try_emplace(Args&&... args) noexcept {
        const uint64_t current_write = write_cursor_.load(std::memory_order_relaxed);

        if (current_write - cached_read_cursor_ >= Capacity) {
            cached_read_cursor_ = read_cursor_.load(std::memory_order_acquire);
            if (current_write - cached_read_cursor_ >= Capacity) {
                return false;
            }
        }

        buffer_[current_write & MASK] = T(std::forward<Args>(args)...);
        write_cursor_.store(current_write + 1, std::memory_order_release);
        return true;
    }

    /**
     * @brief Consumer Hot Path: Try to pop an item without blocking.
     * @return true if popped, false if buffer is empty.
     */
    inline bool try_pop(T& item) noexcept {
        const uint64_t current_read = read_cursor_.load(std::memory_order_relaxed);

        // Check if buffer is empty using local cached write cursor first
        if (current_read == cached_write_cursor_) {
            // Reload producer's atomic write cursor with acquire barrier
            cached_write_cursor_ = write_cursor_.load(std::memory_order_acquire);
            if (current_read == cached_write_cursor_) {
                return false; // Queue is genuinely empty
            }
        }

        // Copy item from buffer
        item = buffer_[current_read & MASK];

        // Publish new read position to producer with release semantics
        read_cursor_.store(current_read + 1, std::memory_order_release);
        return true;
    }

    [[nodiscard]] inline bool empty() const noexcept {
        return read_cursor_.load(std::memory_order_relaxed) == write_cursor_.load(std::memory_order_relaxed);
    }

    [[nodiscard]] inline size_t size() const noexcept {
        uint64_t w = write_cursor_.load(std::memory_order_relaxed);
        uint64_t r = read_cursor_.load(std::memory_order_relaxed);
        return (w >= r) ? static_cast<size_t>(w - r) : 0;
    }

    [[nodiscard]] static constexpr size_t capacity() noexcept {
        return Capacity;
    }

private:
    // =========================================================================
    // PRODUCER CACHE LINE (Only written by Producer thread)
    // =========================================================================
    alignas(64) std::atomic<uint64_t> write_cursor_{0};
    uint64_t cached_read_cursor_{0};
    uint8_t  producer_padding_[64 - sizeof(std::atomic<uint64_t>) - sizeof(uint64_t)];

    // =========================================================================
    // CONSUMER CACHE LINE (Only written by Consumer thread)
    // =========================================================================
    alignas(64) std::atomic<uint64_t> read_cursor_{0};
    uint64_t cached_write_cursor_{0};
    uint8_t  consumer_padding_[64 - sizeof(std::atomic<uint64_t>) - sizeof(uint64_t)];

    // =========================================================================
    // DATA BUFFER (Separated onto its own cache lines)
    // =========================================================================
    alignas(64) T* buffer_{nullptr};
};

} // namespace lob
