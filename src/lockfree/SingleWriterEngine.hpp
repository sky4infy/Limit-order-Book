#pragma once

#include "SpscRingBuffer.hpp"
#include "ThreadAffinity.hpp"
#include "../optimized/OrderBookOptimized.hpp"
#include <thread>
#include <atomic>
#include <vector>
#include <memory>
#include <functional>

#ifdef _MSC_VER
#include <intrin.h>
#pragma warning(disable: 4324) // structure was padded due to alignment specifier (intentional)
#else
#include <immintrin.h>
#endif

namespace lob {

/**
 * @brief Phase 3 Architecture: The Single-Writer Matching Engine (Disruptor Pattern).
 * 
 * In High-Frequency Trading, having multiple threads fight over a mutex-protected order book
 * destroys performance:
 * 1. OS Mutex Sleeps: When contention occurs, the OS scheduler puts threads to sleep (5-50µs penalty).
 * 2. MESI Cache Ping-Pong: Multiple CPU cores writing to the same book memory invalidate each other's L1 cache.
 * 
 * The Single-Writer Principle:
 * - Inbound gateway threads submit orders into dedicated Lock-Free SPSC Queues.
 * - ONLY ONE dedicated Matching Engine Thread writes to the Order Book at full CPU cache speed.
 * - Zero mutexes, zero locks, zero context switches on the matching hot path.
 */
template<size_t NumProducers = 4, size_t QueueCapacity = 65536>
class SingleWriterEngine {
public:
    explicit SingleWriterEngine(uint32_t cpu_core = 2) 
        : engine_core_id_(cpu_core) 
    {
        for (size_t i = 0; i < NumProducers; ++i) {
            inbound_queues_.push_back(std::make_unique<SpscRingBuffer<Order, QueueCapacity>>());
        }
    }

    ~SingleWriterEngine() {
        stop();
    }

    void start() {
        if (running_.exchange(true)) return;
        engine_thread_ = std::thread(&SingleWriterEngine::worker_loop, this);
    }

    void stop() {
        if (!running_.exchange(false)) return;
        if (engine_thread_.joinable()) {
            engine_thread_.join();
        }
    }

    /**
     * @brief Producer Gateway Hot Path: Submit order into producer's dedicated SPSC queue.
     * @param producer_id ID of the calling producer thread (0 .. NumProducers-1).
     * @param order The order to match.
     * @return true if submitted, false if queue is full.
     */
    inline bool submit_order(size_t producer_id, const Order& order) noexcept {
        assert(producer_id < NumProducers);
        return inbound_queues_[producer_id]->try_push(order);
    }

    /**
     * @brief Blocking submit: Spins until slot is available (for benchmarking).
     */
    inline void submit_order_spin(size_t producer_id, const Order& order) noexcept {
        assert(producer_id < NumProducers);
        while (!inbound_queues_[producer_id]->try_push(order)) {
#ifdef _MSC_VER
            _mm_pause();
#else
            asm volatile("pause");
#endif
        }
    }

    [[nodiscard]] uint64_t total_orders_processed() const noexcept {
        return total_orders_processed_.load(std::memory_order_relaxed);
    }

    [[nodiscard]] uint64_t total_trades_executed() const noexcept {
        return total_trades_executed_.load(std::memory_order_relaxed);
    }

    [[nodiscard]] const OrderBookOptimized& book() const noexcept {
        return book_;
    }

    void reset() {
        stop();
        book_.clear();
        total_orders_processed_.store(0, std::memory_order_relaxed);
        total_trades_executed_.store(0, std::memory_order_relaxed);
    }

private:
    uint32_t engine_core_id_;
    std::atomic<bool> running_{false};
    std::thread engine_thread_;

    // Order Book owned exclusively by the Single-Writer thread
    OrderBookOptimized book_;

    // Dedicated Lock-Free SPSC queue for each producer gateway
    std::vector<std::unique_ptr<SpscRingBuffer<Order, QueueCapacity>>> inbound_queues_;

    // Telemetry counters
    alignas(64) std::atomic<uint64_t> total_orders_processed_{0};
    alignas(64) std::atomic<uint64_t> total_trades_executed_{0};

    void worker_loop() {
        // Pin Single-Writer core to isolated physical CPU core
        ThreadAffinity::pin_current_thread_to_core(engine_core_id_);

        constexpr size_t BATCH_DRAIN_LIMIT = 64;
        Order ord;

        while (running_.load(std::memory_order_relaxed)) {
            bool work_done = false;

            // Round-robin poll across all producer gateway queues
            for (size_t p = 0; p < NumProducers; ++p) {
                size_t batch = 0;
                while (batch < BATCH_DRAIN_LIMIT && inbound_queues_[p]->try_pop(ord)) {
                    auto trades = book_.add_order(ord);
                    total_trades_executed_.fetch_add(trades.size(), std::memory_order_relaxed);
                    total_orders_processed_.fetch_add(1, std::memory_order_relaxed);
                    work_done = true;
                    ++batch;
                }
            }

            // If all queues were empty, issue CPU PAUSE to prevent pipeline spin burn
            if (!work_done) {
#ifdef _MSC_VER
                _mm_pause();
#else
                asm volatile("pause");
#endif
            }
        }

        // Drain any remaining orders upon shutdown
        for (size_t p = 0; p < NumProducers; ++p) {
            while (inbound_queues_[p]->try_pop(ord)) {
                auto trades = book_.add_order(ord);
                total_trades_executed_.fetch_add(trades.size(), std::memory_order_relaxed);
                total_orders_processed_.fetch_add(1, std::memory_order_relaxed);
            }
        }
    }
};

} // namespace lob
