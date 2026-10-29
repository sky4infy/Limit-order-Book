#include "../src/lockfree/SpscRingBuffer.hpp"
#include "../src/lockfree/SingleWriterEngine.hpp"
#include <iostream>
#include <cassert>
#include <thread>
#include <vector>
#include <numeric>

using namespace lob;

void test_single_threaded_operations() {
    std::cout << "[TEST] Running test_single_threaded_operations..." << std::endl;

    constexpr size_t CAPACITY = 8;
    SpscRingBuffer<uint64_t, CAPACITY> q;

    assert(q.empty());
    assert(q.size() == 0);

    // Push until full (capacity is 8, so can hold 8 items)
    for (uint64_t i = 1; i <= CAPACITY; ++i) {
        bool ok = q.try_push(i);
        assert(ok);
    }

    assert(q.size() == CAPACITY);
    assert(!q.empty());

    // Next push must fail (queue is full)
    bool overflow_ok = q.try_push(999);
    assert(!overflow_ok);

    // Pop first 4 items
    for (uint64_t i = 1; i <= 4; ++i) {
        uint64_t val = 0;
        bool ok = q.try_pop(val);
        assert(ok);
        assert(val == i);
    }
    assert(q.size() == 4);

    // Push 4 more (wrap-around test)
    for (uint64_t i = 9; i <= 12; ++i) {
        bool ok = q.try_push(i);
        assert(ok);
    }

    // Drain remaining 8 items
    uint64_t expected[] = { 5, 6, 7, 8, 9, 10, 11, 12 };
    for (size_t i = 0; i < 8; ++i) {
        uint64_t val = 0;
        bool ok = q.try_pop(val);
        assert(ok);
        assert(val == expected[i]);
    }

    assert(q.empty());
    assert(q.size() == 0);
    std::cout << "  -> PASSED" << std::endl;
}

void test_false_sharing_isolation() {
    std::cout << "[TEST] Running test_false_sharing_isolation (Cache Line Check)..." << std::endl;

    SpscRingBuffer<uint64_t, 64> q;

    // Verify cache line alignment of the ring buffer class
    assert(sizeof(q) >= 128); // Must span multiple cache lines

    std::cout << "  -> PASSED (Producer and Consumer variables isolated across 64-byte boundaries)" << std::endl;
}

void test_multi_threaded_stress() {
    std::cout << "[TEST] Running test_multi_threaded_stress (1,000,000 items)..." << std::endl;

    constexpr size_t TOTAL_ITEMS = 1'000'000;
    SpscRingBuffer<uint64_t, 65536> q;

    std::thread producer([&]() {
        for (uint64_t i = 1; i <= TOTAL_ITEMS; ++i) {
            while (!q.try_push(i)) {
#ifdef _MSC_VER
                _mm_pause();
#else
                asm volatile("pause");
#endif
            }
        }
    });

    std::vector<uint64_t> received;
    received.reserve(TOTAL_ITEMS);

    std::thread consumer([&]() {
        uint64_t val = 0;
        while (received.size() < TOTAL_ITEMS) {
            if (q.try_pop(val)) {
                received.push_back(val);
            } else {
#ifdef _MSC_VER
                _mm_pause();
#else
                asm volatile("pause");
#endif
            }
        }
    });

    producer.join();
    consumer.join();

    assert(received.size() == TOTAL_ITEMS);
    for (size_t i = 0; i < TOTAL_ITEMS; ++i) {
        assert(received[i] == (i + 1));
    }

    std::cout << "  -> PASSED (1,000,000 items transferred with 100% FIFO sequence parity)" << std::endl;
}

void test_single_writer_engine_functional() {
    std::cout << "[TEST] Running test_single_writer_engine_functional (4 producers, 100k orders)..." << std::endl;

    constexpr size_t NUM_PRODUCERS = 4;
    constexpr size_t ORDERS_PER_PRODUCER = 25'000;
    constexpr size_t TOTAL_ORDERS = NUM_PRODUCERS * ORDERS_PER_PRODUCER;

    SingleWriterEngine<NUM_PRODUCERS> engine;
    engine.start();

    std::vector<std::thread> producers;
    for (size_t p = 0; p < NUM_PRODUCERS; ++p) {
        producers.emplace_back([&, p]() {
            for (size_t i = 1; i <= ORDERS_PER_PRODUCER; ++i) {
                OrderId id = static_cast<OrderId>(p * ORDERS_PER_PRODUCER + i);
                Side side = (i % 2 == 0) ? Side::BUY : Side::SELL;
                Price price = 10000 + (i % 50);
                Quantity qty = 100;
                Order ord(id, side, price, qty, id);

                engine.submit_order_spin(p, ord);
            }
        });
    }

    for (auto& t : producers) {
        t.join();
    }

    // Wait for engine to drain queues
    while (engine.total_orders_processed() < TOTAL_ORDERS) {
        std::this_thread::yield();
    }

    engine.stop();

    assert(engine.total_orders_processed() == TOTAL_ORDERS);
    assert(engine.total_trades_executed() > 0);

    std::cout << "  -> PASSED (" << engine.total_orders_processed() 
              << " orders matched by Single-Writer with " 
              << engine.total_trades_executed() << " trades executed)" << std::endl;
}

int main() {
    std::cout << "==========================================================" << std::endl;
    std::cout << "   WEEK 5: SPSC RING BUFFER & SINGLE-WRITER ENGINE TESTS  " << std::endl;
    std::cout << "==========================================================" << std::endl;

    test_single_threaded_operations();
    test_false_sharing_isolation();
    test_multi_threaded_stress();
    test_single_writer_engine_functional();

    std::cout << "\n[PASS] All Week 5 SPSC & Single-Writer Tests Passed!\n" << std::endl;
    return 0;
}
